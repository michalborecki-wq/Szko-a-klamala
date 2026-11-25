#!/usr/bin/env python3
"""Rolka-pętla ok. 7 s (decyzja Michała 22.11): kinetyczne napisy na ruchomym tle, bez dźwięku.

Cały tekst jest widoczny od klatki 0 (okładka = klatka 0), a ruch jest okresowy (okres = długość
rolki), więc koniec pasuje do początku i pętla nie skacze:
  * żółte „czytające” podświetlenie przebiega przez tekst szybciej, niż da się czytać,
  * pasek „PILNE” przewija się na dole,
  * riposta pulsuje, marker kreśli podkreślenie, cała plansza lekko „oddycha”,
  * tło (wideo lub obraz) – 1/2 czasu do przodu, 1/2 wstecz; obraz – zoom tam i z powrotem.

Użycie:
  python3 petla7.py spec.json --data 2026-11-23 --pora 0900 [--opis opis.md] [--relacja "nagł|pod"]

Spec (JSON):
  id, seria, tag, haczyk (lista linii), riposta, akapity (lista), bronisz, pasek, stopka,
  tlo (ścieżka mp4/jpg/png), tlo_start (s), rozmycie (sigma, domyślnie 7), sek (domyślnie 7),
  ai (true → etykieta „Ilustracja AI…”).
Znaczniki w tekście: *żółte*, !czerwone!, **pogrubione**.
"""
import argparse, html, json, math, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H, FPS = 1080, 1920, 30


def mark(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*", r'<span class="y">\1</span>', t)
    t = re.sub(r"!(.+?)!", r'<span class="r">\1</span>', t)
    t = re.sub(r"(?<=\s)([aiouwzAIOUWZ])\s", r"\1&nbsp;", t)  # twarde spacje
    t = re.sub(r"(\d)\s+(?=\d{3}(?!\d))", r"\1&nbsp;", t)
    return t


def words(t):
    """Opakowuje słowa w <span class="w"> (dla podświetlenia), nie psując znaczników."""
    out, depth = [], 0
    for tok in re.split(r"(<[^>]+>|&nbsp;|\s+)", t):
        if not tok:
            continue
        if tok.startswith("<") or tok.isspace() or tok == "&nbsp;":
            out.append(tok)
        else:
            out.append(f'<span class="w">{tok}</span>')
    return "".join(out)


def build_html(s):
    hook = "<br>".join(mark(l) for l in s["haczyk"])
    paras = "".join(f"<p>{words(mark(p))}</p>" for p in s.get("akapity", []))
    bron = s.get("bronisz")
    bron_html = f'<div class="box"><p>{words(mark(bron))}</p></div>' if bron else ""
    pasek = html.escape(s.get("pasek", "PILNE"))
    if len(s.get("pasek", "")) > 40:
        sys.exit(f"Pasek ma {len(s.get('pasek',''))} znaków – maks. 40 (czytelność, poprawka Michała 25.11). Skróć „pasek” w specu.")
    ai = "Ilustracja AI – nie jest zdjęciem wydarzenia · " if s.get("ai", True) else ""
    stopka = mark(s.get("stopka", ""))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;background:transparent;overflow:hidden}}
