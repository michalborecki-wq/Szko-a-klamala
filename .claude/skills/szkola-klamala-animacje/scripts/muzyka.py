#!/usr/bin/env python3
"""
Muzyka i efekty dźwiękowe „Szkoła kłamała” – oryginalny podkład generowany w kodzie (bez praw autorskich
osób trzecich, bez ryzyka wyciszenia) + efekty zsynchronizowane z animacją.

Użycie:
  python3 muzyka.py out/<id>.mp4            # czyta out/<id>_zdarzenia.json (zapisuje render.py --video)
      [--nastroj kosmos|elektro|napiecie|lekki|spokojny] [--bez-muzyki]

Wynik: <id>_muzyka.mp4 (podkład + efekty, −14 LUFS) i <id>_efekty.mp4 (same efekty – pod dźwięk z trendów).

Budowa podkładu: tonacja a-moll / C-dur, akord na takt (4 uderzenia). Plansza 1 (haczyk) startuje
uderzeniem i lżejszym rytmem, od planszy 2 pełny rytm; przed każdym cięciem narastanie (riser),
na cięciu świst i talerz; uderzenia (liczby, pieczątka) ściszają podkład na moment (ducking).
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from scipy import signal

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "szkola-klamala-montaz", "scripts"))
import montaz  # noqa: E402

RNG = np.random.default_rng(2026)


# ───────────────────────── narzędzia DSP ─────────────────────────
def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(d):
    return np.arange(int(d * SR)) / SR


def env(n, a=0.005, d=0.2, s=0.0, r=0.05, hold=None):
    """ADSR w próbkach; hold = czas trwania nuty (s) przed zwolnieniem."""
    t = np.arange(n) / SR
    hold = hold if hold is not None else n / SR
    e = np.where(t < a, t / max(a, 1e-6), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-6)))
    rel = t > hold
    e[rel] *= np.exp(-(t[rel] - hold) / max(r, 1e-6))
    return e


def sos(kind, f, order=2):
    return signal.butter(order, f, btype=kind, fs=SR, output="sos")


def filt(x, kind, f, order=2):
    return signal.sosfilt(sos(kind, f, order), x, axis=0)


def saw(freq, d, detune=(-0.08, 0.0, 0.08), harm=40):
    t = tt(d)
    out = np.zeros_like(t)
    for dt in detune:
        f = freq * 2 ** (dt / 12)
        for k in range(1, harm + 1):
            if f * k > 9000:
                break
            out += np.sin(2 * np.pi * f * k * t + k * 1.3 * dt) / k
    return out / len(detune)


def reverb(x, sec=1.6, mix=0.25, pre=0.02):
    n = int(sec * SR)
    ir = RNG.standard_normal(n) * np.exp(-np.arange(n) / SR * 6.9 / sec)
    ir = filt(ir, "lowpass", 6000)
    ir = np.concatenate([np.zeros(int(pre * SR)), ir])
    ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
    wet = signal.fftconvolve(x, ir)[: len(x)]
    return x * (1 - mix) + wet * mix * 0.9


def place(buf, x, t, gain=1.0):
    i = int(round(t * SR))
    if i >= len(buf) or i + len(x) <= 0:
        return
    a, b = max(0, i), min(len(buf), i + len(x))
    buf[a:b] += x[a - i: b - i] * gain


def sweep_noise(d, f0, f1, q=1.2):
    """Szum z filtrem pasmowym przesuwanym w czasie (STFT) – świsty i narastania."""
    n = int(d * SR)
    x = RNG.standard_normal(n)
    f, tm, Z = signal.stft(x, SR, nperseg=1024)
    for j in range(Z.shape[1]):
        p = j / max(1, Z.shape[1] - 1)
        fc = f0 * (f1 / f0) ** p
        bw = fc / q
        Z[:, j] *= np.exp(-0.5 * ((f - fc) / bw) ** 2)
    _, y = signal.istft(Z, SR, nperseg=1024)
    y = y[:n]
    return y / (np.max(np.abs(y)) + 1e-9)


# ───────────────────────── instrumenty ─────────────────────────
def kick(g=1.0):
    t = tt(0.45)
    f = 48 + 110 * np.exp(-t * 28)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)
    x[:240] += RNG.standard_normal(240) * np.linspace(.5, 0, 240)
    return np.tanh(x * 1.6) * g


def clap(g=1.0):
    n = int(0.3 * SR)
    x = np.zeros(n)
    for k, off in enumerate((0, .011, .022)):
        b = RNG.standard_normal(int(.02 * SR)) * np.exp(-np.arange(int(.02 * SR)) / SR * 90)
        place(x, b, off, 1 - k * .15)
    tail = RNG.standard_normal(n) * np.exp(-np.arange(n) / SR * 14)
    x += tail * .5
    return filt(filt(x, "highpass", 900), "lowpass", 5000) * g


def hat(g=1.0, d=0.05):
    n = int(0.12 * SR)
    x = RNG.standard_normal(n) * np.exp(-np.arange(n) / SR / d)
    return filt(x, "highpass", 7500, 4) * g


def tick(g=1.0):
    t = tt(0.06)
    return (np.sin(2 * np.pi * 2400 * t) + .5 * np.sin(2 * np.pi * 3700 * t)) * np.exp(-t * 90) * g


def pluck(m, d=0.35, g=1.0, bright=1.0):
    t = tt(d + 0.3)
    f = mtof(m)
    mod = np.sin(2 * np.pi * f * 2 * t) * 2.2 * bright * np.exp(-t * 9)
    x = np.sin(2 * np.pi * f * t + mod) * np.exp(-t * 6)
    x += 0.25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 18)
    return x * env(len(t), 0.003, 1, 1, 0.08, hold=d) * g


def bell(m, g=1.0):
    t = tt(1.6)
    f = mtof(m)
    x = np.sin(2 * np.pi * f * t + 1.6 * np.sin(2 * np.pi * f * 3.5 * t) * np.exp(-t * 3)) * np.exp(-t * 2.4)
    return x * g


def pad(notes, d, g=1.0, cutoff=1400):
    x = sum(saw(mtof(m), d) for m in notes) / len(notes)
    x = filt(x, "lowpass", cutoff, 2)
    return x * env(len(x), 0.35, 1, 1, 0.4, hold=d - 0.1) * g


def bass(m, d, g=1.0, cutoff=380):
    t = tt(d)
    f = mtof(m)
    x = 0.4 * np.sin(2 * np.pi * f * t) + 0.55 * filt(saw(f, d, (0.0,), 20), "lowpass", cutoff * 1.6)
    return x * env(len(t), 0.004, 0.25, 0.7, 0.05, hold=d * 0.85) * g


# ───────────────────────── efekty dźwiękowe ─────────────────────────
def sfx_whoosh(g=1.0, d=0.42):
    y = sweep_noise(d, 300, 5500, q=1.4) * np.sin(np.linspace(0, np.pi, int(d * SR))) ** 1.5
    return reverb(y, 0.8, 0.2) * g


def sfx_boom(g=1.0):
    t = tt(0.9)
    f = 32 + 70 * np.exp(-t * 9)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.2)
    return np.tanh(x * 1.4) * g


def sfx_impact(g=1.0):
    x = sfx_boom(.9)
    hit = RNG.standard_normal(int(.25 * SR)) * np.exp(-np.arange(int(.25 * SR)) / SR * 30)
    place(x, filt(hit, "bandpass", [1200, 6000]) * .5, 0)
    shimmer = sum(bell(m, .12) for m in (81, 88, 93))
    place(x, shimmer[: len(x)], 0.0)
    return reverb(x, 1.4, 0.22) * g


def sfx_crash(g=1.0):
    n = int(1.6 * SR)
    x = RNG.standard_normal(n) * np.exp(-np.arange(n) / SR * 2.6)
    return reverb(filt(x, "highpass", 4500, 2), 1.2, 0.3) * g


def sfx_swish(g=1.0):
    d = 0.32
    y = sweep_noise(d, 1800, 7000, q=2.5) * np.linspace(0.2, 1, int(d * SR)) * np.exp(-np.linspace(0, 3, int(d * SR)))
    return y * g


def sfx_stamp(g=1.0):
    t = tt(0.5)
    thump = np.sin(2 * np.pi * np.cumsum(70 + 90 * np.exp(-t * 40)) / SR) * np.exp(-t * 14)
    knock = filt(RNG.standard_normal(len(t)) * np.exp(-t * 45), "bandpass", [400, 2500])
    return reverb(np.tanh((thump + .7 * knock) * 2), 0.6, 0.18) * g


def sfx_marker(g=1.0):
    d = 0.22
    y = sweep_noise(d, 2500, 5200, q=4) * np.sin(np.linspace(0, np.pi, int(d * SR)))
    return y * g


def sfx_riser(d, g=1.0):
    y = sweep_noise(d, 400, 7000, q=1.1) * np.linspace(0, 1, int(d * SR)) ** 2.2
    return y * g


def sfx_pop(g=1.0):
    t = tt(0.09)
    return np.sin(2 * np.pi * (900 + 600 * np.exp(-t * 60)) * t) * np.exp(-t * 45) * g


def sfx_wrong(g=1.0):
    t = tt(0.35)
    return filt(np.sign(np.sin(2 * np.pi * 140 * t)) * np.exp(-t * 6), "lowpass", 1800) * g


# ───────────────────────── kompozycja ─────────────────────────
PROG = {
    "moll": [(57, 60, 64), (53, 57, 60), (55, 60, 64), (55, 59, 62)],     # Am F C G
    "napiecie": [(57, 60, 64), (57, 60, 64), (53, 57, 60), (56, 59, 64)],  # Am Am F E
    "dur": [(60, 64, 67), (55, 59, 62), (57, 60, 64), (53, 57, 60)],      # C G Am F
}


def compose(nastroj, bpm, length, cuts):
    beat = 60.0 / bpm
    n = int((length + 2.0) * SR)
    L = {k: np.zeros(n) for k in ("drums", "bass", "pad", "lead")}
    prog = PROG["napiecie" if nastroj == "napiecie" else ("dur" if nastroj == "lekki" else "moll")]
    first_cut = cuts[0] if cuts else length
    nb = int(np.ceil(length / beat)) + 1
    for b in range(nb):
        t0 = b * beat
        bar, pos = divmod(b, 4)
        chord = prog[bar % 4]
        full = t0 >= first_cut - 1e-6                # pełny rytm od planszy 2
        # ── perkusja
        if nastroj == "kosmos":
            if full and pos in (0, 2):
                place(L["drums"], kick(.7), t0)
            place(L["drums"], hat(.10 if full else .05, .03), t0 + beat / 2)
        elif nastroj == "spokojny":
            if pos in (0, 2) and (full or pos == 0):
                place(L["drums"], kick(.75), t0)
            if pos in (1, 3) and full:
                place(L["drums"], filt(clap(.5), "lowpass", 3000), t0)
            place(L["drums"], hat(.10, .03), t0 + beat / 2)
        else:
            if full or pos == 0:
                place(L["drums"], kick(.9), t0)
            if pos in (1, 3) and full:
                place(L["drums"], clap(.55 if nastroj != "lekki" else .45), t0)
            place(L["drums"], hat(.16 if full else .09), t0 + beat / 2)
            if full and nastroj in ("elektro", "napiecie"):
                for k in (1, 3):
                    place(L["drums"], hat(.06, .02), t0 + k * beat / 4)
        if b == 0:
            place(L["drums"], kick(1.0), 0)
        # ── bas
        root = chord[0] - 24 if chord[0] - 24 >= 33 else chord[0] - 12
        if nastroj == "kosmos":
            if pos == 0:
                place(L["bass"], bass(root, beat * 4, .55, 220), t0)
        elif nastroj == "spokojny":
            if pos in (0, 2):
                place(L["bass"], bass(root, beat * 1.8, .6, 300), t0)
        else:
            for k in (0, 1):                          # ósemki, druga ciszej (pompowanie)
                place(L["bass"], bass(root, beat * .45, .65 if k == 0 else .45), t0 + k * beat / 2)
        # ── pad (akord na takt)
        if pos == 0:
            cutoff = 900 if not full else (1600 if nastroj != "kosmos" else 2400)
            place(L["pad"], pad(chord, beat * 4 + .3, .32, cutoff), t0)
        # ── melodia / arpeggio
        if nastroj == "kosmos":
            for k in range(2):
                m = chord[(b * 2 + k) % 3] + 24
                place(L["lead"], bell(m, .16), t0 + k * beat / 2)
        elif nastroj == "spokojny":
            if pos in (0, 2):
                for m in chord:
                    place(L["lead"], pluck(m + 12, beat * 1.5, .12, .5), t0 + (m % 3) * .012)
        else:
            steps = 4 if nastroj in ("elektro", "napiecie") else 2
            for k in range(steps):
                m = chord[(b * steps + k) % 3] + 12 + (12 if (b * steps + k) % 8 == 7 else 0)
                gain = (.22 if full else .14) * (1 if k % 2 == 0 else .7)
                place(L["lead"], pluck(m, beat / steps * .9, gain, 1.2 if nastroj == "lekki" else 1.0), t0 + k * beat / steps)
    lead = L["lead"]
    if nastroj in ("kosmos", "elektro"):               # echo ósemkowe na melodii
        d = int(beat * .75 * SR)
        echo = np.zeros_like(lead)
        echo[d:] = lead[:-d] * .35
        echo[2 * d:] += lead[:-2 * d] * .15
        lead = lead + filt(echo, "lowpass", 4000)
    mix = (L["drums"] * .85 + L["bass"] * .5 + reverb(L["pad"], 2.4, .35) * 1.0 + reverb(lead, 1.6, .28) * 1.1)
    return mix[: int(length * SR)]


def sfx_track(events, length, cuts):
    n = int((length + 2.0) * SR)
    fx, duck = np.zeros(n), np.ones(n)

    def ducking(t, depth=.45, d=.35):
        i = int(t * SR)
        k = np.arange(int(d * SR))
        seg = 1 - depth * np.exp(-k / SR * 9)
        a, b = max(0, i), min(n, i + len(k))
        duck[a:b] = np.minimum(duck[a:b], seg[: b - a])

    for c in cuts:
        place(fx, sfx_riser(1.0, .25), c - 1.0)
        place(fx, sfx_whoosh(.55), c - 0.3)
        place(fx, sfx_crash(.22), c)
        place(fx, sfx_boom(.35), c)
        ducking(c, .35, .3)
    for e in events:
        t, typ = e["t"], e["typ"]
        if typ == "start":
            place(fx, sfx_impact(.55), 0)
            ducking(0, .3, .4)
        elif typ == "uderzenie":
            place(fx, sfx_impact(.7), t)
            ducking(t, .5, .45)
        elif typ == "pieczatka":
            place(fx, sfx_stamp(.8), t)
            ducking(t, .45, .3)
        elif typ == "przekreslenie":
            place(fx, sfx_swish(.4), t)
        elif typ == "marker":
            place(fx, sfx_marker(.18), t)
        elif typ == "naglowek":
            place(fx, sfx_whoosh(.12, .3), t - .05)
        elif typ in ("etykieta", "pop"):
            place(fx, sfx_pop(.12), t)
        elif typ == "tik":
            place(fx, tick(.5), t)
        elif typ == "zle":
            place(fx, sfx_wrong(.35), t)
    m = int(length * SR)
    return fx[:m], duck[:m]


def master(x, peak_out=0.8):
    # telefon nie gra poniżej ~80 Hz: tniemy subbas, żeby nie zjadał głośności melodii
    x = signal.sosfilt(sos("highpass", 45, 2), x, axis=0)
    peak = np.max(np.abs(x)) + 1e-9
    x = x / peak * peak_out
    return np.tanh(x * 1.2) / np.tanh(1.2)


def write_wav(path, mono_or_st):
    from scipy.io import wavfile
    st = mono_or_st if mono_or_st.ndim == 2 else np.stack([mono_or_st, mono_or_st], 1)
    wavfile.write(path, SR, (np.clip(st, -1, 1) * 32767).astype(np.int16))


def stereo(x, width=0.0, delay_ms=11):
    """Lekka szerokość stereo dla podkładu (efekt Haasa na wysokich), bas i stopa zostają w środku."""
    hi = filt(x, "highpass", 600)
    lo = x - hi
    d = int(delay_ms / 1000 * SR)
    r = np.concatenate([np.zeros(d), hi[:-d]]) if d else hi
    return np.stack([lo + hi * (1 + width * .3), lo + r * (1 - width * .3)], 1)


def tiktok_1080(src, out):
    """Wersja na TikTok: 1080×1920 z mastera 4K (lanczos), H.264 High@4.1. Edytor TikToka (iOS, 29.10.2026)
    po wczytaniu pionowego pliku 2160×3840 wyświetla obraz podwójnie, jeden pod drugim; TikTok i tak
    pokazuje maks. 1080×1920."""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", "scale=1080:1920:flags=lanczos,setsar=1",
                    "-c:v", "libx264", "-profile:v", "high", "-level:v", "4.1", "-preset", "slow", "-crf", "16",
                    "-pix_fmt", "yuv420p", "-r", "30", "-g", "60", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", out], check=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--zdarzenia")
    ap.add_argument("--nastroj")
    ap.add_argument("--bez-muzyki", action="store_true", help="tylko efekty (np. pod dźwięk z trendów TikToka)")
    a = ap.parse_args()

    base = os.path.splitext(a.video)[0]
    zd = json.load(open(a.zdarzenia or base + "_zdarzenia.json", encoding="utf-8"))
    length = zd["dlugosc"]
    nastroj = a.nastroj or zd.get("nastroj") or "lekki"
    bpm = zd.get("bpm") or 110
    cuts = [e["t"] for e in zd["zdarzenia"] if e["typ"] == "przejscie"]
    fx, duck = sfx_track(zd["zdarzenia"], length, cuts)

    wyniki = []
    for wariant in (["efekty"] if a.bez_muzyki else ["muzyka", "efekty"]):
        if wariant == "muzyka":
            mus = compose(nastroj, bpm, length, cuts)
            fade = int(.12 * SR)
            mus[-fade:] *= np.linspace(1, 0, fade)
            mix = stereo(mus * duck * .55, 1.0) + stereo(fx * .9, .5)
        else:
            mix = stereo(fx, .5)
        mix = master(mix, 0.8 if wariant == "muzyka" else 0.5)   # same efekty: zapas – muzyka dojdzie w aplikacji
        wav = f"{base}_{wariant}.wav"
        write_wav(wav, mix)
        tmp = f"{base}_{wariant}_tmp.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.video, "-i", wav, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", tmp], check=True)
        out = f"{base}_{wariant}.mp4"
        if wariant == "muzyka":
            montaz.glosnosc(tmp, out)                # −14 LUFS
            os.remove(tmp)
        else:
            os.replace(tmp, out)                     # same efekty: bez podbijania – muzyka dojdzie w aplikacji
        wyniki.append(out)
        if wariant == "muzyka":
            tt = f"{base}_tiktok_1080.mp4"
            tiktok_1080(out, tt)
            wyniki.append(tt)
            print(f"  TikTok: {tt} (1080×1920 – edytor TikToka dubluje obraz plików 4K w pionie)")
        print(f"{wariant}: nastrój {nastroj}, {bpm} BPM, {len(cuts)} cięć na bicie")
        if wariant == "muzyka":
            montaz.kontrola(out)
        else:
            print(f"  {out} – same efekty, celowo ciszej (muzyka z trendów dojdzie w aplikacji)")
    return wyniki


if __name__ == "__main__":
    main()
