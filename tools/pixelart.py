"""Base comum dos geradores de pixel art: paleta da marca, formas e atlas.

Mesma densidade dos outros atlas (1 pixel da arte = meio pixel do jogo, desenhado
com s=.5), contorno escuro e luz vinda de cima/esquerda, como nos personagens.
"""
import math
from PIL import Image

# paleta tirada de personagens/*.png, atlas/projeteis-extra.png e atlas/porta-circuito.png
INK = (5, 8, 14)
PAL = {
    'gold': [(120, 48, 6), (198, 104, 3), (253, 182, 5), (254, 238, 196)],
    'cream': [(150, 120, 80), (243, 216, 162), (254, 238, 211), (255, 252, 242)],
    'trim': [(120, 110, 100), (180, 168, 155), (215, 199, 182), (247, 233, 207)],
    'steel': [(20, 25, 33), (38, 45, 56), (79, 83, 88), (170, 182, 171)],
    'plate': [(12, 15, 20), (25, 31, 40), (36, 42, 53), (60, 66, 76)],
    'cyan': [(15, 60, 80), (40, 140, 170), (127, 224, 255), (232, 251, 255)],
    'green': [(10, 60, 40), (30, 140, 90), (93, 252, 154), (220, 255, 230)],
    'red': [(90, 20, 20), (150, 38, 29), (230, 70, 80), (255, 190, 180)],
    'pink': [(100, 30, 50), (190, 70, 100), (255, 138, 154), (255, 220, 225)],
    'manila': [(110, 70, 20), (200, 160, 64), (232, 200, 106), (255, 243, 200)],
    'void': [(0, 0, 0), (10, 10, 14), (28, 28, 32), (57, 57, 61)],
    'spark': [(198, 104, 3), (253, 182, 5), (255, 240, 150), (255, 252, 230)],
}


class Cell:
    """Pinta formas por cor-base; depois aplica sombra, luz e contorno."""
    def __init__(self, w=32, h=None):
        self.w, self.h = w, h or w
        self.m = [[None] * self.w for _ in range(self.h)]   # nome da cor base
        self.fix = {}                                        # pixels com tom fixo

    def _put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.m[y][x] = c

    def _each(self):
        for y in range(self.h):
            for x in range(self.w):
                yield x, y

    def poly(self, pts, c):
        for x, y in self._each():
            if inside(x + .5, y + .5, pts):
                self._put(x, y, c)

    def circle(self, cx, cy, r, c):
        for x, y in self._each():
            if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r:
                self._put(x, y, c)

    def ring(self, cx, cy, r0, r1, c):
        for x, y in self._each():
            if r0 <= math.hypot(x + .5 - cx, y + .5 - cy) <= r1:
                self._put(x, y, c)

    def rect(self, x0, y0, w, h, c):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                self._put(x, y, c)

    def clear(self, x0, y0, w, h):
        self.rect(x0, y0, w, h, None)
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                self.fix.pop((x, y), None)

    def line(self, x0, y0, x1, y1, c, w=1.0):
        for x, y in self._each():
            if seg_dist(x + .5, y + .5, x0, y0, x1, y1) <= w / 2:
                self._put(x, y, c)

    def px(self, x, y, c, tone):
        """Pixel de detalhe com tom fixo (0 escuro .. 3 claro); c=None é contorno."""
        if 0 <= x < self.w and 0 <= y < self.h:
            self.m[y][x] = c or 'ink'
            self.fix[(x, y)] = INK if c is None else PAL[c][tone]

    def hline(self, x0, x1, y, c, tone):
        for x in range(x0, x1):
            self.px(x, y, c, tone)

    def vline(self, x, y0, y1, c, tone):
        for y in range(y0, y1):
            self.px(x, y, c, tone)

    def render(self, outline=True):
        w, h = self.w, self.h
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        filled = lambda x, y: 0 <= x < w and 0 <= y < h and self.m[y][x] is not None
        same = lambda x, y, c: 0 <= x < w and 0 <= y < h and self.m[y][x] == c
        for x, y in self._each():
            c = self.m[y][x]
            if c is None:
                if outline and any(filled(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    img.putpixel((x, y), INK + (255,))
                continue
            if (x, y) in self.fix:
                img.putpixel((x, y), self.fix[(x, y)] + (255,))
                continue
            if c == 'ink':
                img.putpixel((x, y), INK + (255,))
                continue
            tones = PAL[c]
            t = 2
            if not same(x, y - 1, c) or not same(x - 1, y, c):
                t = 3
            if not same(x, y + 1, c) or not same(x + 1, y, c):
                t = 1
            if not same(x, y + 1, c) and not same(x + 1, y, c):
                t = 0 if c != 'void' else 1
            img.putpixel((x, y), tones[t] + (255,))
        return img


def inside(px, py, pts):
    n, ok = len(pts), False
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        if (y0 > py) != (y1 > py) and px < (x1 - x0) * (py - y0) / (y1 - y0) + x0:
            ok = not ok
    return ok


def seg_dist(px, py, x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    t = max(0, min(1, ((px - x0) * dx + (py - y0) * dy) / (dx * dx + dy * dy or 1)))
    return math.hypot(px - x0 - t * dx, py - y0 - t * dy)


def rot(pts, a, cx=16, cy=16):
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def pack(frames, width):
    """frames: [(nome, Image, (ax, ay))] -> (atlas, rects no formato do jogo).

    Empacota em linhas da esquerda para a direita; rect = [x, y, w, h, ax, ay].
    """
    x = y = row_h = 0
    places = []
    for name, img, anchor in frames:
        if x + img.width > width:
            x, y, row_h = 0, y + row_h, 0
        places.append((name, img, anchor, x, y))
        x += img.width
        row_h = max(row_h, img.height)
    atlas = Image.new('RGBA', (width, y + row_h), (0, 0, 0, 0))
    rects = {}
    for name, img, (ax, ay), px_, py_ in places:
        atlas.alpha_composite(img, (px_, py_))
        rects[name] = [px_, py_, img.width, img.height, ax, ay]
    return atlas, rects
