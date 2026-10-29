#!/usr/bin/env python3
"""
Silnik grafik „Szkoła kłamała”.

Użycie:
  python render.py spec.json [--out DIR] [--sheet] [--video]

Spec (JSON) – patrz references/spec-format.md. W skrócie:
{
  "handle": "@szkola_klamala",
  "posts": [
    {"id": "kosmos_mity", "format": "carousel", "vertical_copy": true,
     "series": "SZKOŁA KŁAMAŁA", "subject": "KOSMOS",
     "slides": [ {"type": "cover", ...}, {"type": "myth", ...}, ... ]},
    {"id": "wenus_reel", "format": "reel", "subject": "KOSMOS",
     "durations": [2.6, 4.0, 3.6], "slides": [...]}
  ]
}

Formaty:
  carousel  – 1080×1350 (4:5, Instagram); "vertical_copy": true dorabia natywną wersję 9:16 (TikTok)
  vertical  – 1080×1920 (9:16, TikTok – zdjęcia / Stories)
  reel      – plansze 1080×1920 + MP4 (H.264, 30 kl./s, cicha ścieżka AAC), z flagą --video

Każdy slajd przechodzi automatyczną kontrolę jakości (QA): tekst mieszczący się w strefie
bezpiecznej, minimalne rozmiary czcionek, brak ucięć. Ostrzeżenia trafiają do qa_report.txt.
"""
import argparse
import html
import io
import json
import os
import re
import subprocess
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ───────────────────────── tokeny marki ─────────────────────────
TOK = {
    "bg0": "#0A0E18", "bg1": "#16203A", "blue": "#2F6BFF", "yellow": "#FFC727",
    "red": "#E53935", "white": "#FFFFFF", "text": "#E8E8E8", "muted": "#9AA3B5",
    "strike": "#BFC3CC", "dot": "#34405C",
}

# rozmiar płótna, marginesy i STREFY BEZPIECZNE (miejsce, którego nie zasłania interfejs aplikacji)
FORMATS = {
    # Instagram 4:5 – interfejs nie zasłania treści w feedzie; zostawiamy oddech na pasek i stopkę
    "carousel": dict(W=1080, H=1350, padL=88, padR=88, safeTop=150, safeBottom=150,
                     h1=118, h2=74, body=44, note=30, big=210, min_body=36),
    # 9:16 – u góry nazwa konta/pasek postępu, u dołu podpis i dźwięk, po prawej przyciski TikToka
    "vertical": dict(W=1080, H=1920, padL=90, padR=150, safeTop=250, safeBottom=430,
                     h1=124, h2=86, body=54, note=34, big=250, min_body=44),
}
FORMATS["reel"] = FORMATS["vertical"]

GRAIN = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0'/></filter>"
         "<rect width='100%' height='100%' filter='url(%23n)'/></svg>")

BRUSH = ("<svg class='brush' viewBox='0 0 440 28' preserveAspectRatio='none'>"
         "<path d='M3 17 C 70 6, 190 3, 437 7 L 433 19 C 300 15, 160 18, 70 22 C 40 24, 14 25, 5 24 Z' fill='%s'/>"
         "</svg>" % TOK["red"])

ARROW = ("<svg viewBox='0 0 24 24' width='1em' height='1em' style='vertical-align:-.12em'>"
         "<path d='M4 12h14m-5-6 6 6-6 6' stroke='currentColor' stroke-width='3' fill='none' "
         "stroke-linecap='round' stroke-linejoin='round'/></svg>")


# ───────────────────────── tekst ─────────────────────────
def nbsp(t: str) -> str:
    """Twarde spacje po jednoliterowych spójnikach i przyimkach (polska typografia) + przed „r.”, „%” itd."""
    t = re.sub(r"(?<![\w&;])([aAiIoOuUwWzZ])\s+", r"\1&nbsp;", t)
    t = re.sub(r"(\d)\s+(r\.|w\.|mln|mld|tys\.|km|kg|lat|dni|°C|%|zł)", r"\1&nbsp;\2", t)
    t = re.sub(r"\s+–\s+", "&nbsp;– ", t)
    return t


