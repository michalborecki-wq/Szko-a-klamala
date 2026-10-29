#!/usr/bin/env python3
"""
Arkusz klatek z filmu – do obejrzenia gotowego wideo (narzędzie Read) przed oddaniem.

Użycie:
  python3 klatki.py film.mp4 [--n 10] [--times 0,0.4,2.5] [--out arkusz.jpg] [--w 270]

Domyślnie bierze klatkę 0 i N równo rozłożonych momentów; na każdej klatce wypisuje czas.
"""
import argparse
import json
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    return float(json.loads(out)["format"]["duration"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--times", help="lista sekund rozdzielona przecinkami")
    ap.add_argument("--out")
    ap.add_argument("--w", type=int, default=270)
    a = ap.parse_args()

    d = duration(a.video)
    if a.times:
        ts = [float(x) for x in a.times.split(",")]
    else:
        ts = [0.0] + [d * (k + 1) / (a.n + 1) for k in range(a.n)]
    ts = [min(t, max(0.0, d - 0.05)) for t in ts]

    ims = []
    with tempfile.TemporaryDirectory() as tmp:
        for k, t in enumerate(ts):
            f = os.path.join(tmp, f"{k}.png")
            for back in (0, .1, .2, .4):   # dźwięk bywa dłuższy niż obraz – cofnij się do ostatniej klatki
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, t - back):.3f}", "-i", a.video,
                                "-frames:v", "1", "-vf", f"scale={a.w}:-2", f], check=True)
                if os.path.exists(f):
                    break
            im = Image.open(f).convert("RGB")
            dr = ImageDraw.Draw(im)
            try:
                font = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
            except OSError:
                font = ImageFont.load_default()
            dr.rectangle([0, 0, 74, 26], fill=(0, 0, 0))
            dr.text((6, 3), f"{t:.2f}s", fill=(255, 199, 39), font=font)
            ims.append(im)

    w, h = ims[0].size
    cols = min(len(ims), 6)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * rows), (20, 20, 20))
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % cols) * w, (k // cols) * h))
    out = a.out or os.path.splitext(a.video)[0] + "_klatki.jpg"
    sheet.save(out, quality=88)
    print(out)


if __name__ == "__main__":
    main()
