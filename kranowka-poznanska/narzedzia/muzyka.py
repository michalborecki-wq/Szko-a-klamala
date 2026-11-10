#!/usr/bin/env python3
"""Oryginalna muzyka i efekty dźwiękowe do rolek „Kranówka Poznańska” – w całości generowane w kodzie.

Uruchomienie (po `node rolki/render.js`):  python3 narzedzia/muzyka.py [1|2|3]
Podmienia cichą ścieżkę w gotowe/rolka-*.mp4 (obraz bez ponownej kompresji), głośność −14 LUFS.
Wymaga: numpy, scipy, ffmpeg.
"""
import math
import pathlib
import subprocess
import sys
import tempfile
import wave

import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "gotowe"
B = 0.78                      # „duży” krok rytmu = odstęp cięć w rolce 1 (ok. 77 BPM)
rng = np.random.default_rng(2026)

# D-dur: Dmaj9 – Bm7 – Gmaj7 – A6. (akord, bas)
CHORDS = [([62, 66, 69, 73, 76], 38), ([59, 62, 66, 69, 74], 35), ([55, 59, 62, 66, 71], 43), ([57, 61, 64, 66, 69], 45)]
ARP = [0, 2, 4, 2, 3, 1, 4, 2]

# Czasy z osi animacji (rolki/rolka.html).
ROLKI = {
    1: dict(plik="rolka-1-odcisk", dur=13.8, anchor=6.9, groove=(6.9, 10.8), final=12.14,
            pour=(0.0, 1.5), thuds=[(1.74, 0.5)], whoosh=[(2.45, 0.8, 1), (3.55, 0.75, -1), (5.6, 0.7, 1), (10.8, 0.7, 1)],
            plinks=[(2.97, 84, .35), (3.04, 91, .25), (3.11, 88, .3), (3.18, 95, .2), (4.99, 81, .8)],
            hits=[4.99, 6.9], intro_plucks=2.2),
    2: dict(plik="rolka-2-lej-tej", dur=11.3, anchor=2.5, groove=(2.5, 8.3), final=9.64,
            pour=(0.05, 1.9), thuds=[], whoosh=[(2.5, 0.7, 1), (5.35, 0.6, 1), (8.3, 0.7, 1)],
            plinks=[(1.9, 78, .8), (4.0, 86, .7), (4.16, 90, .3), (4.32, 93, .2)],
            hits=[1.9, 5.7, 6.75], intro_plucks=None),
    3: dict(plik="rolka-3-nie-dzwigaj", dur=10.6, anchor=2.25, groove=(2.25, 7.6), final=8.94,
            pour=None, thuds=[(0.97, .9), (1.02, .7), (1.08, .8), (1.14, .6), (1.2, .7), (1.27, .5), (1.33, .5), (1.4, .4)],
            whoosh=[(1.78, 0.5, -1), (4.7, 0.7, 1), (7.6, 0.7, 1)],
            plinks=[(2.25, 74, 1.0), (2.45, 81, .4), (2.65, 86, .25)],
            hits=[2.25, 5.05, 5.47, 5.89], intro_plucks=None),
}


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env_exp(n, tau, attack=0.003):
    t = np.arange(n) / SR
    return np.minimum(1, t / attack) * np.exp(-t / tau)


def place(buf, sig, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= buf.shape[0] or i < 0:
        return
    sig = sig[: buf.shape[0] - i]
    l, r = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
    buf[i:i + len(sig), 0] += sig * gain * l
    buf[i:i + len(sig), 1] += sig * gain * r


def filt(x, kind, f, order=2):
    return sosfilt(butter(order, f, kind, fs=SR, output="sos"), x)


# ---------------------------------------------------------------- instrumenty
def pluck(m, dur=0.9, bright=1.0):
    """Miękki „szklany” malet: FM z szybko gasnącym indeksem."""
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    idx = 2.2 * bright * np.exp(-t / 0.06)
    s = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * 3.01 * t))
    s += 0.25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / 0.12)
    return s * env_exp(n, 0.28)


def pad(notes, dur):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for m in notes:
        for det in (-0.06, 0.05):
            f = hz(m + det)
            s += np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) + 0.28 * np.sin(2 * np.pi * 2 * f * t) + 0.1 * np.sin(2 * np.pi * 3 * f * t)
    a, r = int(0.3 * SR), int(0.55 * SR)
    e = np.ones(n); e[:a] = np.linspace(0, 1, a) ** 1.5; e[-r:] *= np.linspace(1, 0, r) ** 1.5
    return filt(s / (len(notes) * 2), "low", 2600) * e


