"""Tekstura wysokości boku opony (napisy wytłoczone w gumie) – uruchamiać zwykłym python3, nie w Blenderze.

Pas biegunowy: szerokość = pełne 360°, wysokość = pas boku od r=0,222 do r=0,272 m (opona 205/55 R16).
Proporcje pikseli zgodne z obwodem przy r≈0,25 m, więc litery nie są rozciągnięte.
Bez nazw producentów – tylko oznaczenia techniczne (rozmiar, M+S, symbol 3PMSF).

  python3 sceny/opona_bok.py ../assets/opona_bok.png
"""
import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 8192, 260
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
img = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(img)
# grzbiety ochronne przy feldze i przy barku
d.rectangle([0, H - 26, W, H - 14], fill=150)
d.rectangle([0, 10, W, 16], fill=110)


def tekst(x, s, rozm, jasn=255):
    f = ImageFont.truetype(FONT, rozm)
    bb = d.textbbox((0, 0), s, font=f)
    w = bb[2] - bb[0]
    d.text((x - w / 2 - bb[0], H / 2 - (bb[3] - bb[1]) / 2 - bb[1]), s, font=f, fill=jasn)
    return w


def gora_snieg(cx, rozm=120):
    """Symbol 3PMSF: trzy szczyty z płatkiem śniegu w środku (kontur wytłoczony)."""
    cy = H / 2 + 8
    pts = [(cx - rozm * .62, cy + rozm * .42), (cx - rozm * .34, cy - rozm * .05), (cx - rozm * .2, cy + rozm * .12),
           (cx, cy - rozm * .46), (cx + rozm * .2, cy + rozm * .05), (cx + rozm * .34, cy - rozm * .12),
           (cx + rozm * .62, cy + rozm * .42)]
    d.line(pts + [pts[0]], fill=255, width=9, joint="curve")
    r = rozm * .17
    sx, sy = cx, cy + rozm * .14
    for k in range(3):
        a = math.pi * k / 3
        d.line([(sx - r * math.cos(a), sy - r * math.sin(a)), (sx + r * math.cos(a), sy + r * math.sin(a))], fill=255, width=6)


for kopia in range(2):              # dwa komplety oznaczeń po przeciwnych stronach koła
    o = kopia * W / 2
    tekst(o + 900, "205/55 R16 91H", 120)
    tekst(o + 1900, "WINTER", 104)
    tekst(o + 2550, "M+S", 104)
    gora_snieg(o + 3000)
    tekst(o + 3500, "TUBELESS  RADIAL", 58, 210)

img = img.filter(ImageFilter.GaussianBlur(2.2))     # zaokrąglone krawędzie wytłoczeń
img.save(sys.argv[1] if len(sys.argv) > 1 else "opona_bok.png")
