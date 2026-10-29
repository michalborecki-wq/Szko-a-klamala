#!/usr/bin/env python3
"""
Reel z lektorem „Szkoła kłamała”: animowane plansze (render.py) + polski lektor (Piper TTS, offline)
+ obróbka głosu + −14 LUFS + napisy SRT.

Użycie:
  python3 lektor.py spec.json --out out [--glos mc_speech] [--tempo 0.97] [--draft]

W spec każdy slajd Reela może mieć pole "lektor" – tekst czytany na tej planszy. Liczby zapisuj słowami
(„dziewięćdziesiąt procent”), skróty rozwijaj („około”, nie „ok.”) – syntezator czyta dosłownie.
Długość planszy wydłuża się automatycznie, gdy wypowiedź jest dłuższa niż `durations`.

Wynik: <id>_lektor.mp4 (gotowy do publikacji), <id>_lektor.srt, plansze JPEG, raport kontroli.
"""
import argparse
import copy
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = os.path.join(HERE, "..", "..", "szkola-klamala-grafiki", "scripts", "render.py")
sys.path.insert(0, os.path.join(HERE, "..", "..", "szkola-klamala-montaz", "scripts"))
import montaz  # noqa: E402  (normalizacja głośności i kontrola gotowego filmu)

VOICES = os.environ.get("PIPER_VOICES", "/root/piper")
# głos radiowy: bez dudnienia, równa dynamika, odrobina obecności i „powietrza”
VOICE_FX = ("highpass=f=75,lowpass=f=15000,"
            "acompressor=threshold=-20dB:ratio=3:attack=4:release=90:makeup=3dB,"
            "equalizer=f=200:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=9000:t=h:w=1:g=1.5")


def voice_model(name):
    rel = f"pl/pl_PL/{name}/medium/pl_PL-{name}-medium.onnx"
    path = os.path.join(VOICES, rel)
    if not os.path.exists(path):
        from huggingface_hub import hf_hub_download
        for ext in ("", ".json"):
            hf_hub_download("rhasspy/piper-voices", rel + ext, local_dir=VOICES)
    return path


def tts(text, model, out, tempo):
    subprocess.run([sys.executable, "-m", "piper", "-m", model, "--length-scale", str(tempo), "-f", out],
                   input=text.encode("utf-8"), check=True, capture_output=True)
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                                capture_output=True, text=True, check=True).stdout)


LICZEBNIK = re.compile(r"^(\d\w*|jede?n\w*|dw(a|ie|u|óch|oma|unast\w*|adzie\w*|ieście|ust\w*)|"
                       r"trz(y|ech|ema|ynast\w*|ydzie\w*|yst\w*)|czter\w*|pię[cćt]\w*|sze[śs]\w*|siedem\w*|siedm\w*|"
                       r"osiem\w*|ośm\w*|dziewię\w*|dziesię\w*|dziesiąt\w*|sto|stu|set|tysi\w*|milion\w*|miliard\w*)$")


def norm(t):
    return re.sub(r"[^\wąćęłńóśźż ]", "", t.lower()).split()


