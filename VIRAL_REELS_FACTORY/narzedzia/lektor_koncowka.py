#!/usr/bin/env python3
"""
Lektor tylko na ostatniej planszy (decyzja Michała 6.11): Piper (offline, głos mc_speech) czyta 1 zdanie od wejścia
outro; podkład jest przyciszany pod głos, całość −14 LUFS; robi też wersję TikTok 1080.

  python3 lektor_koncowka.py <rolka_muzyka.mp4> <rolka_zdarzenia.json> "Tekst lektora." <out_ig.mp4> <out_tt.mp4>

Liczby pisz słownie („tysiąc osiemset osiemdziesiąt pięć”) – Piper czyta cyfry niepewnie.
"""
import json
import os
import subprocess
import sys
import tempfile

SK = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".claude", "skills")
sys.path.insert(0, os.path.join(SK, "szkola-klamala-animacje", "scripts"))
sys.path.insert(0, os.path.join(SK, "szkola-klamala-montaz", "scripts"))
import lektor  # noqa: E402
import montaz  # noqa: E402
from muzyka import tiktok_1080  # noqa: E402


def main():
    src, zdj, tekst, out_ig, out_tt = sys.argv[1:6]
    zd = json.load(open(zdj, encoding="utf-8"))
    pl = zd["plansze"]
    logo = 1 if zd.get("logo") else 0
    start = sum(pl[:len(pl) - 1 - logo]) + 0.35  # wejście planszy outro + chwila na pojawienie się napisu
    tmp = tempfile.mkdtemp()
    surowy, glos = os.path.join(tmp, "g.wav"), os.path.join(tmp, "g_fx.wav")
    dur = lektor.tts(tekst, lektor.voice_model("mc_speech"), surowy, 0.95)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", surowy, "-af", lektor.VOICE_FX + ",apad=pad_dur=0.3", glos], check=True)
    ms = int(start * 1000)
    fc = (f"[1:a]adelay={ms}|{ms},volume=1.6[g];[g]asplit=2[gm][sc];"
          "[0:a][sc]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=350[m];"
          "[m][gm]amix=inputs=2:normalize=0:duration=first[a]")
    mix = os.path.join(tmp, "mix.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", glos, "-filter_complex", fc,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", mix], check=True)
    montaz.glosnosc(mix, out_ig)
    tiktok_1080(out_ig, out_tt)
    koniec = start + dur
    print(f"lektor: start {start:.2f} s, długość {dur:.2f} s, koniec {koniec:.2f} s (rolka {zd['dlugosc']:.2f} s)")
    if koniec > zd["dlugosc"]:
        print("UWAGA: głos dłuższy niż rolka – skróć tekst")


if __name__ == "__main__":
    main()
