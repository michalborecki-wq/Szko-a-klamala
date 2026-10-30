#!/usr/bin/env python3
"""
Animowane logo twórcy na końcu każdej rolki „Szkoła kłamała” (zasada Michała z 30.10.2026).

Użycie (zwykle wywołuje to render.py --video automatycznie, przed muzyką):
  python3 logo_outro.py out/<id>.mp4 [--dur 2.8] [--hd]

Dokleja do filmu ok. 2,8 s outro (4K): błysk na cięciu → logo wskakuje z obrotem i z rozmycia →
złota poświata i fala → połysk przez logo → handle @szkola_klamala. Oryginał zostaje jako
<id>_bez_logo.mp4, a <id>_zdarzenia.json dostaje nową długość i zdarzenia (cięcie, uderzenie logo),
więc muzyka.py zgra dźwięk z logo.
"""
import argparse
import base64
import io
import json
import os
import shutil
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render  # noqa: E402  (tło marki, tokeny, koder wideo)

LOGO = os.path.join(HERE, "..", "assets", "logo.png")
TOK = render.TOK

HTML = """<!doctype html><html><head><meta charset='utf-8'><style>{css}
#stage{{position:absolute;inset:0;z-index:4}}
#glow{{position:absolute;left:50%;top:{cy}px;width:900px;height:900px;margin:-450px 0 0 -450px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,199,39,.75) 0%,rgba(255,170,0,.35) 35%,rgba(47,107,255,0) 70%);opacity:0}}
#wave{{position:absolute;left:50%;top:{cy}px;width:640px;height:640px;margin:-320px 0 0 -320px;border-radius:50%;
  border:10px solid {yellow};box-shadow:0 0 40px rgba(255,199,39,.8);opacity:0}}
#logo{{position:absolute;left:50%;top:{cy}px;width:660px;height:660px;margin:-330px 0 0 -330px}}
#logo img{{width:100%;height:100%;display:block}}
#sheen{{position:absolute;inset:0;-webkit-mask-image:url({src});mask-image:url({src});-webkit-mask-size:100% 100%;mask-size:100% 100%;
  background:linear-gradient(105deg,transparent 38%,rgba(255,255,255,.85) 50%,transparent 62%);background-size:300% 100%;
  background-position:150% 0;mix-blend-mode:screen}}
#handle{{position:absolute;left:0;right:0;top:{hy}px;text-align:center;font-family:'Inter Display','Inter';font-weight:900;
  font-style:italic;font-size:66px;color:#fff;text-shadow:0 6px 0 {blue};opacity:0;letter-spacing:.5px}}
#flash{{position:absolute;inset:0;z-index:9;background:radial-gradient(circle at 50% 45%,#fff,rgba(255,199,39,.7) 45%,rgba(47,107,255,0) 80%);opacity:0}}
</style></head><body>
<div class='bg'></div><div class='st a'></div><div class='st a2'></div><div class='st b'></div><div class='st b2'></div>
<div class='vig'></div><div class='grain'></div>
<div id='stage'><div id='glow'></div><div id='wave'></div>
<div id='logo'><img src='{src}'><div id='sheen'></div></div><div id='handle'>{handle}</div></div><div id='flash'></div>
<script>
const $ = id => document.getElementById(id);
const cl = x => Math.min(1, Math.max(0, x));
const outBack = x => {{ const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); }};
const outCubic = x => 1 - Math.pow(1 - x, 3);
window.setT = (t, g) => {{
  $('flash').style.opacity = (0.75 * (1 - cl(t / .28))).toFixed(3);
  const p = cl(t / .55), s = .55 + .45 * outBack(p), b = 18 * (1 - outCubic(cl(t / .4)));
  const L = $('logo');
  L.style.opacity = cl(t / .15).toFixed(3);
  L.style.transform = `scale(${{(s * (1 + .03 * cl((t - .6) / 2.2))).toFixed(4)}}) rotate(${{(-10 * (1 - outCubic(p))).toFixed(2)}}deg)`;
  L.style.filter = b > .1 ? `blur(${{b.toFixed(1)}}px)` : '';
  const gl = t < .45 ? cl((t - .3) / .15) : Math.max(.35, 1 - (t - .45) / .55) + .05 * Math.sin(g * 4);
  $('glow').style.opacity = (gl * .9).toFixed(3);
  $('glow').style.transform = `scale(${{(1 + .4 * cl((t - .3) / .3) * (t < 1 ? 1 : 0)).toFixed(3)}})`;
  const w = cl((t - .45) / .65);
  $('wave').style.opacity = (w > 0 && w < 1 ? 1 - w : 0).toFixed(3);
  $('wave').style.transform = `scale(${{(1 + .75 * outCubic(w)).toFixed(3)}})`;
  $('sheen').style.backgroundPosition = `${{(150 - 200 * cl((t - .8) / .7)).toFixed(1)}}% 0`;
  const h = cl((t - .9) / .4);
  $('handle').style.opacity = h.toFixed(3);
  $('handle').style.transform = `translateY(${{(30 * (1 - outCubic(h))).toFixed(1)}}px)`;
  document.querySelectorAll('.st').forEach((e, i) => e.style.translate = `${{Math.sin(g * .5 + i * 1.7) * 16}}px ${{Math.cos(g * .4 + i) * 8}}px`);
  const gr = document.querySelector('.grain');
  if (gr) gr.style.backgroundPosition = `${{(g * 7919) % 240}}px ${{(g * 6271) % 240}}px`;
}};
</script></body></html>"""


