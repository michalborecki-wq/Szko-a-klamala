#!/usr/bin/env python3
"""
Produkcja rolki fabryki „Szkoła kłamała”: z SCRIPTS/<rid>/spec.json do gotowej paczki w READY_TO_PUBLISH/<rid>/.

Kroki:
  1. wersje bez lektora (A, _wariantB) → render.py --video --muzyka (4K, podkład, efekty, logo, TikTok 1080)
  2. wersja z polem "lektor" (_lektor) → lektor.py (Piper, offline) + podkład z muzyka.py ściszony pod głos
     → <id>_lektor_muzyka.mp4 (−14 LUFS) + TikTok 1080 + napisy SRT
  3. okładki (klatka 2,6 s) dla każdej wersji
  4. paczka: READY_TO_PUBLISH/<rid>/ – pliki do publikacji, opis.md, zrodla.md, scenariusz.md, LISTA.md

Render jednej wersji 4K trwa ok. 10–15 min – uruchamiaj w tle. Każdy krok można powtórzyć (--tylko).
Użycie: python3 produkcja.py <rid> [--tylko render|lektor|paczka] [--hd]
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
SK = os.path.join(REPO, ".claude", "skills")
RENDER = os.path.join(SK, "szkola-klamala-grafiki", "scripts", "render.py")
LEKTOR = os.path.join(SK, "szkola-klamala-animacje", "scripts", "lektor.py")
MUZYKA = os.path.join(SK, "szkola-klamala-animacje", "scripts", "muzyka.py")
sys.path.insert(0, os.path.join(SK, "szkola-klamala-montaz", "scripts"))
sys.path.insert(0, os.path.join(SK, "szkola-klamala-animacje", "scripts"))


def run(cmd):
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def okladka(mp4, jpg):
    run(["ffmpeg", "-v", "error", "-y", "-ss", "2.6", "-i", mp4, "-frames:v", "1", "-q:v", "2", jpg])


def render_bez_lektora(spec, vid, hd):
    posty = [p for p in spec["posts"] if not any(s.get("lektor") for s in p["slides"])]
    if not posty:
        return
    tmp = os.path.join(vid, "spec_bez_lektora.json")
    json.dump(dict(spec, posts=posty), open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    run([sys.executable, RENDER, tmp, "--out", vid, "--video", "--muzyka"] + (["--hd"] if hd else []))


def render_lektor(spec, vid, rid):
    posty = [p for p in spec["posts"] if any(s.get("lektor") for s in p["slides"])]
    if not posty:
        return
    import montaz
    from muzyka import tiktok_1080
    lk = os.path.join(vid, "lektor")
    os.makedirs(lk, exist_ok=True)
    tmp = os.path.join(lk, "spec_lektor.json")
    json.dump(dict(spec, posts=posty), open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    run([sys.executable, LEKTOR, tmp, "--out", lk])
    for p in posty:
        pid = p["id"]
        cichy, glos = os.path.join(lk, f"{pid}.mp4"), os.path.join(lk, f"{pid}_lektor.mp4")
        run([sys.executable, MUZYKA, cichy, "--nastroj", p.get("muzyka", {}).get("nastroj", "spokojny")])
        podklad = os.path.join(lk, f"{pid}_muzyka.mp4")
        mix = os.path.join(lk, f"{pid}_lektor_mix.mp4")
        # głos na wierzchu, podkład ściszony o ok. 14 dB i dodatkowo przyciszany, gdy mówi lektor
        fc = ("[1:a]volume=0.2[m];[0:a]asplit=2[g][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md];"
              "[g][md]amix=inputs=2:normalize=0:duration=longest[a]")
        run(["ffmpeg", "-y", "-v", "error", "-i", glos, "-i", podklad, "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", mix])
        final = os.path.join(vid, f"{pid}_lektor_muzyka.mp4")
        montaz.glosnosc(mix, final)
        tiktok_1080(final, os.path.join(vid, f"{pid}_lektor_tiktok_1080.mp4"))
        srt = os.path.join(lk, f"{pid}_lektor.srt")
        if os.path.exists(srt):
            sub = os.path.join(ROOT, "SUBTITLES", rid)
            os.makedirs(sub, exist_ok=True)
            shutil.copy(srt, sub)
        voc = os.path.join(ROOT, "VOICEOVER", rid)
        os.makedirs(voc, exist_ok=True)
        for w in glob.glob(os.path.join(lk, "_lektor", f"{pid}_*.wav")):
            shutil.copy(w, voc)
        montaz.kontrola(final)


def paczka(spec, vid, rid):
    dst = os.path.join(ROOT, "READY_TO_PUBLISH", rid)
    os.makedirs(dst, exist_ok=True)
    lista = [f"# Paczka do publikacji – {rid}\n", "| Plik | Gdzie | Uwagi |", "|---|---|---|"]
    for p in spec["posts"]:
        pid = p["id"]
        wersja = "B (Rolka próbna)" if pid.endswith("_wariantB") else ("z lektorem (test)" if pid.endswith("_lektor") else "A")
        if pid.endswith("_lektor"):
            ig, tt = os.path.join(vid, f"{pid}_lektor_muzyka.mp4"), os.path.join(vid, f"{pid}_lektor_tiktok_1080.mp4")
        else:
            ig, tt = os.path.join(vid, f"{pid}_muzyka.mp4"), os.path.join(vid, f"{pid}_tiktok_1080.mp4")
        tag = pid.upper()
        for src, nazwa, gdzie in ((ig, f"{tag}_INSTAGRAM.mp4", "Instagram (4K)"), (tt, f"{tag}_TIKTOK_1080.mp4", "TikTok")):
            if os.path.exists(src):
                shutil.copy(src, os.path.join(dst, nazwa))
                lista.append(f"| {nazwa} | {gdzie} | wersja {wersja} |")
        if os.path.exists(ig):
            okladka(ig, os.path.join(dst, f"{tag}_okladka.jpg"))
            lista.append(f"| {tag}_okladka.jpg | okładka IG (ustaw ręcznie) | wersja {wersja} |")
    for f in ("opis.md", "zrodla.md", "scenariusz.md"):
        s = os.path.join(ROOT, "SCRIPTS", rid, f)
        if os.path.exists(s):
            shutil.copy(s, dst)
    lista += ["", "Publikacja: B jako Rolka próbna → 15 min później A → TikTok 1–2 h po IG. Okładka ręcznie, "
              "„Udostępnij na Facebooku” włączone, przypięty komentarz z opis.md, odpowiedzi w 1. godzinie.",
              "Po publikacji: `python3 narzedzia/analityka.py opublikowano " + rid + "` (przenosi paczkę do PUBLISHED)."]
    open(os.path.join(dst, "LISTA.md"), "w", encoding="utf-8").write("\n".join(lista) + "\n")
    print("Paczka:", dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rid")
    ap.add_argument("--tylko", choices=["render", "lektor", "paczka"])
    ap.add_argument("--hd", action="store_true", help="podgląd 1080p (nie do publikacji)")
    a = ap.parse_args()
    spec = json.load(open(os.path.join(ROOT, "SCRIPTS", a.rid, "spec.json"), encoding="utf-8"))
    if "…" in json.dumps(spec, ensure_ascii=False):
        raise SystemExit("spec.json ma niewypełnione pola „…” – uzupełnij scenariusz przed produkcją.")
    vid = os.path.join(ROOT, "VIDEOS", a.rid)
    os.makedirs(vid, exist_ok=True)
    if a.tylko in (None, "render"):
        render_bez_lektora(spec, vid, a.hd)
    if a.tylko in (None, "lektor"):
        render_lektor(spec, vid, a.rid)
    if a.tylko in (None, "paczka"):
        paczka(spec, vid, a.rid)


if __name__ == "__main__":
    main()
