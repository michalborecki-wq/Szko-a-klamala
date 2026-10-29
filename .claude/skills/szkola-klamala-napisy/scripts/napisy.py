#!/usr/bin/env python3
"""
Napisy „Szkoła kłamała”: spisywanie mowy (faster-whisper, słowo po słowie z czasami)
i animowane napisy w stylu marki wypalone w pionowym wideo.

Użycie:
  # 1) transkrypcja → <film>.slowa.json (+ .txt do szybkiej korekty)
  python3 napisy.py transkrybuj film.mp4 [--model medium] [--slownik "Kopernik, Merkator"]

  # 2) (Claude czyta .slowa.json i poprawia źle usłyszane słowa – NIE zmienia czasów ani nie streszcza)

  # 3) napisy → <film>.ass + <film>.srt i wideo z wypalonymi napisami
  python3 napisy.py wypal film.mp4 [--slowa film.slowa.json] [--out film_napisy.mp4] [--y 1150]

Styl: Inter Display Black Italic, wersaliki, biały tekst z niebieskim cieniem przesuniętym w dół
(jak nagłówki marki), aktualnie wypowiadane słowo żółte z krótkim „pop”. 1–3 słowa na raz,
zawsze w strefie bezpiecznej 9:16 (góra 250 px, dół 430 px, prawo 150 px).
"""
import argparse
import json
import os
import re
import subprocess
import sys

YELLOW, WHITE, BLUE = "&H0027C7FF", "&H00FFFFFF", "&H00FF6B2F"   # ASS: &HAABBGGRR
W, H = 1080, 1920
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT, PAD_L = 250, 430, 150, 90


# ───────────────────────── transkrypcja ─────────────────────────
def transkrybuj(video, model="medium", slownik=None, out=None):
    from faster_whisper import WhisperModel
    m = WhisperModel(model, device="cpu", compute_type="int8")
    prompt = f"Słownik: {slownik}." if slownik else None
    # dźwięk dekoduje ffmpeg (16 kHz mono) – niezależnie od wersji biblioteki av
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    segs, info = m.transcribe(audio, language="pl", word_timestamps=True, vad_filter=True,
                              initial_prompt=prompt, condition_on_previous_text=False, beam_size=5)
    words, segments = [], []
    for s in segs:
        sw = []
        for w in s.words or []:
            t = w.word.strip()
            if t:
                sw.append({"w": t, "start": round(w.start, 3), "end": round(w.end, 3), "p": round(w.probability, 3)})
        words += sw
        segments.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(),
                         "n_words": len(sw)})
    out = out or os.path.splitext(video)[0] + ".slowa.json"
    json.dump({"model": model, "language": info.language, "segments": segments, "words": words},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.splitext(out)[0] + ".txt", "w", encoding="utf-8") as fh:
        for s in segments:
            fh.write(f"[{s['start']:7.2f}–{s['end']:7.2f}] {s['text']}\n")
    unsure = [w for w in words if w["p"] < 0.5]
    print(out)
    print(f"słów: {len(words)}, niepewnych (p<0,5): {len(unsure)}"
          + ("" if not unsure else " → sprawdź: " + ", ".join(f"{w['w']}@{w['start']:.1f}s" for w in unsure[:30])))
    return out


# ───────────────────────── grupowanie w krótkie frazy ─────────────────────────
def frazy(words, max_words=3, max_chars=15, gap=0.35):
    """Krótkie frazy: łamanie na pauzach, końcach zdań i limicie znaków; krótkie przyimki i spójniki
    („w”, „na”, „ze”, „po”) trzymają się następnego słowa; „%”, „°C” i interpunkcja – poprzedniego."""
    words = sklej(words)
    out, cur = [], []
    for k, w in enumerate(words):
        if cur:
            prev = cur[-1]
            chars = sum(len(x["w"]) + 1 for x in cur) + len(w["w"])
            brk = (w["start"] - prev["end"] > gap or re.search(r"[.!?…:;]$", prev["w"])
                   or len(cur) >= max_words or chars > max_chars)
            if brk and krotkie(prev):
                # nie zostawiaj „w”, „na”, „ze” na końcu frazy – przenieś cały ogon krótkich słów do następnej
                carry = []
                while len(cur) > 1 and krotkie(cur[-1]):
                    carry.insert(0, cur.pop())
                if carry:
                    out.append(cur)
                    cur = carry
                brk = False
            if brk:
                out.append(cur)
                cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return out


# przyimki, spójniki i „nie” – w polskiej typografii nie zostają na końcu wiersza
LACZNIKI = {"a", "i", "o", "u", "w", "z", "we", "ze", "na", "do", "po", "od", "za", "ku", "bo", "że", "iż",
            "czy", "lub", "albo", "oraz", "ale", "by", "gdy", "jak", "nie", "przez", "przy", "pod", "nad", "bez"}


