#!/usr/bin/env python3
"""Buduje zasoby marki „Kranówka Poznańska”: logo (SVG + JS) i wzór kaustyk (PNG).

Uruchomienie:  python3 narzedzia/build_assets.py
Wymaga: fonttools, brotli, numpy, scipy, pillow.
"""
import math
import json
import pathlib

import numpy as np
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
IMG = ROOT / "assets" / "img"
JS = ROOT / "assets" / "js"

ATRAMENT = "#0B1B3F"
WODA = "#2EA8FF"


# ---------------------------------------------------------------- glify
def load(paths, axes):
    fonts = []
    for p in paths:
        f = TTFont(FONTS / p)
        fonts.append(instantiateVariableFont(f, axes))
    return fonts


def glyph(fonts, ch, scale, dx, dy):
    """Zwraca (ścieżka SVG, szerokość) znaku w układzie SVG (y w dół)."""
    for f in fonts:
        cmap = f.getBestCmap()
        if ord(ch) in cmap:
            name = cmap[ord(ch)]
            gs = f.getGlyphSet()
            pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}")
            gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, dx, dy)))
            return pen.getCommands(), gs[name].width * scale
    raise KeyError(ch)


# ---------------------------------------------------------------- odcisk
def ring_path(cx, cy, r, t, seed=7, n=180):
    """Mokre kółko po szklance: nieregularny pierścień o zmiennej grubości."""
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 2 * math.pi, 6)

    def wob(a, amp, k0=0):
        return amp * (0.55 * math.sin(2 * a + ph[k0]) + 0.3 * math.sin(3 * a + ph[k0 + 1])
                      + 0.15 * math.sin(5 * a + ph[k0 + 2]))

    outer, inner = [], []
    for i in range(n):
        a = 2 * math.pi * i / n
        # grubsza u dołu po lewej – tam, gdzie „zebrała się” woda
        thick = t * (1 + 0.30 * math.cos(a - 2.35) + 0.05 * math.sin(3 * a + ph[5]))
        ro = r + wob(a, r * 0.006)
        ri = ro - thick + wob(a, r * 0.007, 3)
        outer.append((cx + ro * math.cos(a), cy + ro * math.sin(a)))
        inner.append((cx + ri * math.cos(a), cy + ri * math.sin(a)))

    def poly(pts):
        return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"

    return poly(outer) + poly(inner[::-1])


def drop_path(cx, cy, s, rot_deg):
    """Kropla – zastępuje kreskę nad Ó. Czubek do góry przed obrotem."""
    pts = []
    n = 96
    for i in range(n):
        a = 2 * math.pi * i / n
        x = 0.66 * math.sin(a) * math.sin(a / 2) ** 2
        y = -math.cos(a) * 0.75
        pts.append((x * s, y * s))
    rot = math.radians(rot_deg)
    out = []
    for x, y in pts:
        out.append((cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot)))
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in out) + "Z"


def build_logo():
    fr = load(["fraunces-latin-full-normal.woff2"], {"opsz": 144, "wght": 900, "SOFT": 100, "WONK": 0})
    ins = load(["instrument-sans-latin-wght-normal.woff2", "instrument-sans-latin-ext-wght-normal.woff2"],
               {"wght": 600})

    CAP = 400.0                       # wysokość wersalika w jednostkach SVG
    sc = CAP / 1400.0
    base = 660.0                      # linia bazowa
    track = -6.0
    kern = {("K", "R"): -4, ("R", "A"): -22, ("A", "N"): -10, ("N", "O"): 6, ("O", "W"): -4,
            ("W", "K"): -8, ("K", "A"): -30}

    x = 40.0
    parts = []
    prev = None
    ring_r = CAP * 0.535
    ring_t = CAP * 0.155
    ring_box = None
    for ch in "KRANOWKA":
        if prev:
            x += track + kern.get((prev, ch), 0)
        if ch == "O":
            cx, cy = x + ring_r, base - CAP / 2
            d = ring_path(cx, cy, ring_r, ring_t)
            parts.append(("o", "kp-ring", d))
            # kropla = kreska nad Ó
            dd = drop_path(cx + ring_r * 0.22, base - CAP * 1.31, CAP * 0.27, 24)
            parts.append(("drop", "kp-drop", dd))
            ring_box = (cx, cy, ring_r)
            x += ring_r * 2
        else:
            d, w = glyph(fr, ch, sc, x, base)
            parts.append((ch, "kp-l", d))
            x += w
        prev = ch
    width = x + 40.0

    # POZNAŃSKA – wersaliki, szeroko, wyjustowane do szerokości napisu
    sub = "POZNAŃSKA"
    s2 = 104.0 / 720.0
    widths = [glyph(ins, c, s2, 0, 0)[1] for c in sub]
    inner_w = width - 80.0 - 8.0
    gap = (inner_w - sum(widths)) / (len(sub) - 1)
    sx = 44.0
    sub_parts = []
    for c, w in zip(sub, widths):
        d, _ = glyph(ins, c, s2, sx, base + 190)
        sub_parts.append(d)
        sx += w + gap
    height = base + 190 + 50

    def svg(fill, accent, with_sub=True, cls=True):
        g = []
        for i, (ch, c, d) in enumerate(parts):
            col = accent if c in ("kp-ring", "kp-drop") else fill
            attr = f' class="{c}" data-i="{i}"' if cls else ""
            rule = ' fill-rule="evenodd"' if c == "kp-ring" else ""
            g.append(f'<path{attr} fill="{col}"{rule} d="{d}"/>')
        if with_sub:
            attr = ' class="kp-sub"' if cls else ""
            g.append(f'<g{attr} fill="{fill}">' + "".join(f'<path d="{d}"/>' for d in sub_parts) + "</g>")
        h = height if with_sub else base + 40
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {h:.0f}" '
                f'role="img" aria-label="Kranówka Poznańska">' + "".join(g) + "</svg>")

    variants = {
        "logo-atrament": svg(ATRAMENT, WODA, cls=False),
        "logo-papier": svg("#F5F3EE", WODA, cls=False),
        "logo-mono-atrament": svg(ATRAMENT, ATRAMENT, cls=False),
        "logo-mono-papier": svg("#F5F3EE", "#F5F3EE", cls=False),
    }
    for name, s in variants.items():
        (IMG / f"{name}.svg").write_text(s, encoding="utf-8")

    # sam znak (odcisk + kropla)
    cx, cy, r = ring_box
    pad = r * 0.55
    vb = f"{cx - r - pad:.0f} {cy - r - pad * 2.4:.0f} {2 * (r + pad):.0f} {2 * r + pad * 3.4:.0f}"
    for name, col in (("znak-woda", WODA), ("znak-atrament", ATRAMENT), ("znak-papier", "#F5F3EE")):
        mark = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Kranówka Poznańska – znak">'
                + "".join(f'<path fill="{col}" fill-rule="evenodd" d="{d}"/>' for _, c, d in parts
                          if c in ("kp-ring", "kp-drop")) + "</svg>")
        (IMG / f"{name}.svg").write_text(mark, encoding="utf-8")

    data = {
        "logo": svg("currentColor", "var(--kp-akcent, #2EA8FF)"),
        "wordmark": svg("currentColor", "var(--kp-akcent, #2EA8FF)", with_sub=False),
        "ring": ring_path(0, 0, 100, 29),
        "ring2": ring_path(0, 0, 100, 22, seed=21),
        "drop": drop_path(0, 0, 100, 0),
        "ringBox": {"cx": cx, "cy": cy, "r": r, "w": width, "h": height},
    }
    (JS / "logo.js").write_text("window.KP_LOGO = " + json.dumps(data) + ";\n", encoding="utf-8")
    print("logo ok", round(width), round(height))


