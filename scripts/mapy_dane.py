#!/usr/bin/env python3
"""
Dane do planszy „mapa” (DVE 9.11) z Natural Earth (domena publiczna, naturalearthdata.com).
  python3 scripts/mapy_dane.py --adm1 ne_10m_admin_1_states_provinces.geojson --adm0 ne_50m_admin_0_countries.geojson
Pliki źródłowe: https://github.com/nvkelso/natural-earth-vector/tree/master/geojson
Wynik (uproszczony, współrzędne lon/lat z dokładnością 0,001°):
  zrodla/mapy/polska_wojewodztwa.json – 16 województw (nazwy polskie)
  zrodla/mapy/swiat_panstwa.json      – państwa świata (ISO A2, nazwa polska z NAME_PL)
"""
import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WOJ = {"Silesian": "śląskie", "Lesser Poland": "małopolskie", "Subcarpathian": "podkarpackie", "Lower Silesian": "dolnośląskie",
       "Opole": "opolskie", "Podlachian": "podlaskie", "Warmian-Masurian": "warmińsko-mazurskie", "Lubusz": "lubuskie",
       "West Pomeranian": "zachodniopomorskie", "Lublin": "lubelskie", "Pomeranian": "pomorskie", "Masovian": "mazowieckie",
       "Łódź": "łódzkie", "Kuyavian-Pomeranian": "kujawsko-pomorskie", "Greater Poland": "wielkopolskie", "Świętokrzyskie": "świętokrzyskie"}


def dp(pts, eps):
    """Douglas–Peucker."""
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    n = (dx * dx + dy * dy) ** .5 or 1e-12
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / n
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return dp(pts[:idx + 1], eps)[:-1] + dp(pts[idx:], eps)
    return [pts[0], pts[-1]]


def upr(geom, eps, min_pkt=4):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    out = []
    for poly in polys:
        r = [(round(x, 4), round(y, 4)) for x, y in poly[0]]
        # pierścień zamknięty (pierwszy = ostatni punkt): dzielę go w punkcie najdalszym od początku i upraszczam obie połowy
        k = max(range(len(r)), key=lambda i: (r[i][0] - r[0][0]) ** 2 + (r[i][1] - r[0][1]) ** 2)
        ring = dp(r[:k + 1], eps)[:-1] + dp(r[k:], eps)
        if len(ring) >= min_pkt:
            out.append([[round(x, 3), round(y, 3)] for x, y in ring])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adm1", required=True)
    ap.add_argument("--adm0", required=True)
    a = ap.parse_args()
    meta = {"zrodlo": "Natural Earth (naturalearthdata.com), domena publiczna", "uproszczenie": "Douglas–Peucker"}
    d = json.load(open(a.adm1, encoding="utf-8"))
    woj = {WOJ[f["properties"]["name"]]: upr(f["geometry"], .012) for f in d["features"] if f["properties"].get("iso_a2") == "PL"}
    json.dump({**meta, "skala": "1:10m", "obszary": woj}, open(REPO / "zrodla/mapy/polska_wojewodztwa.json", "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    d = json.load(open(a.adm0, encoding="utf-8"))
    sw = {}
    for f in d["features"]:
        p = f["properties"]
        kod = p.get("ISO_A2_EH") if p.get("ISO_A2") in (None, "-99") else p.get("ISO_A2")
        if not kod or kod == "-99":
            continue
        sw[kod] = {"nazwa": p.get("NAME_PL") or p.get("NAME"), "obszary": upr(f["geometry"], .08)}
    json.dump({**meta, "skala": "1:50m", "panstwa": sw}, open(REPO / "zrodla/mapy/swiat_panstwa.json", "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    for n in ("polska_wojewodztwa.json", "swiat_panstwa.json"):
        print(REPO / "zrodla/mapy" / n, (REPO / "zrodla/mapy" / n).stat().st_size)


if __name__ == "__main__":
    main()