def bass(m, dur=0.5):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * 2 * f * t) + 0.2 * np.sin(2 * np.pi * 3 * f * t)
    return np.tanh(1.6 * s) * env_exp(n, 0.32, 0.008)


def kick():
    n = int(0.3 * SR); t = np.arange(n) / SR
    f = 46 + 110 * np.exp(-t / 0.028)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.11)
    return s + 0.25 * filt(rng.normal(size=n), "high", 3000) * np.exp(-t / 0.004)


def hat(open_=False):
    n = int((0.16 if open_ else 0.05) * SR); t = np.arange(n) / SR
    return filt(rng.normal(size=n), "high", 7500) * np.exp(-t / (0.05 if open_ else 0.012))


def snap():
    n = int(0.16 * SR); t = np.arange(n) / SR
    s = filt(rng.normal(size=n), "band", [1300, 4200])
    e = np.exp(-t / 0.045) + 0.6 * np.exp(-np.abs(t - 0.011) / 0.003)
    return s * e


# ---------------------------------------------------------------- efekty wody
def plink(m=84, dur=0.35):
    """Kropla: krótki glissando w górę + rezonans."""
    n = int(dur * SR); t = np.arange(n) / SR; f0 = hz(m)
    f = f0 * (0.55 + 0.45 * (1 - np.exp(-t / 0.012)))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.07)
    s += 0.35 * np.sin(2 * np.pi * f0 * 2.02 * t) * np.exp(-t / 0.03)
    return s * np.minimum(1, t / 0.002)


def svf_band(x, fc, q):
    """Filtr pasmowy o zmiennej częstotliwości (pętla – tylko dla krótkich efektów)."""
    lo = bp = 0.0; out = np.empty_like(x)
    g = 2 * np.sin(np.pi * np.minimum(fc, SR / 6.5) / SR)
    for i in range(len(x)):
        hi = x[i] - lo - q * bp
        bp += g[i] * hi
        lo += g[i] * bp
        out[i] = bp
    return out


def whoosh(dur=0.7, up=1):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    fc = 350 * (9 ** (t if up > 0 else 1 - t))
    e = np.sin(np.pi * t) ** 1.6
    return svf_band(rng.normal(size=n), fc, 0.55) * e


def pour(dur):
    """Nalewanie: szum o rosnącym rezonansie (szklanka się wypełnia) + bąbelki."""
    n = int(dur * SR); t = np.linspace(0, 1, n)
    s = svf_band(rng.normal(size=n), 520 * (2.6 ** t), 0.35)
    e = np.minimum(1, t / 0.05) * np.minimum(1, (1 - t) / 0.12) * (0.75 + 0.25 * np.sin(2 * np.pi * 9 * t * dur + rng.uniform(0, 6)))
    s = s * e * 0.55
    for _ in range(int(26 * dur)):
        p = plink(rng.uniform(86, 104), 0.12) * rng.uniform(0.08, 0.3)
        i = int(rng.uniform(0.02, 0.95) * n)
        s[i:i + len(p)] += p[: n - i]
    return s


def thud():
    n = int(0.22 * SR); t = np.arange(n) / SR
    f = 62 + 70 * np.exp(-t / 0.02)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.06) + 0.3 * filt(rng.normal(size=n), "band", [300, 1500]) * np.exp(-t / 0.012)


# ---------------------------------------------------------------- aranżacja
def chord_at(t, anchor):
    return CHORDS[int(math.floor((t - anchor) / (2 * B))) % 4]