def rich(t) -> str:
    """Escapuje HTML, **pogrubienie** → żółte wyróżnienie, ~~skreślenie~~, nowa linia → <br>."""
    if t is None:
        return ""
    t = html.escape(str(t), quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"~~(.+?)~~", r"<s>\1</s>", t)
    t = t.replace("\n", "<br>")
    return nbsp(t)


# ───────────────────────── CSS ─────────────────────────
def css(f):
    return f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{f['W']}px;height:{f['H']}px;overflow:hidden}}
body{{font-family:'Inter',sans-serif;color:{TOK['text']};background:{TOK['bg0']};position:relative;
  -webkit-font-smoothing:antialiased;font-feature-settings:'ss01','cv11','tnum' 0}}
.bg{{position:absolute;inset:0;background:
  radial-gradient(ellipse 85% 60% at 50% 38%,{TOK['bg1']} 0%,{TOK['bg0']} 72%)}}
.vig{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(0,0,0,.45) 100%)}}
.grain{{position:absolute;inset:0;background-image:url("{GRAIN}");opacity:.07;mix-blend-mode:overlay}}
.st{{position:absolute;background:linear-gradient(90deg,rgba(47,107,255,0),{TOK['blue']} 30%,{TOK['blue']} 70%,rgba(47,107,255,0));
  transform:rotate(-24deg);filter:blur(5px);border-radius:999px}}
.st.a{{width:980px;height:118px;left:-470px;top:40px;opacity:.55}}
.st.a2{{width:820px;height:34px;left:-360px;top:205px;opacity:.38}}
.st.b{{width:980px;height:118px;right:-470px;bottom:50px;opacity:.48}}
.st.b2{{width:820px;height:34px;right:-360px;bottom:215px;opacity:.36}}

.top{{position:absolute;left:{f['padL']}px;right:{f['padL']}px;top:{int(f['safeTop']*0.36)}px;
  display:flex;justify-content:space-between;align-items:center;z-index:5}}
