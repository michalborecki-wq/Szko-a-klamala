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
import base64
import html
import math
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
.content.hook h1{{font-size:{int(f['h1']*1.35)}px;line-height:.98}}
.content.hook .sub{{font-weight:700}}
.content.withhero{{justify-content:flex-start;padding-top:{HERO_H + 20}px}}
.content.withhero > .chip{{margin-top:auto}}
.content.withhero h1{{font-size:{int(f['h1']*1.15)}px}}
body.zolty{{background:{TOK['yellow']}}}
body.zolty .bg{{background:radial-gradient(ellipse 85% 60% at 50% 38%,#FFD95A 0%,{TOK['yellow']} 70%)}}
body.zolty .st,body.zolty .orb,body.zolty .fxbg canvas{{display:none}}
body.zolty .vig{{background:radial-gradient(ellipse at 50% 50%,transparent 60%,rgba(120,80,0,.22) 100%)}}
body.zolty .kontur{{-webkit-text-stroke:3px rgba(10,14,24,.10)}}
body.zolty h1{{color:{TOK['bg0']};text-shadow:0 7px 0 rgba(10,14,24,.16)}}
body.zolty h1 .y{{color:#C62828;text-shadow:0 7px 0 rgba(10,14,24,.16)}}
body.zolty .sub{{color:{TOK['bg0']}}} body.zolty .hd{{color:{TOK['bg0']}}}
body.zolty .chip{{background:{TOK['bg0']};color:{TOK['yellow']}}}
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

.tl-y{{display:block;font-family:'Inter Display','Inter';font-weight:900;font-style:italic;font-size:{int(f['big']*0.42)}px;
  line-height:1;color:{TOK['yellow']};text-shadow:0 5px 0 {TOK['blue']};margin-bottom:6px}}
.tl-t{{display:block;font-size:{int(f['body']*0.92)}px;line-height:1.3;color:{TOK['text']}}}
.tl-t b{{color:{TOK['yellow']};font-weight:800}}
.q-txt{{font-family:'Inter Display','Inter';font-weight:800;font-style:italic;font-size:{int(f['h2']*0.82)}px;line-height:1.18;
  color:#fff;margin:6px 0 26px;text-wrap:balance}}
.q-txt b{{color:{TOK['yellow']}}}
.q-who{{font-size:{f['note']}px;color:{TOK['muted']};font-weight:700;letter-spacing:.5px}}
.q-who:before{{content:'';display:inline-block;width:46px;height:4px;background:{TOK['yellow']};vertical-align:middle;margin-right:14px}}

.doc{{position:relative;background:linear-gradient(180deg,#F4F6FB,#E3E8F2);color:#121826;border-radius:14px;padding:0 0 34px;
  box-shadow:0 40px 90px rgba(0,0,0,.55),0 0 0 2px rgba(47,107,255,.35);transform-origin:50% 0;overflow:hidden}}
.doc-h{{background:{TOK['blue']};color:#fff;font-family:'Inter Display','Inter';font-weight:900;font-style:italic;
  font-size:{int(f['note']*1.05)}px;letter-spacing:1px;padding:16px 30px 14px;text-transform:uppercase}}
.doc-t{{font-family:Georgia,'Times New Roman',serif;font-size:{int(f['body']*0.98)}px;line-height:1.42;padding:28px 34px 0}}
.doc-t b{{font-weight:700;color:#121826}}
.doc-wsk{{align-self:flex-end;margin:120px 10px 0 0;position:relative;z-index:5}}
.doc-wsk span{{display:inline-block;background:{TOK['yellow']};color:{TOK['bg0']};font-family:'Inter Display','Inter';font-weight:900;
  font-style:italic;font-size:{int(f['body']*1.05)}px;line-height:1.1;padding:14px 26px 12px;border-radius:10px;transform:skew(-8deg);
  text-transform:uppercase;box-shadow:0 10px 0 {TOK['blue']},0 0 40px rgba(255,199,39,.45)}}
.doc-l{{height:10px;margin:14px 34px 0;border-radius:5px;background:rgba(18,24,38,.10)}}

.wyc{{background:#F2EEE3;background-image:repeating-linear-gradient(0deg,transparent 0 46px,rgba(18,24,38,.05) 46px 48px);
  border-radius:0;padding:0 0 30px;margin:0 26px;rotate:-1.6deg;overflow:visible;box-shadow:0 40px 90px rgba(0,0,0,.6);
  clip-path:polygon(0 1.5%,4% 0,9% 1.2%,15% .2%,22% 1.4%,30% .3%,38% 1.1%,47% 0,55% 1.3%,63% .2%,71% 1.2%,79% .1%,87% 1.4%,94% .2%,100% 1%,
    100% 98.6%,95% 100%,88% 98.8%,80% 99.8%,72% 98.7%,64% 99.9%,56% 98.6%,48% 99.8%,40% 98.9%,32% 100%,24% 98.7%,16% 99.8%,8% 98.8%,0 99.6%)}}
.wyc:before{{content:'';position:absolute;left:50%;top:-16px;width:190px;height:44px;margin-left:-95px;rotate:3deg;
  background:rgba(255,199,39,.55);box-shadow:0 2px 6px rgba(0,0,0,.2)}}
.wyc-k{{font-family:'Inter';font-weight:700;letter-spacing:2px;color:#5B6170;
  font-size:{int(f['note']*0.8)}px;padding:34px 36px 0;text-transform:uppercase}}
.wyc .wyc-t{{font-family:Georgia,'Times New Roman',serif;font-weight:700;font-size:{int(f['body']*1.25)}px;line-height:1.2;
  padding:16px 36px 0;color:#121826}}
.wyc-tl{{font-size:{int(f['note']*0.95)}px;color:#5B6170;padding:14px 36px 0;font-style:italic}}

.foto{{position:relative;align-self:center;width:86%;aspect-ratio:4/5;max-height:62%;background:#F4F1EA;padding:18px 18px 18px;
  rotate:1.2deg;box-shadow:0 40px 90px rgba(0,0,0,.6);overflow:hidden}}
.foto:before{{content:'';position:absolute;left:50%;top:-12px;width:170px;height:40px;margin-left:-85px;rotate:-3deg;z-index:3;
  background:rgba(255,199,39,.55)}}
.foto-in{{position:relative;width:100%;height:100%;overflow:hidden;background:#0A0E18}}
.foto-b,.foto-f{{position:absolute;inset:0;background-size:cover;background-position:center}}
.foto-b{{filter:blur(14px) brightness(.75);transform-origin:50% 50%}}
.foto-f{{-webkit-mask-image:radial-gradient(ellipse 72% 78% at 50% 48%,#000 62%,transparent 100%);
  mask-image:radial-gradient(ellipse 72% 78% at 50% 48%,#000 62%,transparent 100%)}}
.foto-f.cala{{background-size:contain;background-repeat:no-repeat;-webkit-mask-image:none;mask-image:none}}
.foto-pod{{font-size:{int(f['note']*0.8)}px;color:{TOK['muted']};margin-top:22px;font-weight:600;letter-spacing:.3px}}
.foto-pod.ai{{display:inline-block;color:{TOK['bg0']};background:{TOK['yellow']};padding:8px 14px;border-radius:8px;font-weight:800}}
.fpel{{position:absolute;inset:0;z-index:3;overflow:hidden;pointer-events:none}}
.fpel .foto-b,.fpel .foto-f{{inset:-6%}}
.fpel:after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,14,24,.55) 0%,rgba(10,14,24,.05) 30%,
  rgba(10,14,24,.25) 55%,rgba(10,14,24,.92) 80%,#0A0E18 100%)}}
.content.napelnym{{justify-content:flex-end}}
.mapa{{position:relative;margin:10px 0 18px;flex-shrink:1;min-height:0}}
.mapa-svg{{display:block;max-height:880px;overflow:visible}}
.mapa-svg .obs{{fill:rgba(47,107,255,.16);stroke:{TOK['blue']};stroke-width:2.4;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:0}}
.mapa-svg .obs.wyr{{fill:{TOK['yellow']};stroke:{TOK['yellow']}}}
.mapa-svg .pk-d{{fill:{TOK['red']};stroke:#fff;stroke-width:5}}
.mapa-svg .pk-r{{fill:none;stroke:{TOK['red']};stroke-width:5;opacity:.7}}
.mapa-svg text{{font-family:'Inter Display','Inter';font-weight:900;font-style:italic;font-size:44px;fill:#fff;
  paint-order:stroke;stroke:{TOK['bg0']};stroke-width:10px;stroke-linejoin:round}}

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


# ───────────────────────── wycinki agencji i zdjęcia na wolnych licencjach (decyzja Michała 9.11) ─────────────────────────
REPO = __import__("pathlib").Path(__file__).resolve().parents[4]
LIC_OK = ("CC0", "PUBLIC DOMAIN", "DOMENA PUBLICZNA", "PD", "CC BY", "CC-BY", "CC BY-SA", "CC-BY-SA", "NASA")


def licencja_ok(lic: str) -> bool:
    """Tylko CC0, domena publiczna, CC BY, CC BY-SA. NC i ND odrzucamy (konto ma sponsorów, zdjęcie przycinamy)."""
    u = (lic or "").upper().replace("‑", "-")
    if re.search(r"\bNC\b|\bND\b|NON-?COMMERCIAL|NO-?DERIV", u):
        return False
    return any(k in u for k in LIC_OK)


def foto_dane(s):
    """Ścieżka zdjęcia + metadane (z <slug>.json obok pliku albo z pól planszy). Brak licencji/autora/źródła = błąd."""
    p = __import__("pathlib").Path(s["zdjecie"])
    if not p.is_absolute():
        p = REPO / p
    if not p.exists():
        raise ValueError(f"foto: brak pliku zdjęcia {p}")
    meta = {}
    mj = p.with_suffix(".json")
    if mj.exists():
        meta = json.load(open(mj, encoding="utf-8"))
    for k in ("autor", "licencja", "zrodlo", "serwis"):
        if s.get(k):
            meta[k] = s[k]
    if s.get("ilustracja_ai"):
        return p, meta
    brak = [k for k in ("autor", "licencja", "zrodlo") if not meta.get(k)]
    if brak:
        raise ValueError(f"foto {p.name}: brak {', '.join(brak)} – bez pełnych danych licencji zdjęcia nie używamy")
    if not licencja_ok(meta["licencja"]):
        raise ValueError(f"foto {p.name}: licencja „{meta['licencja']}” niedozwolona (tylko CC0, domena publiczna, CC BY, CC BY-SA; bez NC/ND)")
    return p, meta


def foto_uri(p, max_h=2400):
    im = Image.open(p).convert("RGB")
    if im.height > max_h:
        im = im.resize((int(im.width * max_h / im.height), max_h), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode(), Image.open(p).size


def wycinek_waliduj(s):
    brak = [k for k in ("agencja", "data", "naglowek", "link") if not s.get(k)]
    if brak:
        raise ValueError(f"wycinek: brak pól {', '.join(brak)} (agencja, data, dosłowny nagłówek i link do artykułu są obowiązkowe)")
    n = len(re.sub(r"\*\*", "", s["naglowek"]).split())
    if n > 20:
        raise ValueError(f"wycinek: nagłówek ma {n} słów (> 20) – prawo cytatu: krótki, dosłowny fragment")


# ───────────────────────── mapy z prawdziwych konturów (Natural Earth, domena publiczna) ─────────────────────────
MAPY_BBOX = {"polska": (13.9, 24.3, 48.9, 55.0), "europa": (-12.0, 42.0, 34.0, 71.5), "swiat": (-170.0, 190.0, -58.0, 84.0)}


def mapa_svg(s, W=840, Hmax=900):
    """SVG mapy: obszary (województwa albo państwa), wyróżnienia i punkty z PRAWDZIWYMI współrzędnymi (lat/lon)."""
    rodzaj = s.get("mapa", "polska")
    if rodzaj not in MAPY_BBOX:
        raise ValueError(f"mapa: nieznany rodzaj „{rodzaj}” (polska | europa | swiat)")
    lon0, lon1, lat0, lat1 = s.get("zakres") or MAPY_BBOX[rodzaj]
    if rodzaj == "polska":
        obs = json.load(open(REPO / "zrodla/mapy/polska_wojewodztwa.json", encoding="utf-8"))["obszary"]
    else:
        sw = json.load(open(REPO / "zrodla/mapy/swiat_panstwa.json", encoding="utf-8"))["panstwa"]
        obs = {k: v["obszary"] for k, v in sw.items()}
    kx = math.cos(math.radians((lat0 + lat1) / 2)) if rodzaj != "swiat" else 1.0
    sx = W / ((lon1 - lon0) * kx)
    H = min(Hmax, (lat1 - lat0) * sx)
    sc = min(sx, H / (lat1 - lat0))
    ox = (W - (lon1 - lon0) * kx * sc) / 2
    P = lambda lon, lat: (ox + (lon - lon0) * kx * sc, (lat1 - lat) * sc)
    wyr = {w.lower() if rodzaj == "polska" else w.upper() for w in s.get("wyroznij", [])}
    znane = {k.lower() if rodzaj == "polska" else k for k in obs}
    brak = [w for w in wyr if w not in znane]
    if brak:
        raise ValueError(f"mapa: nie ma obszaru {brak} (polska: nazwy województw, np. „mazowieckie”; świat/europa: kody ISO A2, np. „PL”)")
    pathy = []
    for k, rings in obs.items():
        kk = k.lower() if rodzaj == "polska" else k
        dd = []
        for r in rings:
            if not any(lon0 - 5 <= x <= lon1 + 5 and lat0 - 5 <= y <= lat1 + 5 for x, y in r):
                continue
            pts = [P(x, y) for x, y in r]
            dd.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
        if dd:
            pathy.append(f"<path class='obs{' wyr' if kk in wyr else ''}' pathLength='1' d='{''.join(dd)}'/>")
    pk = ""
    for i, p in enumerate(s.get("punkty", [])):
        if "lat" not in p or "lon" not in p:
            raise ValueError("mapa: punkt bez współrzędnych lat/lon – współrzędne tylko ze źródła (GeoNames, Wikipedia), nigdy „na oko”")
        if not (lon0 <= p["lon"] <= lon1 and lat0 <= p["lat"] <= lat1):
            raise ValueError(f"mapa: punkt {p.get('nazwa')} ({p['lat']}, {p['lon']}) poza zakresem mapy {rodzaj}")
        x, y = P(p["lon"], p["lat"])
        lab = html.escape(p.get("nazwa", ""))
        anchor = "end" if x > W * .62 else "start"
        dx = -30 if anchor == "end" else 30
        pk += (f"<g class='pkt' style='transform-origin:{x:.1f}px {y:.1f}px'><circle class='pk-r' cx='{x:.1f}' cy='{y:.1f}' r='34'/>"
               f"<circle class='pk-d' cx='{x:.1f}' cy='{y:.1f}' r='15'/>"
               + (f"<text x='{x + dx:.1f}' y='{y + 12:.1f}' text-anchor='{anchor}'>{lab}</text>" if lab else "") + "</g>")
    return (f"<svg class='mapa-svg' viewBox='-20 -20 {W + 40} {H + 40:.0f}' width='100%' preserveAspectRatio='xMidYMid meet'>"
            f"<defs><clipPath id='mapaclip'><rect x='0' y='0' width='{W}' height='{H:.0f}' rx='18'/></clipPath></defs>"
            f"<g class='obsy' clip-path='url(#mapaclip)'>{''.join(pathy)}</g>{pk}</svg>")


def tpl(s, post, f, i, n):
    t = s["type"]
    label = f"{post.get('series','SZKOŁA KŁAMAŁA')} · {post.get('subject','')}".strip(" ·")
    title, accent = head(s)
    src = f"<div class='src'>{rich(s['source'])}</div>" if s.get("source") else ""
    note = f"<div class='note'>{rich(s['note'])}</div>" if s.get("note") else ""
    cls = ""

    if t == "cover":
        hero = ""
        if post.get("_fmt") == "reel":
            cls = "hook"      # haczyk rolki: największy krój (wyniki 1.11 – widzowie odpadają w 1–2 s)
            if s.get("obraz"):  # obraz-bohater nad haczykiem (analiza w Canvie 1.11: pierwsza klatka musi mieć co oglądać)
                import obrazy
                hero = obrazy.html(s["obraz"], s.get("obraz_opcje"), HERO_H, s.get("pieczatka"))
                cls = "hook withhero"
        b = (hero +f"<div class='chip'>{html.escape(label)}</div>"
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
    elif t == "timeline":
        # oś czasu: "items": [{"rok": "1610", "tekst": "…"}, …] (2–4 punkty) – linia rysuje się, punkty wskakują po kolei
        tag = f"<div class='tag t-{s['tag'].lower()}'>{html.escape(s['tag'])}</div>" if s.get("tag") else ""
        its = "".join(f"<div class='tl-it'><span class='tl-dot'></span><span class='tl-y'>{rich(it['rok'])}</span>"
                      f"<span class='tl-t'>{rich(it['tekst'])}</span></div>" for it in s["items"])
        b = (f"{tag}" + (f"<h2>{title} <span class='y'>{accent}</span></h2>" if title or accent else "")
             + f"<div class='tl'><div class='tl-line'></div>{its}</div>{note}{src}")
    elif t == "dokument":
        # odsłonięcie dokumentu: DOSŁOWNY fragment aktu prawnego / dokumentu (nie fikcyjny zrzut ekranu);
        # "naglowek": nazwa i jednostka aktu, "tekst": cytat z **wyróżnieniem**, "linie": ile szarych linii kontekstu (0–3)
        tag = f"<div class='tag t-{s['tag'].lower()}'>{html.escape(s['tag'])}</div>" if s.get("tag") else ""
        ln = "".join("<div class='doc-l' style='width:%d%%'></div>" % w for w in (88, 72, 80)[:int(s.get("linie", 2))])
        b = (f"{tag}" + (f"<h2>{title} <span class='y'>{accent}</span></h2>" if title or accent else "")
             + f"<div class='doc'><div class='doc-h'>{rich(s['naglowek'])}</div>"
             f"<div class='doc-t' data-fit>{rich(s['tekst'])}</div>{ln}</div>"
             # "wskaz": krótka etykieta (2–4 słowa) – linia łączy ją z wyróżnieniem (wskazanie szczegółu, DVE 9.11)
             + (f"<div class='doc-wsk'><span>{rich(s['wskaz'])}</span></div>" if s.get("wskaz") else "")
             + f"{note}{src}")
    elif t == "wycinek":
        # wycinek agencji (PAP – Polska, Reuters – świat): NASZA plansza z dosłownym, krótkim nagłówkiem (prawo cytatu, art. 29 pr. aut.),
        # nazwa agencji zwykłym tekstem + data; bez logo i layoutu agencji, to nie jest „zrzut ekranu”. Link idzie do opisu.
        wycinek_waliduj(s)
        tag = f"<div class='tag t-{s['tag'].lower()}'>{html.escape(s['tag'])}</div>" if s.get("tag") else ""
        tl = f"<div class='wyc-tl'>tłum. red.: {rich(s['tlumaczenie'])}</div>" if s.get("tlumaczenie") else ""
        src = f"<div class='src'>{rich(s.get('source') or ('Źródło: ' + s['agencja'] + ', ' + s['data']))}</div>"
        b = (f"{tag}" + (f"<h2>{title} <span class='y'>{accent}</span></h2>" if title or accent else "")
             + f"<div class='doc wyc'><div class='wyc-k'>Nagłówek · {html.escape(s['agencja'])} · {html.escape(s['data'])}</div>"
             f"<div class='doc-t wyc-t' data-fit>„{rich(s['naglowek'])}”</div>{tl}</div>"
             + (f"<div class='doc-wsk'><span>{rich(s['wskaz'])}</span></div>" if s.get("wskaz") else "")
             + f"{note}{src}")
    elif t == "foto":
        # zdjęcie na wolnej licencji (CC0 / domena publiczna / CC BY / CC BY-SA) z podpisem autora i licencji;
        # "uklad": "ramka" (odbitka z taśmą) albo "pelny" (pełny kadr z paralaksą, zdjęcie min. ok. 1600 px wysokości)
        p, meta = foto_dane(s)
        uri, (pw, ph) = foto_uri(p)
        uk = s.get("uklad", "ramka")
        # CC BY-SA: przycięcie, rozmycie i powiększenie to przeróbka, która musiałaby iść na tej samej licencji –
        # pokazujemy zdjęcie w całości (bez kadrowania i bez rozmytej warstwy), tylko w ramce
        sa = bool(re.search(r"\bSA\b|SHARE-?ALIKE", (meta.get("licencja") or "").upper()))
        if sa and uk == "pelny":
            print(f"  ⚠ foto {p.name}: licencja {meta['licencja']} – pełny kadr przycina zdjęcie, używam „ramka” (całe zdjęcie)")
            uk = "ramka"
        if uk == "pelny" and ph < 1600:
            print(f"  ⚠ foto {p.name}: {pw}×{ph} px – za mało na pełny kadr, używam układu „ramka”")
            uk = "ramka"
        if s.get("ilustracja_ai"):
            pod = "<div class='foto-pod ai'>Ilustracja – nie jest zdjęciem wydarzenia</div>"
        else:
            pod = (f"<div class='foto-pod'>Fot. {html.escape(meta['autor'])} · {html.escape(meta['licencja'])}"
                   + (f" · {html.escape(meta['serwis'])}" if meta.get("serwis") else "") + "</div>")
        if sa:
            warstwy = f"<div class='foto-f cala' style=\"background-image:url('{uri}');\"></div>"
        else:
            warstwy = f"<div class='foto-b' style=\"background-image:url('{uri}')\"></div><div class='foto-f' style=\"background-image:url('{uri}')\"></div>"
        tag = f"<div class='tag t-{s['tag'].lower()}'>{html.escape(s['tag'])}</div>" if s.get("tag") else ""
        tekst = ((f"<h2 data-fit>{title} <span class='y'>{accent}</span></h2>" if title or accent else "")
                 + (f"<div class='body' data-fit>{rich(s['body'])}</div>" if s.get("body") else ""))
        if uk == "pelny":
            cls = "napelnym"
            s["_pelny"] = f"<div class='fpel'>{warstwy}</div>"
            b = f"{tag}{tekst}{pod}{note}{src}"
        else:
            styl = f" style='aspect-ratio:{pw}/{ph}'" if sa else ""
            b = f"{tag}<div class='foto'{styl}><div class='foto-in'>{warstwy}</div></div>{tekst}{pod}{note}{src}"
    elif t == "mapa":
        # mapa z konturów Natural Earth; "wyroznij": województwa / kody ISO; "punkty": [{"nazwa","lat","lon"}] ze źródła
        tag = f"<div class='tag t-{s['tag'].lower()}'>{html.escape(s['tag'])}</div>" if s.get("tag") else ""
        src = f"<div class='src'>{rich(s.get('source') or 'Mapa: Natural Earth')}</div>"
        b = (f"{tag}" + (f"<h2>{title} <span class='y'>{accent}</span></h2>" if title or accent else "")
             + f"<div class='mapa'>{mapa_svg(s)}</div>"
             + (f"<div class='body' data-fit>{rich(s['body'])}</div>" if s.get("body") else "") + f"{note}{src}")
    elif t == "quote":
        # cytat: TYLKO dosłowny tekst ze źródła (ustawa, dokument, wypowiedź z nagrania) – "kto": autor/akt
        tag = f"<div class='tag t-{s['tag'].lower()}'>{html.escape(s['tag'])}</div>" if s.get("tag") else ""
        b = (f"{tag}<div class='q-mark'>„</div><div class='q-txt' data-fit>{rich(s['cytat'])}</div>"
             f"<div class='q-who'>{rich(s.get('kto',''))}</div>{note}{src}")
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

    body_cls = " class='zolty'" if (t == "cover" and s.get("uklad") == "zolty") else ""
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css(f)}</style></head><body{body_cls}>"
            f"<div class='bg'></div><div class='st a'></div><div class='st a2'></div><div class='st b'></div>"
            f"<div class='st b2'></div><div class='vig'></div><div class='grain'></div>{s.pop('_pelny', '')}"
            f"{top}<div class='content {cls}'>{b}</div>{bot}</body></html>")


# ───────────────────────── autodopasowanie + QA w przeglądarce ─────────────────────────
FIT_AND_QA = """
(minBody) => {
  const c = document.querySelector('.content');
  const over = () => c.scrollHeight > c.clientHeight + 1 || c.scrollWidth > c.clientWidth + 1;
  // 0) duże liczby dopasuj najpierw do szerokości – osobno, żeby nie zmniejszać przez nie reszty tekstu
  c.querySelectorAll('.big, .hook h1').forEach(el => {   // też wielki nagłówek haczyka rolki
    let fs = parseFloat(getComputedStyle(el).fontSize), g = 0;
    while (el.scrollWidth > c.clientWidth && g++ < 60) { fs *= 0.97; el.style.fontSize = fs + 'px'; }
  });
  // 1) zmniejszaj całą treść małymi krokami, aż się zmieści (nie poniżej minimum czytelności)
  let scale = 1, guard = 0;
  while (over() && guard++ < 40) {
    scale *= 0.96;
    c.querySelectorAll('h1,h2,.body,.sub,.myth,.opt,.big,.num,.cd,.row,.tl-y,.tl-t,.q-txt,.q-mark,.doc-t,.doc-h,.wyc-k').forEach(el => {
      const base = parseFloat(el.dataset.base || getComputedStyle(el).fontSize);
      el.dataset.base = base;
      el.style.fontSize = (base * scale) + 'px';
    });
  }
  const issues = [];
  if (over()) issues.push('TREŚĆ NIE MIEŚCI SIĘ w strefie bezpiecznej – skróć tekst');
  // 2) minimalna czytelność tekstu ciągłego
  c.querySelectorAll('.body,.sub,.myth,.opt,.tl-t,.q-txt,.doc-t').forEach(el => {
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < minBody) issues.push(`czcionka ${fs.toFixed(0)}px < ${minBody}px (${el.className}) – skróć tekst`);
  });
  // 3) nic nie wystaje poza płótno
  const W = innerWidth, H = innerHeight;
  c.querySelectorAll('*').forEach(el => {
    if (el.closest('.hero-ill')) return;               // ilustracja jest przycinana do swojego pola
    const r = el.getBoundingClientRect();
    if (r.width && (r.right > W + 1 || r.left < -1 || r.bottom > H + 1)) issues.push('element poza kadrem: ' + el.tagName);
  });
  // 4) liczba słów na slajd (czytelność w ruchu)
  const cl = c.cloneNode(true);                       // bez kopii do połysku i kolumn cyfr licznika
  cl.querySelectorAll('.sheen,.col,style,svg').forEach(e => e.remove());   // obraz-bohater i jego CSS to nie tekst
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


# standard rolki (decyzja Michała 29.10): co najmniej 4 plansze i 20 s
REEL_MIN_SLIDES, REEL_MIN_SEC = 4, 20.0


def default_durations(n):
    return [2.6] + [4.2] * (n - 2) + [3.8] if n > 1 else [4.0]


# czas czytania: tyle musi stać tekst po wejściu, żeby przeczytać CAŁOŚĆ planszy (z etykietą i źródłem)
# Czytanie zaczyna się już w trakcie wjeżdżania słów, więc liczy się późniejsze z dwóch: koniec wejścia + 1,2 s
# na doczytanie ostatnich słów albo pełny czas czytania całości (0,3 s/słowo ≈ tempo napisów ekranowych).
SEK_NA_SLOWO, ZAPAS_CZYTANIA, MAX_SLOW_ROLKA, MAX_SLOW_OUTRO = 0.30, 0.6, 12, 18
HERO_H = 600         # wysokość obrazu-bohatera na okładce rolki (px w układzie 1080)
REEL_CEL_SEC = 29.2   # szablon B: 25–32 s z logo (2,8 s) → maks. ok. 29 s treści; dłużej spada odsetek obejrzeń


def render_all(spec, out, video=False, fps=30, sub=2, scale=2):
    """scale=2 → pliki w 4K (2160×3840 dla 9:16, 2160×2700 dla 4:5) przy niezmienionym układzie 1080 px CSS."""
    from playwright.sync_api import sync_playwright
    os.makedirs(out, exist_ok=True)
    report, produced, animated = [], {}, {}
    handle = spec.get("handle", "@szkola_klamala")
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(device_scale_factor=scale)
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
                    t3d = Tlo3D(post["tlo3d"]) if post.get("tlo3d") else None
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
                        if t3d:
                            t3d.last = None                 # nowa strona – obraz trzeba wczytać od nowa
                            t3d.ustaw(pg, g + min(2.0, durs[i] * .5))
                        pg.evaluate("window.__setT(60, 0, 999, null, null, false)")
                    qa = pg.evaluate(FIT_AND_QA, f["min_body"])
                    if anim:
                        pg.evaluate("window.__layout()")   # pozycje iskier po dopasowaniu tekstu
                        if enter:
                            # plansza stoi tak długo, żeby przeczytać całość: wejście napisów + czas czytania + zapas
                            need = max((0 if i == 0 else intro) + 1.2, qa["words"] * SEK_NA_SLOWO + 0.4) + ZAPAS_CZYTANIA
                            if i < n - 1:
                                need += 0.25          # ostatnie ćwierć sekundy zabiera przejście
                            if need > durs[i] + 1e-6:
                                old = durs[i]
                                durs[i] = (math.ceil(need / beat - 1e-6) * beat) if bpm else round(need, 2)
                                qa.setdefault("notes", []).append(f"wydłużono {old:.1f}→{durs[i]:.1f} s (czytanie)")
                            qa["czytanie"] = round(need, 1)
                    words_max = 40 if s["type"] in ("quiz", "versus") else 32
                    if fmt == "reel" and s["type"] != "quiz":
                        # w rolce każde słowo kosztuje 0,3 s – krótko i konkretnie (skill szkola-klamala-viral)
                        words_max = MAX_SLOW_OUTRO if s["type"] == "outro" else MAX_SLOW_ROLKA
                    if qa["words"] > words_max:
                        qa["issues"].append(f"{qa['words']} słów (> {words_max}) – za dużo tekstu na slajd")
                    name = f"{post['id']}{suffix}_{i+1:02d}.jpg"
                    path = os.path.join(out, name)
                    png = path[:-4] + ".png"
                    pg.screenshot(path=png)
                    Image.open(png).convert("RGB").save(path, "JPEG", quality=93, optimize=True, subsampling=0)
                    os.remove(png)
                    files.append(path)
                    tagline = f"{name}: słowa={qa['words']} skala={qa['scale']}" + (
                        f" czytanie={qa['czytanie']}s plansza={durs[i]:.1f}s" if anim and "czytanie" in qa else "") + (
                        " (" + "; ".join(qa["notes"]) + ")" if qa.get("notes") else "")
                    report.append(tagline + ("" if not qa["issues"] else "  ⚠ " + " | ".join(qa["issues"])))
                    if anim:
                        nf = round(durs[i] * fps)
                        exit_ = fxs[i + 1]["przejscie"] if i < n - 1 and not cont[i + 1] else None
                        wipe_in = fxs[i]["przejscie"] if i > 0 and not cont[i] else None
                        push = not cont[i] and not (i + 1 < n and cont[i + 1])   # quiz stoi w miejscu
                        hits = [e["t"] for e in res["ev"] if e["typ"] in ("uderzenie", "pieczatka", "start")]
                        for k in range(nf):
                            tk = k / fps
                            # rozmycie ruchu (średnia z `sub` podklatek) tylko tam, gdzie coś szybko się rusza:
                            # wejścia napisów, przejścia, uderzenia; w czasie czytania – pojedyncza klatka (4K jest kosztowne)
                            fast = (enter and tk < intro + .7) or (exit_ and tk > durs[i] - .35) or \
                                (wipe_in and tk < .35) or any(-.05 < tk - h < .55 for h in hits) or \
                                (cont[i] and tk < .6)
                            if t3d:
                                t3d.ustaw(pg, g + tk)
                            if sub == 1 or not fast:
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
                if fmt == "reel":
                    total = sum(durs) if anim else sum(post.get("durations") or default_durations(n))
                    if total > REEL_CEL_SEC + 0.05:
                        report.append(f"{post['id']}: {total:.1f} s  ⚠ ponad {REEL_CEL_SEC:.0f} s – skróć tekst albo usuń planszę"
                                      " (szablon B: 25–32 s z logo, skill szkola-klamala-viral)")
                    if n < REEL_MIN_SLIDES or total < REEL_MIN_SEC - 0.05:
                        report.append(f"{post['id']}: {n} plansz, {total:.1f} s  ⚠ rolka ma mieć min. {REEL_MIN_SLIDES} plansze"
                                      f" i {REEL_MIN_SEC:.0f} s – dodaj planszę (np. drugi fakt, „jak to sprawdzono”, outro)")
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


class Tlo3D:
    """Tło z renderu 3D (skill szkola-klamala-3d): katalog klatek JPEG, klatka wybierana z czasu globalnego rolki.

    W poście: "tlo3d": {"klatki": "ścieżka/do/klatek", "fps": 30, "krycie": 0.85}. Klatki skalowane do 4K w przeglądarce.
    """
    def __init__(self, cfg):
        import glob as _g
        self.files = sorted(_g.glob(os.path.join(cfg["klatki"], "*.jpg")))
        if not self.files:
            raise RuntimeError(f"tlo3d: brak klatek JPEG w {cfg['klatki']}")
        self.fps, self.op, self.last = cfg.get("fps", 30), cfg.get("krycie", 0.85), None

    def ustaw(self, pg, g):
        k = min(len(self.files) - 1, max(0, int(round(g * self.fps))))
        if k == self.last:
            return
        with open(self.files[k], "rb") as fh:
            src = "data:image/jpeg;base64," + base64.b64encode(fh.read()).decode()
        pg.evaluate("(a) => window.__t3d(a[0], a[1])", [src, self.op])
        self.last = k


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
    w, h = Image.open(files[0]).size        # 4K albo 1080p – zgodnie z rozdzielczością plansz
    chain.append(f"[0:v]scale={w}:{h},zoompan=z='min(1+0.0009*on,1.03)':d=1:x='iw/2-(iw/zoom/2)':"
                 f"y='ih/2-(ih/zoom/2)':s={w}x{h}:fps=30[z0]")
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
    ap.add_argument("--draft", action="store_true",
                    help="szybki podgląd wideo w 1080p bez rozmycia ruchu (do sprawdzania układu, nie do publikacji)")
    ap.add_argument("--hd", action="store_true", help="pliki w 1080p zamiast domyślnego 4K")
    ap.add_argument("--muzyka", action="store_true",
                    help="po złożeniu wideo dodaj oryginalny podkład i efekty dźwiękowe (skill szkola-klamala-animacje)")
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    produced, report, animated = render_all(spec, a.out, video=a.video, sub=1 if a.draft else 2,
                                            scale=1 if (a.draft or a.hd) else 2)
    for (pid, fmt), files in produced.items():
        if a.sheet:
            contact_sheet(files, os.path.join(a.out, f"_podglad_{pid}_{fmt}.jpg"))
        if pid in animated and fmt == "reel":
            print("MP4 (animowane napisy):", animated[pid])
            post = next(p for p in spec["posts"] if p["id"] == pid)
            if post.get("logo", True):
                # zasada Michała (30.10): animowane logo twórcy na końcu każdego filmu – przed muzyką,
                # żeby dźwięk zgrał się z wejściem logo
                import logo_outro
                logo_outro.dodaj_logo(animated[pid])
                print("Logo na końcu:", animated[pid])
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
