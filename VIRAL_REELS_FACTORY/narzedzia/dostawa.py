#!/usr/bin/env python3
"""
Dostawa dla Michała (decyzja 5.11): 3 razy dziennie – 9:00 rolka, 13:00 post TikTok (karuzela 9:16), 18:00 rolka.
Bez wariantów B, bez wersji z lektorem, bez paczek zbiorczych – żeby nie było bałaganu.

  python3 dostawa.py <spec.json> <post_id> --opis opis.md [--reklama "<marka>"] [--pora 0900|1300|1800] [--data RRRR-MM-DD]

Post z "format": "vertical" (karuzela 9:16, zwykle 13:00) → DOSTAWA/<data>_<pora>/<TEMAT>_TIKTOK_01..NN.jpg + _opis.md.
Rolka ("format": "reel"):

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
    ap.add_argument("--pora", default="0900" if teraz.hour < 10 else "1300" if teraz.hour < 14 else "1800")
    ap.add_argument("--data", default=teraz.date().isoformat())
    ap.add_argument("--reklama", default="", help="marka produktu z koszyka TikTok Shop – na pliku TikTok pojawi się "
                    "etykieta „Reklama – <marka>” (UOKiK); IG zostaje bez niej")
    ap.add_argument("--suplement", action="store_true", help="produkt w koszyku to suplement diety – dodaje na pliku "
                    "TikTok ostrzeżenie „Suplement diety jest żywnością, a nie lekiem. Nie leczy chorób.” przez całą rolkę")
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
    temat = pid.upper()
    out = os.path.join(ROOT, "DOSTAWA", f"{a.data}_{a.pora}")

    if posty[0].get("format") == "vertical":  # karuzela zdjęć 9:16 na TikTok (post 13:00)
        run([sys.executable, RENDER, one, "--out", work, "--sheet"])
        import glob
        jpgi = sorted(glob.glob(os.path.join(work, f"{pid}_916_*.jpg")) or glob.glob(os.path.join(work, f"{pid}_[0-9][0-9].jpg")))
        if not jpgi:
            raise SystemExit("Render nie dał slajdów 9:16")
        if os.path.isdir(out):
            shutil.rmtree(out)
        os.makedirs(out)
        wynik = []
        for i, f in enumerate(jpgi, 1):
            dst = os.path.join(out, f"{temat}_TIKTOK_{i:02d}.jpg")
            shutil.copy2(f, dst)
            wynik.append(dst)
        dst = os.path.join(out, f"{temat}_opis.md")
        shutil.copy2(a.opis, dst)
        wynik.append(dst)
        print("Podgląd do kontroli:", " ".join(glob.glob(os.path.join(work, "_podglad_*.jpg"))))
        print(f"DOSTAWA – wyślij te {len(wynik)} pliki:")
        for w in wynik:
            print(w)
        return

    run([sys.executable, RENDER, one, "--out", work, "--video", "--muzyka"])

    ig, tt = os.path.join(work, f"{pid}_muzyka.mp4"), os.path.join(work, f"{pid}_tiktok_1080.mp4")
    for f in (ig, tt):
        if not os.path.exists(f):
            raise SystemExit(f"Render nie dał pliku {f}")
    okl = os.path.join(work, f"{pid}_okladka.jpg")
    run(["ffmpeg", "-v", "error", "-y", "-ss", "2.6", "-i", ig, "-frames:v", "1", "-q:v", "2", okl])

    if a.suplement and not a.reklama:
        raise SystemExit("--suplement wymaga --reklama \"<marka>\"")
    if a.reklama:  # koszyk TikTok Shop: oznaczenie na filmie tylko w wersji TikTok
        txt = os.path.join(work, "reklama.txt")
        open(txt, "w", encoding="utf-8").write(f"Reklama – {a.reklama}")
        font = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
        ost = os.path.join(work, "suplement.txt")
        open(ost, "w", encoding="utf-8").write("Suplement diety jest żywnością, a nie lekiem.\nNie leczy chorób.")
        tt_rek = os.path.join(work, f"{pid}_tiktok_1080_reklama.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-i", tt, "-vf",
             f"drawtext=fontfile={font}:textfile={txt}:fontsize=34:fontcolor=0x0A0E18:box=1:boxcolor=0xFFC727:"
             "boxborderw=14:x=60:y=262" + (
                 f",drawtext=fontfile={font}:textfile={ost}:fontsize=30:fontcolor=white:box=1:boxcolor=0xE53935:"
                 "boxborderw=12:x=60:y=330:line_spacing=6" if a.suplement else ""), "-c:v", "libx264", "-profile:v", "high", "-level", "4.1",
             "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "copy", "-movflags", "+faststart", tt_rek])
        tt = tt_rek

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