def krotkie(w):
    return w["w"].lower() in LACZNIKI


def sklej(words):
    """Doklej do poprzedniego słowa tokeny, które nie są słowami: „%”, „°C”, samą interpunkcję."""
    out = []
    for w in words:
        if out and re.fullmatch(r"[%‰°CF.,!?…:;)\]–-]+", w["w"]) and not w["w"].isalpha():
            out[-1] = dict(out[-1], w=out[-1]["w"] + ("\u00a0" if w["w"] in ("°C", "°F") else "") + w["w"], end=w["end"])
        else:
            out.append(dict(w))
    return out


def ass_time(t):
    t = max(0, t)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def esc(t):
    return t.replace("\\", "").replace("{", "(").replace("}", ")")


def zrob_ass(words, path, y=1150, size=92):
    y = min(max(y, SAFE_TOP + size), H - SAFE_BOTTOM - size // 2)
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Marka,Inter Display Black,{size},{WHITE},{WHITE},&H00180E0A,{BLUE},-1,-1,0,0,100,100,0,0,1,2.5,7,5,{PAD_L},{SAFE_RIGHT},0,238

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    x = (PAD_L + (W - SAFE_RIGHT)) // 2
    ev = []
    groups = frazy(words)
    for gi, g in enumerate(groups):
        g_end = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else g[-1]["end"] + 0.4
        g_end = min(g_end, g[-1]["end"] + 0.6)          # fraza nie wisi długo w ciszy
        for k, w in enumerate(g):
            s = w["start"] if k else g[0]["start"]
            e = g[k + 1]["start"] if k + 1 < len(g) else g_end
            parts = []
            for j, x_ in enumerate(g):
                t = esc(x_["w"].upper())
                if j == k:   # aktywne słowo: żółte, krótki „pop” 108% → 100%
                    parts.append(r"{\c" + YELLOW + r"&\fscx108\fscy108\t(0,120,\fscx100\fscy100)}" + t + r"{\c" + WHITE + r"&\fscx100\fscy100}")
                else:
                    parts.append(t)
            # wejście całej frazy: lekki wjazd z dołu tylko przy pierwszym słowie
            fad = 0 if s < 0.1 else 60          # pierwsza fraza filmu widoczna od klatki 0
            mv = (r"{\move(%d,%d,%d,%d,0,140)\fad(%d,0)}" % (x, y + 26, x, y, fad)) if k == 0 else (r"{\pos(%d,%d)}" % (x, y))
            ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Marka,,0,0,0,,{mv}{' '.join(parts)}")
    open(path, "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")
    return path


def zrob_srt(words, path):
    def ts(t):
        ms = int(round(t * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    groups = frazy(words, max_words=7, max_chars=42, gap=0.6)
    with open(path, "w", encoding="utf-8") as fh:
        for k, g in enumerate(groups, 1):
            fh.write(f"{k}\n{ts(g[0]['start'])} --> {ts(g[-1]['end'])}\n{' '.join(w['w'] for w in g)}\n\n")
    return path


def wypal(video, slowa=None, out=None, y=1150):
    slowa = slowa or os.path.splitext(video)[0] + ".slowa.json"
    words = sklej(json.load(open(slowa, encoding="utf-8"))["words"])
    base = os.path.splitext(video)[0]
    ass = zrob_ass(words, base + ".ass", y=y)
    srt = zrob_srt(words, base + ".srt")
    out = out or base + "_napisy.mp4"
    assp = ass.replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-vf", f"ass='{assp}'", "-c:v", "libx264",
                    "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy",
                    "-movflags", "+faststart", out], check=True)
    print(out)
    print(ass)
    print(srt)
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("transkrybuj")
    t.add_argument("video")
    t.add_argument("--model", default="medium", help="tiny/base/small/medium/large-v3 (większy = dokładniej, wolniej)")
    t.add_argument("--slownik", help="nazwy własne i trudne słowa, przecinkami")
    t.add_argument("--out")
    w = sub.add_parser("wypal")
    w.add_argument("video")
    w.add_argument("--slowa")
    w.add_argument("--out")
    w.add_argument("--y", type=int, default=1150, help="pionowy środek napisów (px), domyślnie 1150 – nad podpisem aplikacji")
    a = ap.parse_args()
    if a.cmd == "transkrybuj":
        transkrybuj(a.video, a.model, a.slownik, a.out)
    else:
        wypal(a.video, a.slowa, a.out, a.y)


if __name__ == "__main__":
    sys.exit(main())
