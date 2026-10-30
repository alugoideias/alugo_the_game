"""Gera assets/atlas/projeteis-chefes.png: projéteis dos chefes em pixel art.

Estilo e paleta em tools/pixelart.py.
Uso: python tools/gerar-projeteis-chefes.py  (requer Pillow)
"""
from pathlib import Path
import json, math
from PIL import Image
from pixelart import Cell, rot

CELL = 32
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'atlas' / 'projeteis-chefes.png'

# ---- Pressa: ponteiro de relógio arremessado (gira em 4 quadros) ----
def ponteiro(a):
    c = Cell()
    c.poly(rot([(5, 14.2), (20, 14), (20, 18), (5, 17.8)], a), 'steel')        # haste
    c.poly(rot([(18, 10.5), (29, 16), (18, 21.5), (20.5, 16)], a), 'gold')     # ponta de seta
    ex, ey = rot([(5.5, 16)], a)[0]
    c.circle(ex, ey, 3.6, 'gold')                                               # contrapeso
    c.circle(16, 16, 3, 'cream')                                                # eixo
    c.px(16, 16, None, 0)
    return c


# ---- Pressa: relógio que cria a zona lenta (face ciano = tempo lento) ----
def relogio(k):
    c = Cell()
    c.circle(9.5, 7.5, 3.6, 'gold'); c.circle(22.5, 7.5, 3.6, 'gold')          # sinos
    c.circle(16, 17, 11, 'gold')
    c.circle(16, 17, 8, 'cyan')
    c.rect(9, 26, 4, 3, 'gold'); c.rect(19, 26, 4, 3, 'gold')                  # pés
    for i in range(12):
        ang = i / 12 * math.tau
        if i % 3 == 0:
            c.px(round(16 + math.cos(ang) * 6.5 - .5), round(17 + math.sin(ang) * 6.5 - .5), 'cyan', 0)
    a = -math.pi / 2 + k * math.pi / 2
    for i in range(6):
        c.px(16 + round(math.cos(a) * i), 17 + round(math.sin(a) * i), None, 0)
    c.px(16, 17, None, 0); c.px(17, 17, None, 0)
    c.px(16, 16, None, 0)
    c.px(11, 13, 'cyan', 3); c.px(12, 12, 'cyan', 3); c.px(13, 11, 'cyan', 3)                          # reflexo
    return c


# ---- Barão Silo: cadeado arremessado ----
def cadeado(k):
    c = Cell()
    c.ring(16, 11, 5, 8.5, 'steel')
    c.rect(6, 12, 20, 16, 'gold')
    c.rect(15, 17, 2, 2, 'ink'); c.rect(15, 19, 2, 4, 'ink')
    c.rect(14, 17, 4, 2, 'ink')
    if k:
        c.px(8, 14, 'gold', 3); c.px(9, 14, 'gold', 3); c.px(8, 15, 'gold', 3)
        c.px(23, 24, 'cream', 3)
    for x in (8, 12, 20, 24):
        c.px(x, 26, 'gold', 0)
    return c


# ---- Dona Complexa: peça de quebra-cabeça em órbita ----
def peca(a):
    c = Cell()
    body = rot([(8, 10), (24, 10), (24, 26), (8, 26)], a)
    c.poly(body, 'red')
    tx, ty = rot([(16, 7.5)], a)[0]
    c.circle(tx, ty, 3.4, 'red')                                                # encaixe
    sx, sy = rot([(26.5, 18)], a)[0]
    c.circle(sx, sy, 3.2, 'red')
    hx, hy = rot([(8, 18)], a)[0]
    for y in range(CELL):                                                       # recorte (furo)
        for x in range(CELL):
            if (x + .5 - hx) ** 2 + (y + .5 - hy) ** 2 <= 9:
                c.m[y][x] = None
    return c