def build(cfg):
    dur = cfg["dur"]; n = int(dur * SR); A = cfg["anchor"]; g0, g1 = cfg["groove"]
    mus = np.zeros((n, 2)); fx = np.zeros((n, 2))

    # pad – przez cały film, akord co 2 kroki
    k0 = int(math.floor((0 - A) / (2 * B)))
    t = A + k0 * 2 * B
    while t < dur:
        notes, _ = chord_at(t + 0.01, A)
        level = 0.34 if t < g0 - 0.01 else (0.42 if t < g1 - 0.01 else 0.5)
        place(mus, pad(notes, 2 * B + 0.55), max(t, 0) if t >= 0 else 0, level) if t >= 0 else place(mus, pad(notes, 2 * B + 0.55 + t), 0, level)
        t += 2 * B

    # groove: stopa na każdym kroku (w rolce 1 = na każdym cięciu), pstryk na parzystych, hi-hat ósemkami
    step = 0
    t = g0
    while t < g1 - 0.05:
        notes, root = chord_at(t + 0.01, A)
        place(mus, kick(), t, 0.95)
        if step % 2 == 1:
            place(mus, snap(), t, 0.3, 0.15)
        place(mus, bass(root, 0.55), t, 0.5)
        place(mus, bass(root, 0.3), t + B * 0.75, 0.32)
        for j in range(4):
            place(mus, hat(j == 2 and step % 2 == 1), t + j * B / 4, 0.11 if j % 2 else 0.07, -0.25 if j % 2 else 0.25)
        for j in range(2):                                   # arpeggio ósemkami
            m = notes[ARP[(step * 2 + j) % 8]] + 12
            tt = t + j * B / 2
            place(mus, pluck(m), tt, 0.3, -0.45 if j else 0.45)
            place(mus, pluck(m, bright=0.5), tt + B * 0.375, 0.1, 0.45 if j else -0.45)   # echo
        t += B; step += 1

    # wstęp: rzadkie maletki przed groove’em (na siatce)
    if cfg.get("intro_plucks") is not None:
        t = A - math.floor((A - cfg["intro_plucks"]) / B) * B
        i = 0
        while t < g0 - 0.05:
            notes, _ = chord_at(t + 0.01, A)
            place(mus, pluck(notes[ARP[i % 8]] + 12, bright=0.6), t, 0.2 + 0.03 * i, 0.3 * (-1) ** i)
            t += B; i += 1

    # akcenty: akord maletów w dokładnym czasie zdarzenia na ekranie
    for th in cfg["hits"]:
        notes, root = chord_at(th + 0.01, A)
        for j, m in enumerate(notes):
            place(mus, pluck(m + 12, 1.2, 1.2), th + j * 0.012, 0.2, (j - 2) / 3)
        place(mus, bass(root, 0.7), th, 0.4)

    # finał: kropla trafia na miejsce w logo
    tf = cfg["final"]
    for j, m in enumerate([62, 66, 69, 73, 76, 81]):
        place(mus, pluck(m + 12, 1.6, 1.3), tf + j * 0.03, 0.26, (j - 2.5) / 3.5)
    place(mus, pad([50, 57, 62, 66, 69, 76], dur - tf + 0.2)[: n - int(tf * SR)], tf, 0.55)
    place(mus, bass(38, 1.2), tf, 0.55)
    place(fx, plink(81, 0.5), tf, 0.75)

    # efekty
    if cfg["pour"]:
        p0, p1 = cfg["pour"]; place(fx, pour(p1 - p0), p0, 0.9)
    for tt, gain in cfg["thuds"]:
        place(fx, thud(), tt, 0.8 * gain, rng.uniform(-0.3, 0.3))
    for tt, d, up in cfg["whoosh"]:
        place(fx, whoosh(d, up), tt, 0.42)
    for tt, m, gain in cfg["plinks"]:
        place(fx, plink(m), tt, 0.7 * gain, rng.uniform(-0.4, 0.4))

    mix = mus * 0.8 + fx * 0.75
    mix = filt(mix.T, "high", 32).T
    mix = np.tanh(mix * 1.15) / 1.15
    fade = int(0.9 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 1.4
    mix[: int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))[:, None]
    return mix / max(1e-9, np.abs(mix).max()) * 0.89


def main():
    only = [int(a) for a in sys.argv[1:] if a in "123"] or [1, 2, 3]
    for r in only:
        cfg = ROLKI[r]; mp4 = OUT / f"{cfg['plik']}.mp4"
        mix = build(cfg)
        with tempfile.TemporaryDirectory() as td:
            wav = pathlib.Path(td) / "m.wav"; tmp = pathlib.Path(td) / "o.mp4"
            with wave.open(str(wav), "wb") as w:
                w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
                w.writeframes((mix * 32767).astype("<i2").tobytes())
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-i", str(wav), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                            "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-shortest",
                            "-movflags", "+faststart", str(tmp)], check=True)
            mp4.write_bytes(tmp.read_bytes())
        print(f"rolka {r}: muzyka dodana → gotowe/{mp4.name}")


if __name__ == "__main__":
    main()
