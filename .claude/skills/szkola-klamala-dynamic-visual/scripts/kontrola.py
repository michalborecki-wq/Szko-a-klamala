#!/usr/bin/env python3
"""
Kontrola jakości ruchu rolki „Szkoła kłamała” (Dynamic Visual Engine).

  python3 kontrola.py <rolka.mp4> [--zdarzenia <rolka_zdarzenia.json>] [--przed <stara_rolka.mp4>] [--out katalog]

Tworzy w katalogu --out (domyślnie obok filmu):
  <id>_2s.jpg          – pierwsze 2 s: klatki 0 / 0,15 / 0,3 / 0,5 / 0,8 / 1,2 / 2,0 s (haczyk ma być czytelny w KAŻDEJ)
  <id>_przejscia.jpg   – po 2 klatki przed i po każdym cięciu + klatki „drugiego akcentu” (z pliku zdarzeń)
  <id>_przed_po.jpg    – (z --przed) te same chwile starej i nowej wersji jeden pod drugim
Obrazy ogląda się narzędziem Read. Skrypt niczego nie ocenia sam – ocena należy do człowieka/agenta.
"""
import argparse
import io
import json
import os
import subprocess

from PIL import Image, ImageDraw

T2S = [0.0, 0.15, 0.3, 0.5, 0.8, 1.2, 2.0]


def klatka(mp4, t, w=180, h=320):
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t):.2f}", "-i", mp4, "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "mjpeg", "-"], capture_output=True).stdout
    if not b:
        return Image.new("RGB", (w, h), (40, 0, 0))
    return Image.open(io.BytesIO(b)).convert("RGB").resize((w, h))


def arkusz(rzedy, czasy, path, w=180, h=320):
    """rzedy: [(etykieta, mp4)], czasy: lista sekund – siatka z podpisami czasu."""
    lw = 80 if len(rzedy) > 1 else 0
    sh = Image.new("RGB", (lw + w * len(czasy), 22 + h * len(rzedy)), (16, 16, 16))
    d = ImageDraw.Draw(sh)
    for j, t in enumerate(czasy):
        d.text((lw + j * w + 6, 4), f"{t:.2f}s", fill=(255, 199, 39))
    for i, (lab, mp4) in enumerate(rzedy):
        if lw:
            d.text((6, 22 + i * h + h // 2), lab, fill=(255, 255, 255))
        for j, t in enumerate(czasy):
            sh.paste(klatka(mp4, t, w, h), (lw + j * w, 22 + i * h))
    sh.save(path, quality=88)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("--zdarzenia")
    ap.add_argument("--przed")
    ap.add_argument("--out")
    a = ap.parse_args()
    base = os.path.splitext(os.path.basename(a.mp4))[0]
    out = a.out or os.path.dirname(os.path.abspath(a.mp4))
    os.makedirs(out, exist_ok=True)
    print(arkusz([("PO", a.mp4)], T2S, os.path.join(out, f"{base}_2s.jpg")))
    zdj = a.zdarzenia or os.path.join(os.path.dirname(a.mp4), base.replace("_muzyka", "") + "_zdarzenia.json")
    if os.path.exists(zdj):
        z = json.load(open(zdj, encoding="utf-8"))
        cuts = [e["t"] for e in z["zdarzenia"] if e["typ"] == "przejscie"]
        ts = sorted({round(x, 2) for c in cuts for x in (c - .12, c + .12)} |
                    {round(e["t"] + .1, 2) for e in z["zdarzenia"] if e["typ"] == "tik"})
        if ts:
            # po 8 klatek w rzędzie
            rz = [ts[i:i + 8] for i in range(0, len(ts), 8)]
            ims = [Image.open(arkusz([("", a.mp4)], r, os.path.join(out, f"_tmp{i}.jpg"))) for i, r in enumerate(rz)]
            W = max(im.width for im in ims)
            sh = Image.new("RGB", (W, sum(im.height for im in ims)), (16, 16, 16))
            y = 0
            for i, im in enumerate(ims):
                sh.paste(im, (0, y)); y += im.height
                os.remove(os.path.join(out, f"_tmp{i}.jpg"))
            p = os.path.join(out, f"{base}_przejscia.jpg"); sh.save(p, quality=88); print(p)
    if a.przed:
        czasy = T2S[:4] + [2.0, 5.0, 9.0, 15.0]
        print(arkusz([("PRZED", a.przed), ("PO", a.mp4)], czasy, os.path.join(out, f"{base}_przed_po.jpg"), 150, 267))


if __name__ == "__main__":
    main()
