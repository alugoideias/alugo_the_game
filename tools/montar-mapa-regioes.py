"""Monta assets/atlas/mapa-regioes.png: ilhas do mapa de Digitus feitas só com a arte das fases.

Cada ilha é um recorte do fundo da região (assets/fundos) com o marco dela, sobre
um bloco de chão com os tiles da própria fase (assets/tiles). Nada é desenhado:
os pixels vêm dos PNGs existentes; só há recorte, máscara, contorno e escurecimento
para o estado "tomada pelo chefe". Densidade dos atlas: desenhar com s=.5.
Uso: python tools/montar-mapa-regioes.py  (requer Pillow)
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'atlas' / 'mapa-regioes.png'
INK = (5, 8, 14, 255)
W = 160                       # 5 tiles de 16 px, ampliados 2x como no jogo

# região -> (mundo dos fundos/tiles, canto do recorte no fundo 320x224, altura da cena)
REG = {
    'ruido': ('vale-confusao', (24, 4), 80),
    'pressa': ('distrito-prazos', (14, 4), 80),
    'silo': ('fortaleza-desconectada', (0, 22), 80),
    'dona': ('labirinto-processos', (40, 4), 80),
    'torta': ('oficina-rascunhos', (160, 82), 48),
    'apagao': ('arquivo-esquecimento', (0, 24), 64),
}


def tiles(world):
    ts = Image.open(ROOT / 'assets' / 'tiles' / f'{world}.png').convert('RGBA')
    return [ts.crop(((i % 4) * 16, (i // 4) * 16, (i % 4) * 16 + 16, (i // 4) * 16 + 16)).resize((32, 32), Image.NEAREST)
            for i in range(12)]


def chao(world, w):
    """Bloco flutuante: tampo completo e base afinando, com os tiles da fase."""
    t = tiles(world)
    n = w // 32
    img = Image.new('RGBA', (w, 56), (0, 0, 0, 0))
    top = [0] + [1, 2] * n
    for i in range(n):
        img.alpha_composite(t[top[i] if i < n - 1 else 3], (i * 32, 0))
    body = [4] + [5, 6] * n
    for i in range(n - 1):                                   # segunda fileira: meio tile, recuada
        k = body[i] if i < n - 2 else 7
        img.alpha_composite(t[k].crop((0, 0, 32, 16)), (16 + i * 32, 32))
    for i in range(n - 3):                                   # ponta de baixo
        k = 4 if i == 0 else 7 if i == n - 4 else 5
        img.alpha_composite(t[k].crop((0, 0, 32, 8)), (48 + i * 32, 48))
    return img


def contorno(img):
    a = img.split()[3].point(lambda v: 255 if v > 0 else 0)
    ring = a.filter(ImageFilter.MaxFilter(3))
    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    out.paste(Image.new('RGBA', img.size, INK), (0, 0), ring)
    out.alpha_composite(img)
    return out


def ilha(k):
    world, (cx, cy), sh = REG[k]
    bg = Image.open(ROOT / 'assets' / 'fundos' / f'{world}.png').convert('RGBA')
    cena = bg.crop((cx, cy, cx + W, cy + sh))
    m = Image.new('L', (W, sh), 0)
    ImageDraw.Draw(m).rounded_rectangle((2, 0, W - 3, sh + 40), radius=26, fill=255)   # cúpula
    img = Image.new('RGBA', (W + 2, sh + 56 + 2), (0, 0, 0, 0))
    img.paste(cena, (1, 1), m)
    img.alpha_composite(chao(world, W), (1, sh + 1))
    return contorno(img), sh


def tomada(img, k=.55):
    """Estado com o chefe: mesma arte, apagada e dessaturada."""
    rgb, a = img.convert('RGB'), img.split()[3]
    rgb = ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(.45)).enhance(k)
    out = rgb.convert('RGBA')
    out.putalpha(a)
    return out


frames = []
for k in REG:
    img, sh = ilha(k)
    anchor = (W // 2 + 1, sh + 1 + 16)       # o caminho chega 8 px do jogo abaixo do tampo
    if k == 'apagao':
        frames += [('apagao-lacrado', tomada(img, .4), anchor), ('apagao', tomada(img, .75), anchor),
                   ('apagao-restaurada', img, anchor)]
    else:
        frames += [(k, tomada(img), anchor), (k + '-restaurada', img, anchor)]
hub = contorno(chao('vale-confusao', 192).crop((0, 0, 192, 40)))
frames.append(('hub', hub, (96, -20)))      # tampo 10 px abaixo do ponto, onde o farol pousa

# empacota em linhas
x = y = row_h = 0
places, AW = [], 4 * (W + 2)
for name, img, anc in frames:
    if x + img.width > AW:
        x, y, row_h = 0, y + row_h, 0
    places.append((name, img, anc, x, y))
    x += img.width
    row_h = max(row_h, img.height)
atlas = Image.new('RGBA', (AW, y + row_h), (0, 0, 0, 0))
rects = {}
for name, img, (ax, ay), px, py in places:
    atlas.alpha_composite(img, (px, py))
    rects[name] = [px, py, img.width, img.height, ax, ay]
atlas.save(OUT)
print(json.dumps(rects, separators=(',', ':')))
