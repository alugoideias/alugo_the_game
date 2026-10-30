"""Gera assets/atlas/porta-chefe.png: porta modular das arenas de chefe.

Peças: pilar (repete na vertical), moldura, folha (persiana que sobe), barras de
energia (arena selada), cadeado (faltam fragmentos), luzes de estado e moldura do
retrato. Medidas em pixels da arte (2x o jogo): porta com 104 de largura e vão de
64x96, como em drawBossGate(). Estilo e paleta em tools/pixelart.py.
Uso: python tools/gerar-porta-chefe.py  (requer Pillow)
"""
from pathlib import Path
import json
from pixelart import Cell, pack

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'atlas' / 'porta-chefe.png'
WD, GAP_X, GAP_W, GAP_H, LINTEL = 104, 20, 64, 96, 28


def hazard(c, x0, y0, w, h, phase=0):
    """Faixa de perigo dourada/escura em diagonal."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            k = (x + y + phase) // 4 % 2
            c.px(x, y, 'gold' if k else 'plate', 2 if k else 0)


def rivet(c, x, y):
    c.px(x, y, 'trim', 3); c.px(x + 1, y, 'trim', 1)
    c.px(x, y + 1, 'trim', 1); c.px(x + 1, y + 1, 'steel', 0)


def post(c, x0, y0, h, inner_right):
    """Montante lateral: placa creme com trilho escuro e faixa de perigo."""
    c.rect(x0, y0, 20, h, 'trim')
    rail = x0 + 14 if inner_right else x0 + 2
    c.rect(rail, y0, 4, h, 'steel')
    band = x0 + 4 if inner_right else x0 + 8
    hazard(c, band, y0, 8, h)
    c.vline(band - 1, y0, y0 + h, 'trim', 1)
    c.vline(band + 8, y0, y0 + h, 'trim', 1)


def pilar():
    c = Cell(WD, 32)
    post(c, 0, 0, 32, True)
    post(c, WD - 20, 0, 32, False)
    c.rect(20, 0, 64, 32, 'plate')
    c.hline(20, 84, 0, 'steel', 2)                  # junta entre placas
    c.hline(20, 84, 31, 'plate', 0)
    for x in (24, 78):
        rivet(c, x, 4); rivet(c, x, 26)
    c.rect(36, 10, 32, 12, 'steel')                 # chapa central
    c.hline(37, 67, 15, 'gold', 1); c.hline(37, 67, 16, 'gold', 2)
    return c.render(outline=False)


def moldura():
    h = LINTEL + GAP_H
    c = Cell(WD, h)
    post(c, 0, LINTEL, GAP_H, True)
    post(c, WD - 20, LINTEL, GAP_H, False)
    c.rect(0, 0, WD, LINTEL, 'steel')               # verga
    c.rect(2, 2, WD - 4, 4, 'trim')
    c.hline(2, WD - 2, LINTEL - 3, 'gold', 2); c.hline(2, WD - 2, LINTEL - 2, 'gold', 1)
    for x in (26, 66):                              # encaixes das luzes
        c.rect(x, 9, 12, 12, 'ink')
        c.hline(x, x + 12, 21, 'steel', 3)
    c.rect(44, 9, 16, 12, 'plate')                  # placa central
    c.hline(46, 58, 14, 'gold', 2); c.hline(46, 58, 16, 'gold', 1)
    for x in (6, WD - 8):
        rivet(c, x, 10); rivet(c, x, 17)
    for y in (LINTEL + 6, LINTEL + 46, h - 10):     # braçadeiras dos montantes
        for x0 in (0, WD - 20):
            c.rect(x0, y, 20, 4, 'gold')
    hazard(c, GAP_X, h - 4, GAP_W, 4)               # soleira
    c.clear(GAP_X, LINTEL, GAP_W, GAP_H - 4)        # vão vazado
    return c.render()


def folha():
    c = Cell(GAP_W, GAP_H)
    for i in range(GAP_H // 8):                     # lâminas da persiana
        y = i * 8
        c.rect(0, y, GAP_W, 8, 'plate')
        c.hline(0, GAP_W, y, 'steel', 2)
        c.hline(0, GAP_W, y + 7, 'plate', 0)
    for y in range(0, GAP_H - 12):                  # circuito, como em porta-circuito.png
        x = 31 + (2 if (y // 16) % 2 else -2)
        c.px(x, y, 'gold', 2); c.px(x + 1, y, 'gold', 1)
    for y in range(0, GAP_H - 12, 16):
        for x in range(29, 35):
            c.px(x, y, 'gold', 2)
    c.rect(0, GAP_H - 12, GAP_W, 12, 'steel')       # barra de baixo
    hazard(c, 2, GAP_H - 8, GAP_W - 4, 4, 2)
    c.rect(26, GAP_H - 12, 12, 3, 'trim')           # puxador
    return c.render(outline=False)


def barras(k):
    c = Cell(GAP_W, GAP_H)
    for x in (4, 21, 37, 53):
        c.rect(x, 0, 7, GAP_H, 'steel')
        for y in range(2, GAP_H - 2):
            hot = (y // 5 + x // 16 + k) % 3 != 0     # pulso de energia descendo
            for dx, t in ((1, 1), (2, 2), (3, 3 if hot else 2), (4, 2), (5, 1)):
                c.px(x + dx, y, 'red', t)
    for y in (0, GAP_H - 6):                        # travessas
        c.rect(0, y, GAP_W, 6, 'steel')
        c.hline(1, GAP_W - 1, y + 2, 'red', 2 + k)
        c.hline(1, GAP_W - 1, y + 3, 'red', 1 + k)
    return c.render()


def cadeado():
    c = Cell(32, 32)
    c.ring(16, 11, 5, 9, 'steel')
    c.rect(5, 12, 22, 17, 'gold')
    c.poly([(16, 15), (20, 19), (16, 23), (12, 19)], 'cream')    # fragmento no lugar da chave
    c.px(16, 17, 'gold', 0); c.px(16, 18, 'gold', 0); c.px(16, 19, 'gold', 0)
    c.px(7, 14, 'gold', 3); c.px(8, 14, 'gold', 3); c.px(7, 15, 'gold', 3)
    for x in (7, 11, 21, 25):
        c.px(x, 27, 'gold', 0)
    return c.render()


def luz(cor):
    c = Cell(12, 12)
    c.circle(6, 6, 5, cor)
    c.px(4, 3, cor, 3); c.px(3, 4, cor, 3)
    return c.render()


def retrato():
    c = Cell(60, 60)
    c.rect(0, 0, 60, 60, 'gold')
    c.rect(3, 3, 54, 54, 'steel')
    for x, y in ((1, 1), (56, 1), (1, 56), (56, 56)):
        c.rect(x, y, 3, 3, 'trim')
    c.clear(6, 6, 48, 48)
    return c.render()


frames = [
    ('pilar', pilar(), (WD // 2, 0)),
    ('moldura', moldura(), (WD // 2, LINTEL + GAP_H)),
    ('folha', folha(), (GAP_W // 2, GAP_H)),
    ('barras-0', barras(0), (GAP_W // 2, GAP_H)),
    ('barras-1', barras(1), (GAP_W // 2, GAP_H)),
    ('retrato', retrato(), (30, 30)),
    ('cadeado', cadeado(), (16, 16)),
    ('luz-vermelha', luz('red'), (6, 6)),
    ('luz-ambar', luz('gold'), (6, 6)),
    ('luz-verde', luz('green'), (6, 6)),
    ('luz-apagada', luz('steel'), (6, 6)),
]
atlas, rects = pack(frames, 512)
atlas.save(OUT)
print(json.dumps(rects, separators=(',', ':')))