def sprawdz_lektora(final, clips, starts, durs):
    """Kontrola słuchu: rozpoznawanie mowy na gotowym filmie – czy lektor jest zrozumiały
    i czy każda wypowiedź pada na swojej planszy. Liczby porównuje po zapisie słownym/cyfrowym luźno."""
    import difflib
    import numpy as np
    from faster_whisper import WhisperModel
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", final, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    segs, _ = WhisperModel("medium", device="cpu", compute_type="int8").transcribe(
        np.frombuffer(raw, np.float32), language="pl", word_timestamps=True)
    words = [w for sg in segs for w in sg.words]
    ok = True
    for i, wav, lead, vd, text in clips:
        a, b = starts[i], starts[i] + durs[i]
        heard = " ".join(w.word for w in words if a <= w.start < b)
        # liczby: lektor czyta słowami, rozpoznawanie zapisuje cyframi i skrótami – porównuj bez liczebników
        heard_n = re.sub(r"%", " procent", re.sub(r"\bkm\b", "kilometrów", heard))
        ref = [x for x in norm(text) if not LICZEBNIK.match(x)]
        hyp = [x for x in norm(heard_n) if not LICZEBNIK.match(x)]
        r = difflib.SequenceMatcher(None, ref, hyp).ratio()
        bad = r < 0.85
        ok &= not bad
        print(f"  lektor, plansza {i + 1}: zgodność {r:.2f} {'⚠ niewyraźne lub poza planszą – zmień sformułowanie' if bad else '✓'}"
              f" | słychać: {heard.strip()}")
    return ok


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out", default="out")
    ap.add_argument("--glos", default="mc_speech", help="mc_speech (najczytelniejszy), gosia, darkman")
    ap.add_argument("--tempo", type=float, default=0.97, help="<1 szybciej, >1 wolniej")
    ap.add_argument("--draft", action="store_true")
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding="utf-8"))
    work = os.path.join(a.out, "_lektor")
    os.makedirs(work, exist_ok=True)
    model = voice_model(a.glos)
    plan = {}
    for post in spec["posts"]:
        if post.get("format") != "reel" or not any(s.get("lektor") for s in post["slides"]):
            continue
        n = len(post["slides"])
        durs = list(post.get("durations") or [2.6] + [3.6] * (n - 1))
        clips = []
        for i, s in enumerate(post["slides"]):
            if not s.get("lektor"):
                continue
            wav = os.path.join(work, f"{post['id']}_{i + 1:02d}.wav")
            vd = tts(s["lektor"], model, wav, a.tempo)
            lead = 0.1 if i == 0 else 0.32          # po przejściu smugą (0,22 s) i chwili oddechu
            tail = 1.0 if i == n - 1 else 0.45
            durs[i] = round(max(durs[i], lead + vd + tail), 2)
            clips.append((i, wav, lead, vd, s["lektor"]))
        post["durations"] = durs
        plan[post["id"]] = clips

    if not plan:
        sys.exit("Brak Reelsów z polem „lektor” w spec.")
    tmp_spec = os.path.join(work, "spec_lektor.json")
    json.dump(spec, open(tmp_spec, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cmd = [sys.executable, RENDER, tmp_spec, "--out", a.out, "--video", "--sheet"] + (["--draft"] if a.draft else [])
    subprocess.run(cmd, check=True)

    for post in spec["posts"]:
        if post["id"] not in plan:
            continue
        durs, clips = post["durations"], plan[post["id"]]
        starts = [sum(durs[:k]) for k in range(len(durs))]
        video = os.path.join(a.out, f"{post['id']}.mp4")
        inputs, fc, labels = ["-i", video], [], ""
        for k, (i, wav, lead, vd, _) in enumerate(clips):
            ms = int(round((starts[i] + lead) * 1000))
            inputs += ["-i", wav]
            fc.append(f"[{k + 1}:a]aresample=48000,{VOICE_FX},adelay={ms}|{ms},aformat=channel_layouts=stereo[a{k}]")
            labels += f"[a{k}]"
        fc.append(f"{labels}amix=inputs={len(clips)}:normalize=0,apad[a]")
        mixed = os.path.join(work, f"{post['id']}_mix.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "0:v",
                        "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", mixed], check=True)
        final = os.path.join(a.out, f"{post['id']}_lektor.mp4")
        montaz.glosnosc(mixed, final)

        # SRT: zdania rozłożone w czasie wypowiedzi proporcjonalnie do długości
        srt, idx = [], 1
        for i, wav, lead, vd, text in clips:
            sent = [x.strip() for x in re.split(r"(?<=[.!?…])\s+", text) if x.strip()]
            total = sum(len(x) for x in sent)
            t = starts[i] + lead
            for x in sent:
                d = vd * len(x) / total
                srt.append(f"{idx}\n{srt_time(t)} --> {srt_time(t + d)}\n{x}\n")
                idx, t = idx + 1, t + d
        open(os.path.join(a.out, f"{post['id']}_lektor.srt"), "w", encoding="utf-8").write("\n".join(srt))
        print(f"Plansze: {', '.join(f'{d:.2f}s' for d in durs)} (razem {sum(durs):.1f} s)")
        montaz.kontrola(final)
        sprawdz_lektora(final, clips, starts, durs)


if __name__ == "__main__":
    main()