# ---- Apagão/Arquivista: pasta de arquivo girando ----
def arquivo(k):
    c = Cell()
    if k == 0:
        c.poly([(6, 11), (13, 11), (15, 13), (26, 13), (26, 24), (6, 24)], 'manila')
        c.rect(9, 15, 14, 1, 'cream'); c.rect(9, 18, 10, 1, 'cream')
        for x in range(9, 23): c.px(x, 15, 'cream', 3)
        for x in range(9, 19): c.px(x, 18, 'cream', 2)
        c.px(7, 12, 'manila', 3)
    else:
        c.poly([(8, 8), (24, 12), (22, 26), (6, 22)], 'manila')
        c.poly([(11, 6), (20, 8), (19, 13), (10, 11)], 'cream')                # folha escapando
        c.line(11, 15, 20, 17, 'manila', 1)
        for x, y in ((11, 15), (13, 16), (15, 16), (17, 17), (19, 17)): c.px(x, y, 'manila', 0)
    return c


# ---- Apagão/Núcleo: esfera de vazio ----
def vazio(k):
    c = Cell()
    c.circle(16, 16, 9.5, 'gold')
    c.circle(16, 16, 7.5, 'void')
    for i in range(8):
        ang = i / 8 * math.tau + k * math.pi / 8
        x, y = 16 + math.cos(ang) * 8.5, 16 + math.sin(ang) * 8.5
        c.px(int(x), int(y), 'gold', 3 if i % 2 == 0 else 1)
    c.px(12, 12, 'void', 3); c.px(13, 12, 'void', 3); c.px(12, 13, 'void', 3)
    if k:
        for x, y in ((4, 9), (27, 22), (25, 6)):
            c.px(x, y, 'gold', 3)
    return c


# ---- Ideia Torta: descarga elétrica ----
def raio(k):
    c = Cell()
    pts = [(18, 3), (9, 17), (15, 17), (12, 29), (23, 13), (17, 13), (21, 3)]
    if k:
        pts = [(x + (1 if y < 16 else -1), y) for x, y in pts]
    c.poly(pts, 'spark')
    for x, y in ((6, 8), (25, 20), (8, 25)) if k else ((24, 7), (7, 21)):
        c.px(x, y, 'spark', 3)
    return c


# ---- Ruído: tiro de foco (mira) ----
def foco(k):
    c = Cell()
    c.circle(16, 16, 8, 'red')
    c.circle(16, 16, 4, 'cream')
    c.px(16, 16, 'red', 2); c.px(15, 16, 'red', 2)
    if k:
        for d in (-11, 10):
            c.px(16 + d, 16, 'red', 3); c.px(16, 16 + d, 'red', 3)
    return c


# ---- Dona Complexa: nó que inverte controles ----
def no(k):
    c = Cell()
    ph = k * math.pi / 2
    prev = None
    for i in range(90):                                                         # nó de trevo
        t = i / 89 * math.tau
        x = 16 + (math.sin(t) + 2 * math.sin(2 * t)) * 3.2
        y = 16 + (math.cos(t) - 2 * math.cos(2 * t)) * 3.2
        x, y = rot([(x, y)], ph / 3)[0]
        if prev:
            c.line(prev[0], prev[1], x, y, 'pink', 2.2)
        prev = (x, y)
    return c


FRAMES = []
for i in range(4): FRAMES.append((f'ponteiro-{i}', ponteiro(i * math.pi / 4)))
for i in range(2): FRAMES.append((f'relogio-{i}', relogio(i)))
for i in range(2): FRAMES.append((f'cadeado-{i}', cadeado(i)))
for i in range(2): FRAMES.append((f'peca-{i}', peca(i * math.pi / 2)))
for i in range(2): FRAMES.append((f'arquivo-{i}', arquivo(i)))
for i in range(2): FRAMES.append((f'vazio-{i}', vazio(i)))
for i in range(2): FRAMES.append((f'raio-{i}', raio(i)))
for i in range(2): FRAMES.append((f'foco-{i}', foco(i)))
for i in range(2): FRAMES.append((f'no-{i}', no(i)))

COLS = 8
rows = math.ceil(len(FRAMES) / COLS)
atlas = Image.new('RGBA', (COLS * CELL, rows * CELL), (0, 0, 0, 0))
rects = {}
for n, (name, cell) in enumerate(FRAMES):
    x, y = (n % COLS) * CELL, (n // COLS) * CELL
    atlas.alpha_composite(cell.render(), (x, y))
    rects[name] = [x, y, CELL, CELL, CELL // 2, CELL // 2]
OUT.parent.mkdir(parents=True, exist_ok=True)
atlas.save(OUT)
print(json.dumps(rects, separators=(',', ':')))
