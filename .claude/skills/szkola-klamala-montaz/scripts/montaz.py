#!/usr/bin/env python3
"""
Montaż nagrań „Szkoła kłamała” według 8 zasad (SKILL.md):
kopia oryginału → wycięcie pauz i gorszych podejść → pion 1080×1920 → napisy PL słowo w słowo
→ głośność −14 LUFS → kontrola gotowego filmu.

Użycie:
  python3 montaz.py przygotuj nagranie.mov --praca praca/odcinek1
      # kopia oryginału (suma SHA-256), transkrypcja, PROPOZYCJA cięć → praca/.../ciecia.json do przejrzenia
  python3 montaz.py zloz praca/odcinek1 [--kadr blur|crop] [--bez-napisow]
      # wykonuje cięcia z ciecia.json, kadruje do 1080×1920, wypala napisy, normalizuje do −14 LUFS,
      # transkrybuje film po cięciach do korekty napisów
  python3 napisy.py wypal …  (polecenie wypisuje montaz.py zloz)
  python3 montaz.py wykoncz praca/odcinek1
      # normalizuje do −14 LUFS i sprawdza wynik (ffprobe, LUFS, arkusz klatek)

Oryginał nigdy nie jest modyfikowany: wszystko dzieje się na kopii w katalogu pracy.
"""
import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAPISY = os.path.join(HERE, "..", "..", "szkola-klamala-napisy", "scripts", "napisy.py")
KLATKI = os.path.join(HERE, "klatki.py")
LUFS, TP, LRA = -14.0, -1.5, 11.0   # TP z zapasem: kodowanie AAC podbija szczyt o ok. 0,3–0,5 dB


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration",
               "-of", "json", path], capture_output=True, text=True).stdout
    return json.loads(out)


# ───────────────────────── 1. przygotowanie ─────────────────────────
def norm(t):
    return re.sub(r"[^\wąćęłńóśźż ]", "", t.lower()).strip()


def propozycja_ciec(slowa, pauza=0.45, oddech=0.12, podobne=0.72):
    """Zostaw mowę; usuń pauzy dłuższe niż `pauza` (z marginesem `oddech`) i wcześniejsze podejścia,
    gdy segment powtarza się w kolejnym (zostaje ostatnie podejście – zwykle najlepsze)."""
    segs, words = slowa["segments"], slowa["words"]
    odrzucone = []
    for k in range(len(segs) - 1):
        a, b = norm(segs[k]["text"]), norm(segs[k + 1]["text"])
        if not a or not b:
            continue
        # powtórzenie: początek kolejnego segmentu jest bardzo podobny do tego segmentu
        r = difflib.SequenceMatcher(None, a, b[:len(a) + 10]).ratio()
        if r >= podobne:
            odrzucone.append({"start": segs[k]["start"], "end": segs[k]["end"], "tekst": segs[k]["text"],
                              "powod": f"gorsze podejście (podobieństwo {r:.2f} do następnego)"})
    def odrzucone_slowo(w):
        return any(o["start"] - 0.05 <= w["start"] and w["end"] <= o["end"] + 0.05 for o in odrzucone)
    keep = [w for w in words if not odrzucone_slowo(w)]
    zostaw = []
    for w in keep:
        s, e = max(0.0, w["start"] - oddech), w["end"] + oddech
        if zostaw and s - zostaw[-1][1] < pauza - 2 * oddech:
            zostaw[-1][1] = max(zostaw[-1][1], e)
        else:
            zostaw.append([s, e])
    return {"zostaw": [[round(s, 3), round(e, 3)] for s, e in zostaw], "odrzucone_podejscia": odrzucone,
            "uwaga": "Przejrzyj: możesz usunąć/dodać przedziały w 'zostaw' (sekundy oryginału). Potem: montaz.py zloz"}


