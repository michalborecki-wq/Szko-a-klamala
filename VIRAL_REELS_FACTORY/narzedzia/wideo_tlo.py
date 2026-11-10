#!/usr/bin/env python3
"""
Film (np. klip Higgsfield z zrodla/ai_higgsfield/) → tło rolki dla silnika (pole "tlo3d" w poście).

  python3 VIRAL_REELS_FACTORY/narzedzia/wideo_tlo.py zrodla/ai_higgsfield/2026-11-10/wideo/lupa.mp4 [--sek 45] [--jasnosc -0.12]

Tworzy VIRAL_REELS_FACTORY/VIDEOS/tla/<nazwa>/0000.jpg… (1080×1920, 30 kl./s): klip zapętlony „w przód i w tył”
(bez skoku na końcu pętli), lekko przyciemniony, żeby tekst marki był czytelny. W specu posta:

  "tlo3d": {"klatki": "VIRAL_REELS_FACTORY/VIDEOS/tla/<nazwa>", "fps": 30, "krycie": 0.55},
  "etykieta_ai": true

Ilustracja AI zawsze z etykietą „Ilustracja AI – nie jest zdjęciem wydarzenia” (CLAUDE.md) – daje ją "etykieta_ai".
Katalog klatek jest w .gitignore (VIDEOS) – przed renderem w nowej sesji uruchom ten skrypt ponownie.
"""
import argparse
import os
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("--sek", type=float, default=45, help="długość tła (s) – co najmniej długość rolki")
    ap.add_argument("--jasnosc", type=float, default=-0.12, help="eq brightness (ujemna = ciemniej)")
    ap.add_argument("--nazwa")
    a = ap.parse_args()
    nazwa = a.nazwa or os.path.splitext(os.path.basename(a.mp4))[0]
    out = os.path.join(ROOT, "VIRAL_REELS_FACTORY", "VIDEOS", "tla", nazwa)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    tmp = os.path.join(out, "_pingpong.mp4")
    # przód + tył (płynna pętla), skala do 9:16 1080×1920, 30 kl./s, przyciemnienie
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.mp4, "-filter_complex",
                    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,split[a][b];"
                    "[b]reverse[r];[a][r]concat=n=2:v=1:a=0," f"eq=brightness={a.jasnosc}:saturation=1.05[v]",
                    "-map", "[v]", "-an", tmp], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-i", tmp, "-t", str(a.sek),
                    "-q:v", "3", os.path.join(out, "%04d.jpg")], check=True)
    os.remove(tmp)
    n = len([f for f in os.listdir(out) if f.endswith(".jpg")])
    print(f"{out} – {n} klatek ({n / 30:.1f} s)")


if __name__ == "__main__":
    main()