.wm{{font-family:'Inter Display','Inter';font-weight:900;font-style:italic;font-size:26px;letter-spacing:.5px;color:#fff}}
.wm span{{color:{TOK['yellow']}}}
.dots{{display:flex;gap:10px}}
.dots i{{width:12px;height:12px;border-radius:50%;background:{TOK['dot']}}}
.dots i.on{{background:{TOK['yellow']};box-shadow:0 0 12px rgba(255,199,39,.6)}}
.dots i.done{{background:#7C6A2E}}
.bot{{position:absolute;left:{f['padL']}px;right:{f['padL']}px;bottom:{int(f['safeBottom']*0.36) if f['H']==1350 else 140}px;
  display:flex;justify-content:space-between;align-items:center;font-size:29px;z-index:5}}
.hd{{color:{TOK['muted']};font-weight:600}}
.sw{{color:{TOK['yellow']};font-weight:800;font-style:italic}}

.content{{position:absolute;left:{f['padL']}px;right:{f['padR']}px;top:{f['safeTop']}px;bottom:{f['safeBottom']}px;
  display:flex;flex-direction:column;justify-content:center;z-index:4}}
.content.center{{align-items:center;text-align:center}}
.content.toptight{{justify-content:flex-start;padding-top:{int(f['H']*0.06)}px}}
.chip.red{{background:{TOK['red']};color:#fff;box-shadow:0 8px 24px rgba(229,57,53,.25)}}

.chip{{display:inline-block;align-self:flex-start;background:{TOK['yellow']};color:{TOK['bg0']};
  font-family:'Inter Display','Inter';font-weight:900;font-style:italic;font-size:{int(f['note']*1.0)}px;
  letter-spacing:1px;padding:10px 22px 9px;transform:skew(-8deg);margin-bottom:42px;box-shadow:0 8px 24px rgba(255,199,39,.18)}}
.center .chip{{align-self:center}}
.tag{{display:inline-block;align-self:flex-start;font-family:'Inter Display','Inter';font-weight:900;font-style:italic;
  font-size:{int(f['note']*1.12)}px;letter-spacing:1px;padding:8px 22px 7px;transform:skew(-8deg);color:#fff;margin-bottom:20px}}
.center .tag{{align-self:center}}
.t-mit,.t-przeciw{{background:{TOK['red']}}} .t-fakt,.t-za{{background:{TOK['blue']}}}
.t-zrodla{{background:{TOK['yellow']};color:{TOK['bg0']}}}

h1,h2{{font-family:'Inter Display','Inter';font-weight:900;font-style:italic;text-transform:uppercase;color:#fff;
  letter-spacing:-.5px;text-wrap:balance}}
h1{{font-size:{f['h1']}px;line-height:1.0;text-shadow:0 7px 0 {TOK['blue']}}}
h2{{font-size:{f['h2']}px;line-height:1.04;text-shadow:0 5px 0 {TOK['blue']};margin-bottom:34px}}
h1 .y,h2 .y{{color:{TOK['yellow']};text-shadow:0 7px 0 {TOK['blue']},0 0 44px rgba(255,199,39,.32)}}
h1 .y{{display:block}}
.brush{{display:block;width:430px;height:26px;transform:rotate(-2.5deg);margin:34px 0 36px -6px}}
.center .brush{{margin:34px auto 36px}}

.sub{{font-size:{f['body']}px;line-height:1.32;color:{TOK['text']};text-wrap:pretty}}
.body{{font-size:{f['body']}px;line-height:1.38;color:{TOK['text']};text-wrap:pretty}}
.body b,.sub b{{color:{TOK['yellow']};font-weight:800}}
.note{{font-size:{f['note']}px;line-height:1.35;color:{TOK['muted']};margin-top:34px}}
.src{{font-size:{f['note']}px;color:{TOK['muted']};margin-top:30px}}
.src:before{{content:'';display:inline-block;width:28px;height:3px;background:{TOK['muted']};vertical-align:middle;margin-right:12px;opacity:.6}}

.num{{font-family:'Inter Display','Inter';font-weight:900;font-style:italic;font-size:{int(f['big']*0.7)}px;line-height:.9;
  color:{TOK['yellow']};text-shadow:0 0 44px rgba(255,199,39,.42);margin-bottom:24px}}
.big{{font-family:'Inter Display','Inter';font-weight:900;font-style:italic;font-size:{f['big']}px;line-height:.92;
  color:{TOK['yellow']};text-shadow:0 10px 0 {TOK['blue']},0 0 70px rgba(255,199,39,.4);white-space:nowrap;margin-bottom:28px;
  letter-spacing:-4px}}
.hero{{font-size:{int(f['big']*2.15)}px;letter-spacing:-10px;text-shadow:0 14px 0 {TOK['blue']},0 0 100px rgba(255,199,39,.45)}}
.myth{{font-size:{f['body']}px;line-height:1.32;color:{TOK['strike']};margin-bottom:46px;position:relative}}
.myth s{{text-decoration:none}}
.myth span{{background-image:linear-gradient({TOK['red']},{TOK['red']});background-size:100% 4px;
  background-position:0 58%;background-repeat:no-repeat;-webkit-box-decoration-break:clone;box-decoration-break:clone}}

.card{{background:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.025));border:1px solid rgba(255,255,255,.08);
  border-radius:22px;padding:36px 38px;box-shadow:0 24px 60px rgba(0,0,0,.35)}}
.card + .card{{margin-top:22px}}

.rows{{margin-top:18px}}
.row{{display:grid;grid-template-columns:var(--kw,240px) 1fr auto;align-items:center;gap:20px;margin:20px 0;
  font-size:{int(f['body']*0.82)}px}}
.row .k{{color:{TOK['muted']};font-weight:700}}
.row .track{{height:{int(f['body']*1.05)}px;background:rgba(255,255,255,.06);border-radius:10px;overflow:hidden}}
.row .fill{{height:100%;background:linear-gradient(90deg,#2458E0,{TOK['blue']} 70%,#5B8CFF);border-radius:10px}}
.row .n{{color:{TOK['yellow']};font-weight:900;font-style:italic;min-width:2ch;text-align:right}}

.opt{{font-size:{int(f['body']*0.98)}px;line-height:1.3;margin:18px 0;padding:26px 30px;border-radius:16px;
  background:rgba(255,255,255,.055);border-left:10px solid {TOK['blue']};display:flex;gap:22px;align-items:baseline}}
.opt .l{{color:{TOK['yellow']};font-weight:900;font-style:italic;font-size:1.15em}}
.opt.bad{{border-left-color:{TOK['red']};background:rgba(229,57,53,.16)}}
.opt.dim{{opacity:.45}}
.cd{{font-family:'Inter Display','Inter';font-weight:900;font-style:italic;font-size:{int(f['big']*0.95)}px;
  color:{TOK['yellow']};text-align:center;text-shadow:0 0 60px rgba(255,199,39,.5);margin-top:26px;line-height:1}}
.partner{{margin-top:56px;border:2px dashed rgba(154,163,181,.28);border-radius:18px;height:120px;width:400px;
  display:flex;align-items:center;justify-content:center;color:rgba(154,163,181,.35);font-size:22px;letter-spacing:2px}}
.center .partner{{margin-left:auto;margin-right:auto}}
"""


# ───────────────────────── szablony slajdów ─────────────────────────
def head(s):
    """Nagłówek: 'title' + opcjonalny 'accent' (żółty, w nowej linii w h1, w tej samej w h2)."""
    return rich(s.get("title", "")), rich(s.get("accent", ""))


def tpl(s, post, f, i, n):
    t = s["type"]
    label = f"{post.get('series','SZKOŁA KŁAMAŁA')} · {post.get('subject','')}".strip(" ·")
    title, accent = head(s)
    src = f"<div class='src'>{rich(s['source'])}</div>" if s.get("source") else ""
    note = f"<div class='note'>{rich(s['note'])}</div>" if s.get("note") else ""
    cls = ""

    if t == "cover":
        b = (f"<div class='chip'>{html.escape(label)}</div>"
             f"<h1 data-fit>{title}<span class='y'>{accent}</span></h1>{BRUSH}"
             f"<div class='sub'>{rich(s.get('sub',''))}</div>{note}")
    elif t == "myth":
        num = f"<div class='num'>{html.escape(s['num'])}</div>" if s.get("num") else ""
        b = (f"{num}<div class='tag t-mit'>{html.escape(s.get('myth_label','MIT'))}</div>"
             f"<div class='myth'><span>{rich(s['myth'])}</span></div>"
             f"<div class='tag t-fakt'>{html.escape(s.get('fact_label','FAKT'))}</div>"
             f"<div class='body' data-fit>{rich(s['fact'])}</div>{src}")
    elif t == "number":
        tag = f"<div class='tag t-{s['tag'].lower()}'>{html.escape(s['tag'])}</div>" if s.get("tag") else ""
        b = (f"{tag}<div class='big'>{rich(s['big'])}</div>"
             + (f"<h2>{title} <span class='y'>{accent}</span></h2>" if title or accent else "")
             + f"<div class='body' data-fit>{rich(s.get('body',''))}</div>{note}{src}")
    elif t == "hero":
        cls = "center"
        b = (f"<div class='chip'>{html.escape(label)}</div>"
             f"<div class='big hero'>{rich(s['big'])}</div>"
             f"<h1 data-fit style='font-size:{int(f['h1']*0.78)}px'>{title}<span class='y'>{accent}</span></h1>{BRUSH}"
             f"<div class='sub'>{rich(s.get('sub',''))}</div>{src}")
    elif t == "text":
        tag = f"<div class='tag t-{s['tag'].lower()}'>{html.escape(s['tag'])}</div>" if s.get("tag") else ""
        b = (f"{tag}<h2>{title} <span class='y'>{accent}</span></h2>"
             f"<div class='body' data-fit>{rich(s.get('body',''))}</div>{note}{src}")
    elif t == "versus":
        side = s.get("side", "za")
        b = (f"<div class='tag t-{'za' if side=='za' else 'przeciw'}'>{html.escape(s.get('label', side.upper()))}</div>"
             f"<h2>{title} <span class='y'>{accent}</span></h2>"
             f"<div class='card'><div class='body' data-fit>{rich(s.get('body',''))}</div></div>{src}")
    elif t == "bars":
        rows = s["rows"]
        mx = max(float(r[1]) for r in rows) or 1
        kw = s.get("label_width", 240)
        rr = "".join(
            f"<div class='row'><span class='k'>{rich(r[0])}</span><span class='track'>"
            f"<span class='fill' style='display:block;width:{max(3, 100*float(r[1])/mx):.1f}%'></span></span>"
            f"<span class='n'>{rich(r[2])}</span></div>" for r in rows)
        b = (f"<h2>{title} <span class='y'>{accent}</span></h2>"
             + (f"<div class='body'>{rich(s['body'])}</div>" if s.get("body") else "")
             + f"<div class='rows' style='--kw:{kw}px'>{rr}</div>{note}{src}")
    elif t == "quiz":
        opts = s["options"]
        rev = s.get("reveal")
        oo = ""
        for k, o in enumerate(opts):
            c = "" if rev is None else ("bad" if k == rev else "dim")
            oo += f"<div class='opt {c}'><span class='l'>{chr(65+k)}</span><span>{rich(o)}</span></div>"
        cd = f"<div class='cd'>{s['countdown']}</div>" if s.get("countdown") else ""
        cls = "toptight"  # stała pozycja opcji między klatkami odliczania – nic nie „skacze” w wideo
        chipc = "chip red" if rev is not None else "chip"
        b = (f"<div class='{chipc}'>{rich(s.get('question','KTÓRY FAKT JEST FAŁSZYWY?'))}</div>{oo}{cd}")
    elif t == "outro":
        partner = "<div class='partner'>PARTNER</div>" if s.get("partner_slot", True) else ""
        b = (f"<h2 data-fit>{rich(s.get('question',''))}</h2>{BRUSH}"
             f"<div class='sub'>{rich(s.get('sub',''))}</div>"
             + (f"<div class='src'>{rich(s['sources'])}</div>" if s.get("sources") else "")
             + partner)
    else:
        raise ValueError(f"Nieznany typ slajdu: {t}")

    # górny pasek: znak marki + kropki postępu (tylko karuzele, nie Reelsy)
    dots = ""
    if post["_fmt"] != "reel" and n > 1:
        dots = "<div class='dots'>" + "".join(
            f"<i class='{'on' if k==i else ('done' if k<i else '')}'></i>" for k in range(n)) + "</div>"
    wm = "" if t in ("cover", "hero", "quiz") else "<div class='wm'>SZKOŁA <span>KŁAMAŁA</span></div>"
    top = f"<div class='top'>{wm or '<span></span>'}{dots}</div>"
    swipe = "" if (i == n - 1 or post["_fmt"] == "reel") else f"<span class='sw'>przesuń {ARROW}</span>"
    bot = f"<div class='bot'><span class='hd'>{html.escape(post['_handle'])}</span>{swipe}</div>"

    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css(f)}</style></head><body>"
            f"<div class='bg'></div><div class='st a'></div><div class='st a2'></div><div class='st b'></div>"
            f"<div class='st b2'></div><div class='vig'></div><div class='grain'></div>"
            f"{top}<div class='content {cls}'>{b}</div>{bot}</body></html>")


# ───────────────────────── autodopasowanie + QA w przeglądarce ─────────────────────────
FIT_AND_QA = """
(minBody) => {
  const c = document.querySelector('.content');
  const over = () => c.scrollHeight > c.clientHeight + 1 || c.scrollWidth > c.clientWidth + 1;
  // 0) duże liczby dopasuj najpierw do szerokości – osobno, żeby nie zmniejszać przez nie reszty tekstu
  c.querySelectorAll('.big').forEach(el => {
    let fs = parseFloat(getComputedStyle(el).fontSize), g = 0;
    while (el.scrollWidth > c.clientWidth && g++ < 60) { fs *= 0.97; el.style.fontSize = fs + 'px'; }
  });
  // 1) zmniejszaj całą treść małymi krokami, aż się zmieści (nie poniżej minimum czytelności)
  let scale = 1, guard = 0;
  while (over() && guard++ < 40) {
    scale *= 0.96;
    c.querySelectorAll('h1,h2,.body,.sub,.myth,.opt,.big,.num,.cd,.row').forEach(el => {
      const base = parseFloat(el.dataset.base || getComputedStyle(el).fontSize);
      el.dataset.base = base;
      el.style.fontSize = (base * scale) + 'px';
    });
  }
  const issues = [];
  if (over()) issues.push('TREŚĆ NIE MIEŚCI SIĘ w strefie bezpiecznej – skróć tekst');
  // 2) minimalna czytelność tekstu ciągłego
  c.querySelectorAll('.body,.sub,.myth,.opt').forEach(el => {
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < minBody) issues.push(`czcionka ${fs.toFixed(0)}px < ${minBody}px (${el.className}) – skróć tekst`);
  });
  // 3) nic nie wystaje poza płótno
  const W = innerWidth, H = innerHeight;
  c.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width && (r.right > W + 1 || r.left < -1 || r.bottom > H + 1)) issues.push('element poza kadrem: ' + el.tagName);
  });
  // 4) liczba słów na slajd (czytelność w ruchu)
  const cl = c.cloneNode(true);                       // bez kopii do połysku i kolumn cyfr licznika
  cl.querySelectorAll('.sheen,.col').forEach(e => e.remove());
  const words = (cl.textContent || '').split(/\\s+/).filter(Boolean).length;
  return {issues: [...new Set(issues)], words, scale: +scale.toFixed(2)};
}
"""


# ───────────────────────── animowane napisy (Reelsy) ─────────────────────────
# Klatki renderowane deterministycznie: animacje CSS są zatrzymane, a każda klatka ustawia
# currentTime wszystkich animacji (window.__setT). Dzięki temu wideo jest powtarzalne co do klatki.
import ruch  # noqa: E402  biblioteka efektów ruchu (warianty, tła, przejścia, zdarzenia)

ANIM_CSS = ruch.css(TOK)


def open_video_pipe(out_mp4, fps=30):
    """ffmpeg czyta klatki JPEG ze stdin; dokłada cichą ścieżkę AAC (część systemów odrzuca wideo bez audio)."""
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(fps),
           "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out_mp4]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def default_durations(n):
    return [2.6] + [3.6] * (n - 2) + [3.6] if n > 1 else [4.0]


def render_all(spec, out, video=False, fps=30, sub=2):
    from playwright.sync_api import sync_playwright
    os.makedirs(out, exist_ok=True)
    report, produced, animated = [], {}, {}
    handle = spec.get("handle", "@szkola_klamala")
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page()
        for post in spec["posts"]:
            fmts = [post.get("format", "carousel")]
            if fmts[0] == "carousel" and post.get("vertical_copy"):
                fmts.append("vertical")
            for fmt in fmts:
                f = FORMATS[fmt]
                post["_fmt"], post["_handle"] = fmt, handle
                suffix = {"carousel": "", "vertical": "_916", "reel": "_reel"}[fmt]
                files = []
                n = len(post["slides"])
                anim = video and fmt == "reel" and post.get("animate", True)
                if anim:
                    durs = post.get("durations") or default_durations(n)
                    if len(durs) != n:
                        durs = default_durations(n)
                    bpm = ruch.bpm(post)
                    if bpm:   # cięcia na bit: długość każdej planszy = całkowita liczba uderzeń
                        beat = 60.0 / bpm
                        durs = [max(2, round(d / beat)) * beat for d in durs]
                    fxs = [ruch.styl(post, k, n) for k in range(n)]
                    seed = ruch._h(post["id"]) % 4294967295
                    events, t_start = [], 0.0
                    mp4 = os.path.join(out, f"{post['id']}.mp4")
                    proc, g = open_video_pipe(mp4, fps), 0.0
                    # klatka quizu z odliczaniem/rozwiązaniem kontynuuje poprzednią – bez wyjścia i ponownego wejścia
                    cont = [s["type"] == "quiz" and (s.get("countdown") or s.get("reveal") is not None)
                            for s in post["slides"]]
                for i, s in enumerate(post["slides"]):
                    doc = tpl(s, post, f, i, n)
                    pg.set_viewport_size({"width": f["W"], "height": f["H"]})
                    pg.set_content(doc, wait_until="load")
                    pg.evaluate("document.fonts.ready")
                    if anim:
                        pg.add_style_tag(content=ANIM_CSS)
                        enter = s.get("enter", not cont[i])
                        res = pg.evaluate(ruch.PREP, {"first": i == 0, "enter": enter, "count": s.get("count", True),
                                                      "fx": fxs[i], "seed": seed + i, "subject": post.get("subject", "")})
                        intro = res["t"]
                        if i > 0 and not cont[i]:
                            events.append({"t": round(t_start, 3), "typ": "przejscie", "wariant": fxs[i]["przejscie"]})
                        events += [{"t": round(t_start + e["t"], 3), "typ": e["typ"]} for e in res["ev"]]
                        # stan końcowy animacji – pomiar i JPEG bez przesunięć i powiększeń z wejścia
                        pg.evaluate("window.__setT(60, 0, 999, null, null, false)")
                    qa = pg.evaluate(FIT_AND_QA, f["min_body"])
                    if anim:
                        pg.evaluate("window.__layout()")   # pozycje iskier po dopasowaniu tekstu
                        if enter and intro > durs[i] - 1.2:
                            qa["issues"].append(f"wejście napisów trwa {intro:.1f} s przy planszy {durs[i]} s"
                                                " – wydłuż planszę albo skróć tekst")
                    words_max = 40 if s["type"] in ("quiz", "versus") else 32
                    if qa["words"] > words_max:
                        qa["issues"].append(f"{qa['words']} słów (> {words_max}) – za dużo tekstu na slajd")
                    name = f"{post['id']}{suffix}_{i+1:02d}.jpg"
                    path = os.path.join(out, name)
                    png = path[:-4] + ".png"
                    pg.screenshot(path=png)
                    Image.open(png).convert("RGB").save(path, "JPEG", quality=93, optimize=True, subsampling=0)
                    os.remove(png)
                    files.append(path)
                    tagline = f"{name}: słowa={qa['words']} skala={qa['scale']}"
                    report.append(tagline + ("" if not qa["issues"] else "  ⚠ " + " | ".join(qa["issues"])))
                    if anim:
                        nf = round(durs[i] * fps)
                        exit_ = fxs[i + 1]["przejscie"] if i < n - 1 and not cont[i + 1] else None
                        wipe_in = fxs[i]["przejscie"] if i > 0 and not cont[i] else None
                        push = not cont[i] and not (i + 1 < n and cont[i + 1])   # quiz stoi w miejscu
                        for k in range(nf):
                            # rozmycie ruchu: średnia z `sub` podklatek w obrębie jednej klatki wyjściowej
                            if sub == 1:
                                pg.evaluate("(a) => window.__setT(...a)", [k / fps, g + k / fps, durs[i], exit_, wipe_in, push])
                                proc.stdin.write(pg.screenshot(type="jpeg", quality=93))
                                continue
                            acc = None
                            for j in range(sub):
                                tt = (k + j / sub) / fps
                                pg.evaluate("(a) => window.__setT(...a)", [tt, g + tt, durs[i], exit_, wipe_in, push])
                                im = Image.open(io.BytesIO(pg.screenshot(type="jpeg", quality=96))).convert("RGB")
                                acc = im if acc is None else Image.blend(acc, im, 1 / (j + 1))
                            buf = io.BytesIO()
                            acc.save(buf, "JPEG", quality=93)
                            proc.stdin.write(buf.getvalue())
                        g += nf / fps
                        t_start += nf / fps
                produced[(post["id"], fmt)] = files
                if anim:
                    proc.stdin.close()
                    if proc.wait() != 0:
                        raise RuntimeError(f"ffmpeg nie złożył {mp4}")
                    animated[post["id"]] = mp4
                    with open(os.path.join(out, f"{post['id']}_zdarzenia.json"), "w", encoding="utf-8") as fh:
                        json.dump({"dlugosc": round(t_start, 3), "plansze": [round(d, 3) for d in durs], "bpm": bpm,
                                   "przedmiot": post.get("subject", ""), "nastroj": ruch.nastroj(post),
                                   "efekty": fxs, "zdarzenia": sorted(events, key=lambda e: e["t"])},
                                  fh, ensure_ascii=False, indent=1)
        br.close()
    with open(os.path.join(out, "qa_report.txt"), "w") as fh:
        fh.write("\n".join(report) + "\n")
    return produced, report, animated


# ───────────────────────── wideo (Reelsy) ─────────────────────────
def make_video(files, durations, out_mp4, trans=0.28):
    if not durations or len(durations) != len(files):
        durations = default_durations(len(files))
    inp = []
    for im, d in zip(files, durations):
        inp += ["-loop", "1", "-t", f"{d + trans:.2f}", "-framerate", "30", "-i", im]
    total = sum(durations) + trans
    inp += ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo"]
    chain, prev, off = [], "[0:v]", 0.0
    # delikatny „oddech” pierwszej planszy (zoom 1.00→1.03), żeby haczyk nie był martwą klatką
    chain.append(f"[0:v]scale=1080:1920,zoompan=z='min(1+0.0009*on,1.03)':d=1:x='iw/2-(iw/zoom/2)':"
                 f"y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30[z0]")
    prev = "[z0]"
    for k in range(1, len(files)):
        off += durations[k - 1]
        tr = "slideleft" if k % 2 else "fade"
        chain.append(f"{prev}[{k}:v]xfade=transition={tr}:duration={trans}:offset={off:.2f}[v{k}]")
        prev = f"[v{k}]"
    chain.append(f"{prev}format=yuv420p[vo]")
    cmd = ["ffmpeg", "-y", "-v", "error", *inp, "-filter_complex", ";".join(chain), "-map", "[vo]",
           "-map", f"{len(files)}:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", "30",
           "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out_mp4]
    subprocess.run(cmd, check=True)
    return out_mp4


def contact_sheet(files, out, cols=8, w=270):
    ims = [Image.open(f) for f in files]
    h = int(w * ims[0].height / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (w * min(cols, len(ims)), h * rows), (20, 20, 20))
    for k, im in enumerate(ims):
        sheet.paste(im.resize((w, h)), ((k % cols) * w, (k // cols) * h))
    sheet.save(out, quality=88)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out", default="out")
    ap.add_argument("--sheet", action="store_true", help="podgląd zbiorczy każdego posta (do kontroli Read)")
    ap.add_argument("--video", action="store_true", help="złóż MP4 dla postów 'reel'")
    ap.add_argument("--draft", action="store_true", help="szybki podgląd wideo bez rozmycia ruchu (do sprawdzania układu)")
    ap.add_argument("--muzyka", action="store_true",
                    help="po złożeniu wideo dodaj oryginalny podkład i efekty dźwiękowe (skill szkola-klamala-animacje)")
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    produced, report, animated = render_all(spec, a.out, video=a.video, sub=1 if a.draft else 2)
    for (pid, fmt), files in produced.items():
        if a.sheet:
            contact_sheet(files, os.path.join(a.out, f"_podglad_{pid}_{fmt}.jpg"))
        if pid in animated and fmt == "reel":
            print("MP4 (animowane napisy):", animated[pid])
            if a.muzyka:
                muz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                   "szkola-klamala-animacje", "scripts", "muzyka.py")
                subprocess.run([sys.executable, muz, animated[pid]], check=True)
        elif a.video and fmt == "reel":
            post = next(p for p in spec["posts"] if p["id"] == pid)
            mp4 = make_video(files, post.get("durations"), os.path.join(a.out, f"{pid}.mp4"))
            print("MP4:", mp4)
    warn = [r for r in report if "⚠" in r]
    print("\n".join(report))
    print(f"\nQA: {len(report)} slajdów, ostrzeżeń: {len(warn)} (szczegóły: {a.out}/qa_report.txt)")
    sys.exit(0)


if __name__ == "__main__":
    main()