def przygotuj(src, praca, model):
    os.makedirs(praca, exist_ok=True)
    ext = os.path.splitext(src)[1].lower() or ".mp4"
    kopia = os.path.join(praca, "kopia" + ext)
    h0 = sha(src)
    shutil.copy2(src, kopia)
    if sha(kopia) != h0:
        sys.exit("Kopia różni się od oryginału – przerwano.")
    json.dump({"oryginal": os.path.abspath(src), "sha256": h0, "kopia": kopia},
              open(os.path.join(praca, "zrodlo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    slowa_path = os.path.join(praca, "kopia.slowa.json")
    run([sys.executable, NAPISY, "transkrybuj", kopia, "--model", model, "--out", slowa_path])
    slowa = json.load(open(slowa_path, encoding="utf-8"))
    plan = propozycja_ciec(slowa)
    json.dump(plan, open(os.path.join(praca, "ciecia.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    dur = float(probe(kopia)["format"]["duration"])
    zost = sum(e - s for s, e in plan["zostaw"])
    print(f"Kopia: {kopia} (SHA-256 zgodne z oryginałem)")
    print(f"Długość {dur:.1f} s → po cięciach ok. {zost:.1f} s; odrzucone podejścia: {len(plan['odrzucone_podejscia'])}")
    for o in plan["odrzucone_podejscia"]:
        print(f"  ✂ {o['start']:.1f}–{o['end']:.1f} s: „{o['tekst']}” ({o['powod']})")
    print(f"Plan cięć: {os.path.join(praca, 'ciecia.json')}")


# ───────────────────────── 2. złożenie ─────────────────────────
def tnij(kopia, zostaw, out):
    """Cięcia z mikro-przenikaniem dźwięku (10 ms), żeby nie było trzasków na łączeniach."""
    has_a = any(s["codec_type"] == "audio" for s in probe(kopia)["streams"])
    fc, cat = [], ""
    for k, (s, e) in enumerate(zostaw):
        fc.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{k}]")
        if has_a:
            d = e - s
            fc.append(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0, d - 0.01):.3f}:d=0.01[a{k}]")
        cat += f"[v{k}]" + (f"[a{k}]" if has_a else "")
    fc.append(f"{cat}concat=n={len(zostaw)}:v=1:a={1 if has_a else 0}[v]" + ("[a]" if has_a else ""))
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", kopia, "-filter_complex", ";".join(fc), "-map", "[v]"]
    if has_a:
        cmd += ["-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
    run(cmd + ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out])
    return out


def pion(src, out, kadr="blur"):
    """1080×1920. 'crop' – wypełnij i przytnij środek; 'blur' – całe ujęcie na rozmytym, przyciemnionym tle."""
    if kadr == "crop":
        vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30"
        args = ["-vf", vf]
    else:
        fc = ("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
              "gblur=sigma=40,eq=brightness=-0.18[bg];[b]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
              "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=30[v]")
        args = ["-filter_complex", fc, "-map", "[v]", "-map", "0:a?"]
    run(["ffmpeg", "-y", "-v", "error", "-i", src, *args, "-c:v", "libx264", "-preset", "medium", "-crf", "17",
         "-pix_fmt", "yuv420p", "-c:a", "copy", out])
    return out


def glosnosc(src, out):
    """Dwuprzebiegowa normalizacja EBU R128 do −14 LUFS (szczyt −1 dBTP); bez dźwięku – dokłada cichą ścieżkę."""
    if not any(s["codec_type"] == "audio" for s in probe(src)["streams"]):
        run(["ffmpeg", "-y", "-v", "error", "-i", src, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out])
        return out, None
    p1 = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af",
                         f"loudnorm=I={LUFS}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    m = json.loads(p1[p1.rindex("{"):p1.rindex("}") + 1])
    af = (f"loudnorm=I={LUFS}:TP={TP}:LRA={LRA}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    tmp = out + ".etap.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", af, "-ar", "48000", "-c:v", "copy", "-c:a", "aac",
         "-b:a", "192k", "-movflags", "+faststart", tmp])
    # loudnorm bywa ograniczany przez szczyt albo go przekracza – dociągnij głośność do celu i zawsze pilnuj
    # szczytu limiterem (próbkowy, więc z zapasem 1 dB na nadwyżkę true peak po kodowaniu AAC); maks. 3 rundy
    for _ in range(3):
        i, tp = zmierz_lufs(tmp)
        if i is None or (abs(i - LUFS) <= 0.4 and (tp is None or tp <= TP)):
            break
        nxt = out + ".etap2.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-af",
             f"volume={LUFS - i:.2f}dB,alimiter=limit={10 ** ((TP - 1.0) / 20):.3f}:attack=2:release=60:level=false,"
             "aresample=48000", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", nxt])
        os.replace(nxt, tmp)
    os.replace(tmp, out)
    return out, m


def zmierz_lufs(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)
    return (float(i[-1]) if i else None), (float(tp[-1]) if tp else None)


def zloz(praca, kadr, napisy, model):
    zr = json.load(open(os.path.join(praca, "zrodlo.json"), encoding="utf-8"))
    if os.path.exists(zr["oryginal"]) and sha(zr["oryginal"]) != zr["sha256"]:
        print("⚠ Oryginał zmienił się od przygotowania – sprawdź, czy to zamierzone.")
    plan = json.load(open(os.path.join(praca, "ciecia.json"), encoding="utf-8"))
    ciete = tnij(zr["kopia"], plan["zostaw"], os.path.join(praca, "1_ciete.mp4"))
    pionowe = pion(ciete, os.path.join(praca, "2_pion.mp4"), kadr)
    etap = pionowe
    if napisy:
        # transkrypcja po cięciach – czasy słów zgodne z gotowym filmem
        run([sys.executable, NAPISY, "transkrybuj", pionowe, "--model", model])
        print(f"→ Przejrzyj i popraw {os.path.splitext(pionowe)[0]}.slowa.json (słowo w słowo), potem uruchom:")
        print(f"  python3 {NAPISY} wypal {pionowe} --out {os.path.join(praca, '3_napisy.mp4')}")
        print(f"  python3 {__file__} wykoncz {praca}")
        return
    wykoncz(praca, etap)


def wykoncz(praca, src=None):
    src = src or os.path.join(praca, "3_napisy.mp4")
    gotowe = os.path.join(praca, "GOTOWE_1080x1920.mp4")
    glosnosc(src, gotowe)
    kontrola(gotowe)


def kontrola(path):
    p = probe(path)
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    a = [s for s in p["streams"] if s["codec_type"] == "audio"]
    i, tp = zmierz_lufs(path)
    ok_wh = (v["width"], v["height"]) == (1080, 1920)
    print(f"Gotowe: {path}")
    print(f"  obraz {v['width']}×{v['height']} {'✓' if ok_wh else '✗ (wymagane 1080×1920)'}, {v['r_frame_rate']} kl./s, "
          f"dźwięk: {'tak' if a else 'NIE'}, długość {float(p['format']['duration']):.1f} s")
    if i is not None:
        ok_l = abs(i - LUFS) <= 1.0
        print(f"  głośność {i:.1f} LUFS {'✓' if ok_l else '✗ (cel −14 ±1)'}, szczyt {tp} dBFS")
    sheet = run([sys.executable, KLATKI, path, "--n", "11"], capture_output=True, text=True).stdout.strip()
    print(f"  arkusz klatek do obejrzenia: {sheet}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("przygotuj")
    a1.add_argument("nagranie")
    a1.add_argument("--praca", required=True)
    a1.add_argument("--model", default="medium")
    a2 = sub.add_parser("zloz")
    a2.add_argument("praca")
    a2.add_argument("--kadr", choices=["blur", "crop"], default="blur")
    a2.add_argument("--bez-napisow", action="store_true")
    a2.add_argument("--model", default="medium")
    a3 = sub.add_parser("wykoncz")
    a3.add_argument("praca")
    a4 = sub.add_parser("kontrola")
    a4.add_argument("film")
    a = ap.parse_args()
    if a.cmd == "przygotuj":
        przygotuj(a.nagranie, a.praca, a.model)
    elif a.cmd == "zloz":
        zloz(a.praca, a.kadr, not a.bez_napisow, a.model)
    elif a.cmd == "wykoncz":
        wykoncz(a.praca)
    else:
        kontrola(a.film)


if __name__ == "__main__":
    main()