def render_outro(out_mp4, dur=2.8, scale=2, fps=30, handle="@szkola_klamala", g0=0.0):
    from playwright.sync_api import sync_playwright
    f = render.FORMATS["reel"]
    src = "data:image/png;base64," + base64.b64encode(open(LOGO, "rb").read()).decode()
    cy = 860                                   # środek logo – w strefie bezpiecznej 9:16 (250…1490)
    doc = HTML.format(css=render.css(f), cy=cy, hy=cy + 380, src=src, handle=handle,
                      yellow=TOK["yellow"], blue=TOK["blue"])
    proc = render.open_video_pipe(out_mp4, fps)
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(device_scale_factor=scale, viewport={"width": f["W"], "height": f["H"]})
        pg.set_content(doc, wait_until="load")
        pg.evaluate("document.fonts.ready")
        for k in range(round(dur * fps)):
            t = k / fps
            subs = 2 if t < 1.6 else 1          # rozmycie ruchu tam, gdzie logo szybko się rusza
            acc = None
            for j in range(subs):
                tt = t + j / (fps * subs)
                pg.evaluate("([t,g]) => setT(t,g)", [tt, g0 + tt])
                im = Image.open(io.BytesIO(pg.screenshot(type="jpeg", quality=95))).convert("RGB")
                acc = im if acc is None else Image.blend(acc, im, 1 / (j + 1))
            buf = io.BytesIO()
            acc.save(buf, "JPEG", quality=93)
            proc.stdin.write(buf.getvalue())
        br.close()
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg nie złożył outro z logo")
    return out_mp4


def dodaj_logo(mp4, dur=2.8, scale=2):
    """Dokleja outro z logo do <id>.mp4 i aktualizuje <id>_zdarzenia.json (dla muzyki)."""
    base = os.path.splitext(mp4)[0]
    zpath = base + "_zdarzenia.json"
    bez = base + "_bez_logo.mp4"
    if not os.path.exists(bez):
        shutil.copy2(mp4, bez)
    zd = json.load(open(zpath, encoding="utf-8")) if os.path.exists(zpath) else None
    if zd and zd.get("logo"):
        zd["dlugosc"] = zd["logo"]["start"]            # ponowne doklejenie – licz od wersji bez logo
        zd["zdarzenia"] = [e for e in zd["zdarzenia"] if e["t"] < zd["dlugosc"] - 1e-3]
        zd["plansze"] = zd["plansze"][:-1]
    w = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width",
                            "-of", "csv=p=0", bez], capture_output=True, text=True).stdout.strip())
    outro = base + "_logo_outro.mp4"
    L = zd["dlugosc"] if zd else float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", bez],
        capture_output=True, text=True).stdout)
    render_outro(outro, dur, scale=max(1, round(w / 1080)), g0=L)
    lst = base + "_concat.txt"
    open(lst, "w").write(f"file '{os.path.abspath(bez)}'\nfile '{os.path.abspath(outro)}'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    "-movflags", "+faststart", mp4], check=True)
    os.remove(lst)
    if zd:
        zd["logo"] = {"start": round(L, 3), "dlugosc": dur}
        zd["plansze"].append(dur)
        zd["zdarzenia"] += [{"t": round(L, 3), "typ": "przejscie", "wariant": "logo"},
                            {"t": round(L + .45, 3), "typ": "uderzenie"}]
        zd["dlugosc"] = round(L + round(dur * 30) / 30, 3)
        json.dump(zd, open(zpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return mp4


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--dur", type=float, default=2.8)
    a = ap.parse_args()
    print(dodaj_logo(a.video, a.dur))