# ---------------------------------------------------------------- kaustyki
def caustic(size=1536, seed=3, cells=11, lw=0.030):
    """Kafel bez szwów: siatka światła jak na dnie szklanki z wodą."""
    rng = np.random.default_rng(seed)
    n = cells * cells
    gx, gy = np.meshgrid(np.arange(cells), np.arange(cells))
    pts = np.stack([gx.ravel(), gy.ravel()], 1).astype(float) + rng.uniform(0.08, 0.92, (n, 2))
    pts /= cells
    tiles = np.concatenate([pts + np.array([dx, dy]) for dx in (-1, 0, 1) for dy in (-1, 0, 1)])
    tree = cKDTree(tiles)

    u = (np.arange(size) + 0.5) / size
    X, Y = np.meshgrid(u, u)
    tau = 2 * math.pi
    # zniekształcenie domeny – okresowe, żeby kafel się zamykał
    wx = 0.030 * np.sin(tau * (2 * Y + 0.3)) + 0.016 * np.sin(tau * (3 * X + 5 * Y) + 1.1) + 0.010 * np.sin(tau * 7 * Y + 2)
    wy = 0.030 * np.sin(tau * (2 * X + 0.7)) + 0.016 * np.sin(tau * (5 * X - 3 * Y) + 0.4) + 0.010 * np.sin(tau * 6 * X + 4)
    q = np.stack([(X + wx) % 1.0, (Y + wy) % 1.0], -1).reshape(-1, 2)
    d, _ = tree.query(q, k=3)
    edge = (d[:, 1] - d[:, 0]).reshape(size, size) * cells      # 0 na krawędzi komórki
    node = (d[:, 2] - d[:, 0]).reshape(size, size) * cells      # 0 w węźle

    # zmienna grubość linii (światło „zbiera się” nierówno)
    mod = 0.75 + 0.45 * np.sin(tau * (X * 2 + Y) + 1.7) * np.sin(tau * (Y * 3 - X) + 0.2)
    w = lw * cells / 11 * (0.7 + 0.6 * mod)
    line = np.exp(-(edge / w) ** 2)
    glow = 0.30 * np.exp(-(edge / (w * 3.2)) ** 2)
    knot = 0.55 * np.exp(-(node / (w * 3.0)) ** 2)
    a = np.clip(line + glow + knot, 0, 1)
    a = gaussian_filter(a, 0.8, mode="wrap")
    return a


def save_tile(a, path, hexcol):
    h, w = a.shape
    rgb = tuple(int(hexcol[i:i + 2], 16) for i in (1, 3, 5))
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., :3] = rgb
    rgba[..., 3] = (np.clip(a, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(path, optimize=True)


def build_caustics():
    a = caustic(size=1280, seed=3, cells=11, lw=0.030)
    b = caustic(size=1024, seed=11, cells=7, lw=0.024)
    hard = gaussian_filter(np.clip((a - 0.42) * 6, 0, 1), 0.6, mode="wrap")
    save_tile(a, IMG / "kaustyka-a-woda.png", WODA)
    save_tile(a, IMG / "kaustyka-a-papier.png", "#FFFFFF")
    save_tile(b, IMG / "kaustyka-b-woda.png", WODA)
    save_tile(b, IMG / "kaustyka-b-papier.png", "#FFFFFF")
    save_tile(hard, IMG / "kaustyka-druk-atrament.png", ATRAMENT)
    save_tile(hard, IMG / "kaustyka-druk-woda.png", WODA)
    save_tile(hard, IMG / "kaustyka-druk-papier.png", "#F5F3EE")
    print("kaustyki ok")


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    build_logo()
    build_caustics()
