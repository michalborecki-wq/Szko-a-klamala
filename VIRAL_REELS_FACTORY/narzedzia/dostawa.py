#!/usr/bin/env python3
"""
Dostawa dla Michała (decyzja 4.11): 2 razy dziennie – ok. 9:00 i ok. 17:00 – JEDNA rolka + opis IG i TikTok.
Bez wariantów B, bez wersji z lektorem, bez paczek zbiorczych – żeby nie było bałaganu.

  python3 dostawa.py <spec.json> <post_id> --opis opis.md [--pora 0900|1700] [--data RRRR-MM-DD]

Robi:
  1. wyciąga z <spec.json> jeden post <post_id> i renderuje go (render.py --video --muzyka: 4K, podkład, logo, TikTok 1080),
  2. okładka = klatka z 2,6 s,
  3. DOSTAWA/<data>_<pora>/ – dokładnie 4 pliki:
       <TEMAT>_INSTAGRAM.mp4  (4K, nasz podkład)
       <TEMAT>_TIKTOK.mp4     (1080×1920)
       <TEMAT>_okladka.jpg
       <TEMAT>_opis.md        (IG + TikTok + przypięty komentarz – z pliku --opis)
Na końcu wypisuje ścieżki 4 plików (do SendUserFile).
"""
import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
RENDER = os.path.join(REPO, ".claude", "skills", "szkola-klamala-grafiki", "scripts", "render.py")
TZ = ZoneInfo("Europe/Warsaw")


def run(cmd):
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("post_id")
    ap.add_argument("--opis", required=True, help="plik .md z opisem IG, TikTok i przypiętym komentarzem")
    teraz = dt.datetime.now(TZ)
    ap.add_argument("--pora", default="0900" if teraz.hour < 12 else "1700")
    ap.add_argument("--data", default=teraz.date().isoformat())
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding="utf-8"))
    posty = [p for p in spec["posts"] if p["id"] == a.post_id]
    if not posty:
        raise SystemExit(f"Brak posta {a.post_id} w {a.spec}: {[p['id'] for p in spec['posts']]}")
    tekst = json.dumps(posty[0], ensure_ascii=False)
    if '": "…"' in tekst or "TODO" in tekst:
        raise SystemExit("Spec ma niewypełnione miejsca (… / TODO) – najpierw scenariusz.")
    if not os.path.exists(a.opis):
        raise SystemExit(f"Brak opisu {a.opis}")

    pid = a.post_id
    work = os.path.join(ROOT, "VIDEOS", f"dostawa_{a.data}_{a.pora}")
    os.makedirs(work, exist_ok=True)
    one = os.path.join(work, f"spec_{pid}.json")
    json.dump(dict(spec, posts=posty), open(one, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    run([sys.executable, RENDER, one, "--out", work, "--video", "--muzyka"])

    ig, tt = os.path.join(work, f"{pid}_muzyka.mp4"), os.path.join(work, f"{pid}_tiktok_1080.mp4")
    for f in (ig, tt):
        if not os.path.exists(f):
            raise SystemExit(f"Render nie dał pliku {f}")
    okl = os.path.join(work, f"{pid}_okladka.jpg")
    run(["ffmpeg", "-v", "error", "-y", "-ss", "2.6", "-i", ig, "-frames:v", "1", "-q:v", "2", okl])

    temat = pid.upper()
    out = os.path.join(ROOT, "DOSTAWA", f"{a.data}_{a.pora}")
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    pliki = [(ig, f"{temat}_INSTAGRAM.mp4"), (tt, f"{temat}_TIKTOK.mp4"), (okl, f"{temat}_okladka.jpg"),
             (a.opis, f"{temat}_opis.md")]
    wynik = []
    for src, name in pliki:
        dst = os.path.join(out, name)
        shutil.copy2(src, dst)
        wynik.append(dst)
    print("Arkusz klatek do kontroli:", os.path.join(work, f"{pid}_muzyka_klatki.jpg"))

    print("DOSTAWA – wyślij te 4 pliki:")
    for w in wynik:
        print(w)


if __name__ == "__main__":
    main()
