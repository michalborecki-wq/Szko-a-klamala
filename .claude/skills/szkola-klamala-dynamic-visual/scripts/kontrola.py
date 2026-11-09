#!/usr/bin/env python3
"""
Kontrola jakości ruchu rolki „Szkoła kłamała” (Dynamic Visual Engine).

  python3 kontrola.py <rolka.mp4> [--zdarzenia <rolka_zdarzenia.json>] [--przed <stara_rolka.mp4>] [--out katalog]

Tworzy w katalogu --out (domyślnie obok filmu):
  <id>_2s.jpg          – pierwsze 2 s: klatki 0 / 0,15 / 0,3 / 0,5 / 0,8 / 1,2 / 2,0 s (haczyk ma być czytelny w KAŻDEJ)
  <id>_przejscia.jpg   – po 2 klatki przed i po każdym cięciu + klatki „drugiego akcentu” (z pliku zdarzeń)
  <id>_przed_po.jpg    – (z --przed) te same chwile starej i nowej wersji jeden pod drugim
  <id>_kontrola.json   – pomiary automatyczne (DVE 9.11): parametry pliku, migotanie, czarne klatki,
                         najdłuższy nieruchomy kadr, średni ruch, głośność; z --przed także pomiary starej wersji
Obrazy ogląda się narzędziem Read. Pomiary wyłapują błędy techniczne; ocena wyglądu należy do człowieka/agenta.
Kod wyjścia 1, gdy pomiar znalazł błąd (⚠ BŁĄD) – rolki nie wysyłaj, dopóki go nie poprawisz.
"""
import argparse
import io
import json
import os
import subprocess
import sys

import numpy as np

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


def parametry(mp4):
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", mp4],
                                   capture_output=True, text=True).stdout or "{}")
    v = next((x for x in pr.get("streams", []) if x["codec_type"] == "video"), {})
    a = next((x for x in pr.get("streams", []) if x["codec_type"] == "audio"), None)
    n, d = (v.get("r_frame_rate", "0/1").split("/") + ["1"])[:2]
    return {"w": v.get("width"), "h": v.get("height"), "fps": round(int(n) / max(1, int(d)), 2), "kodek": v.get("codec_name"),
            "audio": bool(a), "dlugosc": round(float(pr.get("format", {}).get("duration", 0)), 2)}


def luma(mp4, fps):
    """Jasność i ruch klatka po klatce w małej rozdzielczości (90×160, szarość)."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-vf", "scale=90:160,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 160, 90).astype(np.float32)
    return fr, fps


def glosnosc(mp4):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    import re
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)
    return float(m[-1]) if m else None


def pomiary(mp4, cuts=()):
    par = parametry(mp4)
    fr, fps = luma(mp4, par["fps"] or 30)
    mean = fr.mean(axis=(1, 2))
    diff = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2)) if len(fr) > 1 else np.zeros(1)
    t = np.arange(len(diff)) / fps
    near_cut = np.array([any(abs(x - c) < .35 for c in cuts) for x in t]) if cuts else np.zeros(len(t), bool)
    # migotanie: jasność skacze i wraca w ciągu 1–2 klatek poza przejściami
    dm = np.diff(mean)
    mig = [round(float(i / fps), 2) for i in range(1, len(dm) - 1)
           if abs(dm[i]) > 18 and np.sign(dm[i]) != np.sign(dm[i + 1]) and abs(dm[i + 1]) > 12 and not near_cut[min(i, len(near_cut) - 1)]]
    czarne = [round(float(i / fps), 2) for i, m in enumerate(mean) if m < 4]
    # najdłuższy „stojący” kadr (średnia zmiana < 0,25 poziomu jasności na klatkę), bez końcowego logo (ostatnie 3 s)
    lim = max(1, len(diff) - int(3 * fps)); run = best = 0; start = bs = 0
    for i, d in enumerate(diff[:lim]):
        if d < .25:
            if run == 0: start = i
            run += 1
            if run > best: best, bs = run, start
        else:
            run = 0
    wynik = {"plik": par, "ruch_sredni": round(float(diff[:lim].mean()), 3), "ruch_2s": round(float(diff[:int(2 * fps)].mean()), 3),
             "najdluzszy_stoj_s": round(best / fps, 2), "stoj_od_s": round(bs / fps, 2),
             "migotanie_s": mig[:20], "czarne_klatki": len(czarne), "lufs": glosnosc(mp4) if par["audio"] else None}
    bledy = []
    if (par["w"], par["h"]) not in ((1080, 1920), (2160, 3840)): bledy.append(f"rozdzielczość {par['w']}×{par['h']} (ma być 9:16 1080×1920 albo 2160×3840)")
    if (par["fps"] or 0) < 29.9: bledy.append(f"{par['fps']} kl./s (min. 30)")
    if not par["audio"]: bledy.append("brak ścieżki audio")
    if mig: bledy.append(f"możliwe migotanie w {mig[:5]} s")
    if czarne: bledy.append(f"{len(czarne)} czarnych klatek (od {czarne[0]} s)")
    if best / fps > 4: bledy.append(f"kadr stoi {best / fps:.1f} s (od {bs / fps:.1f} s) – brief: zmiana co 2–4 s")
    # −14 LUFS dotyczy pliku z naszym podkładem (IG); plik TikTok/efekty jest celowo cichszy (dźwięk z trendów w aplikacji)
    pelny = any(k in os.path.basename(mp4).lower() for k in ("muzyka", "instagram"))
    if pelny and wynik["lufs"] is not None and wynik["lufs"] > -50 and abs(wynik["lufs"] + 14) > 1.5:
        bledy.append(f"głośność {wynik['lufs']} LUFS (cel −14)")
    wynik["bledy"] = bledy
    return wynik


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
    cuts = []
    if os.path.exists(zdj):
        cuts = [e["t"] for e in json.load(open(zdj, encoding="utf-8"))["zdarzenia"] if e["typ"] == "przejscie"]
    po = pomiary(a.mp4, cuts)
    raport = {"po": po}
    if a.przed:
        zp = os.path.join(os.path.dirname(a.przed), os.path.splitext(os.path.basename(a.przed))[0].replace("_muzyka", "") + "_zdarzenia.json")
        cp = [e["t"] for e in json.load(open(zp, encoding="utf-8"))["zdarzenia"] if e["typ"] == "przejscie"] if os.path.exists(zp) else []
        raport["przed"] = pomiary(a.przed, cp)
    pj = os.path.join(out, f"{base}_kontrola.json")
    json.dump(raport, open(pj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(pj)
    for k, w in raport.items():
        print(f"[{k.upper()}] {w['plik']['w']}×{w['plik']['h']} {w['plik']['fps']} kl./s {w['plik']['dlugosc']} s, audio={w['plik']['audio']}, "
              f"ruch śr.={w['ruch_sredni']} (0–2 s: {w['ruch_2s']}), najdłuższy stojący kadr={w['najdluzszy_stoj_s']} s, "
              f"LUFS={w['lufs']}")
        for b in w["bledy"]:
            print(f"  ⚠ BŁĄD [{k}]: {b}")
    if a.przed:
        czasy = T2S[:4] + [2.0, 5.0, 9.0, 15.0]
        print(arkusz([("PRZED", a.przed), ("PO", a.mp4)], czasy, os.path.join(out, f"{base}_przed_po.jpg"), 150, 267))
    sys.exit(1 if po["bledy"] else 0)


if __name__ == "__main__":
    main()