body{{font-family:"Inter",sans-serif;color:#fff;position:relative;text-shadow:0 2px 10px rgba(0,0,0,.85)}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,14,24,.25) 0%,rgba(10,14,24,.64) 22%,rgba(10,14,24,.72) 68%,rgba(10,14,24,.30) 100%)}}
.top{{position:absolute;top:150px;left:64px;right:150px;font:900 italic 30px "Inter Display";letter-spacing:2px;color:#FFC727}}
.dot{{display:inline-block;width:14px;height:14px;border-radius:50%;background:#E53935;margin-right:12px;vertical-align:2px}}
#card{{position:absolute;top:240px;left:64px;right:150px;transform-origin:0 0}}
.tag{{display:inline-block;background:#E53935;font:900 italic 30px "Inter Display";padding:6px 14px;transform:skew(-6deg);margin-bottom:16px}}
h1{{font:900 italic 88px/0.98 "Inter Display";margin:0;text-transform:uppercase}}
h1 .y{{color:#FFC727;background:none;padding:0;text-shadow:0 2px 10px rgba(0,0,0,.85)}} h1 .r{{color:#E53935}}
#rip .y{{background:none;color:#FFC727;padding:0}}
.siren{{position:absolute;inset:0;pointer-events:none;mix-blend-mode:screen}}
#prog{{position:absolute;top:118px;left:64px;right:150px;height:10px;background:rgba(255,255,255,.18);border-radius:5px;overflow:hidden}}
#pf{{height:100%;width:0;background:linear-gradient(90deg,#FFC727,#E53935)}}
#plab{{position:absolute;top:88px;right:150px;font:800 22px "Inter";color:#fff}}
#flash{{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none}}
#rip{{display:inline-block;font:900 italic 92px/1.05 "Inter Display";color:#E53935;text-transform:uppercase;transform-origin:0 60%;position:relative;margin:4px 0 22px}}
#mk{{position:absolute;left:0;bottom:-4px;height:12px;background:#FFC727;border-radius:6px;width:0}}
p{{font:500 32px/1.3 "Inter";margin:0 0 14px}}
b{{font-weight:800}} .y{{background:#FFC727;color:#0A0E18;padding:0 6px;font-weight:800;text-shadow:none}} .r{{color:#ff6b66;font-weight:800}}
.w{{border-radius:6px;transition:none}}
.w.on{{background:rgba(255,199,39,.92);color:#0A0E18;text-shadow:none}}
.box{{border-left:8px solid #FFC727;padding:4px 0 4px 20px;margin-top:6px}} .box p{{margin:0}}
#tick{{position:absolute;left:0;right:0;bottom:380px;height:64px;background:#E53935;overflow:hidden;transform:skewY(-2deg)}}
#tt{{position:absolute;top:8px;white-space:nowrap;font:900 italic 40px "Inter Display";color:#fff;text-shadow:none}}
.foot{{position:absolute;bottom:470px;left:64px;right:150px;font:500 21px/1.35 "Inter";color:#d5ddf0}}
</style></head><body>
<div class="shade"></div>
<div class="siren" id="sr"></div>
<div id="prog"><div id="pf"></div></div><div id="plab">ZDĄŻYSZ?</div>
<div class="top"><span class="dot" id="dot"></span>SZKOŁA KŁAMAŁA · {html.escape(s.get('seria',''))}</div>
<div id="card">
<div class="tag">{html.escape(s.get('tag',''))}</div>
<h1>{hook}</h1>
<div id="rip">{mark(s.get('riposta',''))}<span id="mk"></span></div>
{paras}{bron_html}
</div>
<div class="foot">{stopka}<br>{ai}@szkola_klamala</div>
<div id="tick"><div id="tt"></div></div>
<div id="flash"></div>
<script>
const PASEK = {json.dumps(pasek + '   •   ')};
const tt = document.getElementById('tt');
tt.textContent = PASEK.repeat(12);
let unit = 0;
function measure(){{ const s=document.createElement('span'); s.style.font=getComputedStyle(tt).font; s.style.whiteSpace='nowrap'; s.textContent=PASEK; document.body.appendChild(s); unit=s.getBoundingClientRect().width; s.remove(); }}
const ws=[...document.querySelectorAll('#card .w')];
function setT(t, T){{
  if(!unit) measure();
  const ph = t / T;                         // 0..1, okresowe
  const k = Math.floor(ph * ws.length);     // „czytające” podświetlenie – za szybkie
  ws.forEach((w,i)=>w.classList.toggle('on', i>=k && i<k+3));
  // pasek czytelny (poprawka Michała 25.11): ok. 130 px/s zamiast ok. 700 px/s; przesunięcie = całe powtórzenia
  // paska, więc pętla dalej jest bez szwu (krótki pasek ≤ 40 znaków → 1 powtórzenie na 7 s)
  const nrep = Math.max(1, Math.round(900/unit));
  tt.style.transform = `translateX(${{-ph*unit*nrep}}px)`;
  const pul = 1 + 0.06*Math.pow(Math.max(0,Math.sin(ph*Math.PI*4)),6);
  document.getElementById('rip').style.transform = `scale(${{pul}}) rotate(-2deg)`;
  const mk = document.getElementById('mk');
  const m = ph < .5 ? ph*2 : 1 - (ph-.5)*2;              // marker tam i z powrotem
  mk.style.width = (Math.min(1, m*1.6)*100) + '%';
  const br = 1 + 0.012*Math.sin(ph*Math.PI*2);
  document.getElementById('card').style.transform = `scale(${{br}})`;
  document.getElementById('dot').style.opacity = (Math.sin(ph*Math.PI*8)>0)?1:.25;
  // światła „koguta”: czerwone z lewej, niebieskie z prawej, na zmianę (4 cykle na okres)
  const a = (Math.sin(ph*Math.PI*8)+1)/2, bb = 1-a;
  document.getElementById('sr').style.background =
    `radial-gradient(60% 40% at 0% 30%, rgba(229,57,53,${{.55*a}}), transparent 70%),`+
    `radial-gradient(60% 40% at 100% 70%, rgba(47,107,255,${{.55*bb}}), transparent 70%)`;
  // pasek „zdążysz?” – pełny tuż przed końcem pętli
  document.getElementById('pf').style.width = (ph*100)+'%';
  document.getElementById('plab').textContent = (T - t).toFixed(1).replace('.',',') + ' s';
  // drganie haczyka + błysk i szarpnięcie przy przejściu pętli (ph ≈ 0 i ≈ 1)
  // tylko końcówka pętli – klatka 0 (okładka, pierwsze wrażenie) zostaje czysta
  const hit = Math.max(0, 1 - (1-ph)*T/0.22);
  document.getElementById('flash').style.opacity = (0.55*hit).toFixed(3);
  const j = Math.sin(ph*Math.PI*2*14)*1.2 + hit*10;
  document.querySelector('h1').style.transform = `translate(${{j}}px, ${{-hit*6}}px)`;
}}
</script></body></html>"""


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"Błąd: {' '.join(cmd[:3])}…\n{r.stderr[-1500:]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("--data", required=True); ap.add_argument("--pora", required=True)
    ap.add_argument("--opis"); ap.add_argument("--relacja"); ap.add_argument("--out")
    a = ap.parse_args()
    s = json.load(open(a.spec, encoding="utf-8"))
    T = float(s.get("sek", 7)); N = int(round(T * FPS)); ID = s["id"].upper()
    out = a.out or os.path.join(ROOT, "VIRAL_REELS_FACTORY/DOSTAWA", f"{a.data}_{a.pora}")
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="petla7_")
    hp = os.path.join(tmp, "p.html"); open(hp, "w", encoding="utf-8").write(build_html(s))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg.goto("file://" + hp); pg.wait_for_timeout(600)
        bottom = pg.evaluate("document.getElementById('card').getBoundingClientRect().bottom")
        nw = pg.evaluate("document.querySelectorAll('#card .w').length")
        if bottom > H - 520:
            print(f"⚠ Tekst sięga {bottom:.0f} px (limit {H-520}) – skróć akapity.")
        print(f"Słowa w treści: {nw} (cel 90–120)")
        for i in range(N):
            pg.evaluate(f"setT({i/FPS}, {T})")
            pg.screenshot(path=os.path.join(tmp, f"f{i:04d}.png"), omit_background=True)
        b.close()
    tlo = os.path.join(ROOT, s["tlo"]) if not os.path.isabs(s["tlo"]) else s["tlo"]
    sig = s.get("rozmycie", 7); half = T / 2
    base = f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},gblur=sigma={sig},eq=brightness=0.04:saturation=1.15,setsar=1"
    if tlo.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        zf = f"zoompan=z='1+0.08*(1-cos(2*PI*on/{N}))/2':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={N}:s={W*2}x{H*2}:fps={FPS}"
        bg_in = ["-loop", "1", "-i", tlo]; bgf = f"[0:v]scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},{zf},gblur=sigma={sig},setsar=1,trim=end_frame={N}[bg]"
    else:
        st = s.get("tlo_start", 0)
        bg_in = ["-i", tlo]
        bgf = f"[0:v]trim={st}:{st+half},setpts=PTS-STARTPTS,fps={FPS},{base},split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0[bg]"
    ig = os.path.join(out, f"{ID}_INSTAGRAM.mp4"); tk = os.path.join(out, f"{ID}_TIKTOK.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", *bg_in, "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.png"),
         "-filter_complex", f"{bgf};[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[v]", "-map", "[v]", "-an",
         "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-level", "5.1", "-movflags", "+faststart", "-t", str(T), ig])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", ig, "-vf", "scale=1080:1920:flags=lanczos", "-an", "-c:v", "libx264", "-crf", "18",
         "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p", "-movflags", "+faststart", tk])
    okl = os.path.join(out, f"{ID}_okladka.jpg")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", ig, "-frames:v", "1", "-q:v", "2", okl])
    sel = "+".join(f"eq(n\\,{int(N*f)})" for f in (0, .25, .5, .75)) + f"+eq(n\\,{N-1})"
    sheet = os.path.join(out, f"{ID}_klatki.jpg")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", ig, "-vf", f"select='{sel}',scale=432:-1,tile=5x1", "-frames:v", "1", sheet])
    if a.relacja:
        nag, _, pod = a.relacja.partition("|")
        run([sys.executable, os.path.join(ROOT, "VIRAL_REELS_FACTORY/narzedzia/relacja.py"), okl,
             os.path.join(out, f"{ID}_relacja.jpg"), "--naglowek", nag, "--pod", pod])
    if a.opis:
        shutil.copy(a.opis, os.path.join(out, f"{ID}_opis.md"))
    shutil.rmtree(tmp, ignore_errors=True)
    print("Arkusz klatek do kontroli:", sheet)
    print("DOSTAWA – wyślij pojedynczo:")
    for f in sorted(os.listdir(out)):
        if f.startswith(ID) and not f.endswith("_klatki.jpg"):
            print(os.path.join(out, f))


if __name__ == "__main__":
    main()
