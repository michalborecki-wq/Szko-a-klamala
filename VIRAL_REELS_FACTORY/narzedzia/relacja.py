#!/usr/bin/env python3
"""
Wklejka do relacji IG/TikTok (9:16, 2160×3840) w stylu marki: nagłówek, okładka rolki jako karta, plakietka
„NOWA ROLKA” i puste pole na naklejkę (ankieta / suwak / link do posta), poza strefami UI relacji.

  python3 relacja.py <okladka.jpg> <out.jpg> --naglowek "Broń bez pozwolenia?" [--pod "Sprawdź, co mówi ustawa"]
        [--naklejka "Tu wklej ankietę"]

Strefy: góra 250 px i dół 340 px (w układzie 1080) zostają wolne – tam aplikacja ma pasek i pole odpowiedzi.
"""
import argparse
import base64
import html

from playwright.sync_api import sync_playwright

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;font-family:'Inter';color:#fff;position:relative;
 background:linear-gradient(160deg,#0A0E18 0%,#16203A 100%)}
.s{position:absolute;width:1600px;height:150px;background:linear-gradient(90deg,transparent,#2F6BFF99,transparent);transform:rotate(-24deg)}
.s1{top:180px;left:-320px}.s2{bottom:420px;left:-260px;opacity:.55}
.grain{position:absolute;inset:0;opacity:.07;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence baseFrequency='.9'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>")}
.mark{position:absolute;top:270px;left:70px;font:900 italic 30px 'Inter Display';letter-spacing:1px}
.mark b{color:#FFC727}
h1{position:absolute;top:330px;left:70px;right:70px;font:900 italic 88px/1.02 'Inter Display';text-transform:uppercase}
h1 span{color:#FFC727}
.pod{position:absolute;top:0;left:70px;right:70px;font:600 38px/1.3 Inter;color:#E8ECF6}
.card{position:absolute;left:50%;top:640px;width:446px;height:793px;margin-left:-223px;border-radius:36px;overflow:hidden;
 transform:rotate(-3deg);box-shadow:0 40px 90px #000c,0 0 0 6px #FFC727}
.card img{width:100%;height:100%;object-fit:cover}
.badge{position:absolute;top:618px;left:205px;transform:rotate(-8deg);background:#E53935;color:#fff;
 font:900 italic 44px 'Inter Display';padding:10px 26px;border-radius:12px;box-shadow:0 12px 30px #0008;z-index:2}
.play{position:absolute;left:680px;top:1320px;width:120px;height:120px;border-radius:50%;
 background:#FFC727;display:flex;align-items:center;justify-content:center;z-index:2;box-shadow:0 12px 40px #0009}
.play:after{content:"";border-left:42px solid #0A0E18;border-top:26px solid transparent;border-bottom:26px solid transparent;margin-left:10px}
.slot{position:absolute;left:170px;right:170px;bottom:355px;height:130px;border:4px dashed #FFC72799;border-radius:28px;
 display:flex;align-items:center;justify-content:center;font:700 30px Inter;color:#FFC727cc;z-index:3;background:#0A0E18aa}
.handle{position:absolute;bottom:550px;width:100%;text-align:center;font:700 30px Inter;color:#C9D3EA;z-index:3}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("okladka")
    ap.add_argument("out")
    ap.add_argument("--naglowek", required=True, help="≤6 słów; *gwiazdki* = żółty akcent")
    ap.add_argument("--pod", default="")
    ap.add_argument("--naklejka", default="▼ tu naklejka: ankieta")
    a = ap.parse_args()

    img = "data:image/jpeg;base64," + base64.b64encode(open(a.okladka, "rb").read()).decode()
    nag = html.escape(a.naglowek)
    parts = nag.split("*")
    nag = "".join(f"<span>{p}</span>" if i % 2 else p for i, p in enumerate(parts))
    pod = f"<div class=pod id=pod>{html.escape(a.pod)}</div>" if a.pod else ""
    body = (f"<div class='s s1'></div><div class='s s2'></div><div class=mark>SZKOŁA <b>KŁAMAŁA</b></div>"
            f"<h1 id=h>{nag}</h1>{pod}<div class=badge>NOWA ROLKA</div><div class=card><img src='{img}'></div>"
            f"<div class=play></div>"
            f"<div class=slot>{html.escape(a.naklejka)}</div><div class=grain></div>")
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        pg.set_content(f"<html><head><style>{CSS}</style></head><body>{body}</body></html>")
        pg.wait_for_timeout(300)
        # podtekst tuż pod nagłówkiem; nagłówek nie może wejść na kartę
        pg.evaluate("""() => { const h = document.getElementById('h'), p = document.getElementById('pod');
            let fs = 88; while (h.getBoundingClientRect().bottom > (p ? 520 : 580) && fs > 52) { fs -= 4; h.style.fontSize = fs + 'px'; }
            if (p) p.style.top = (h.getBoundingClientRect().bottom + 16) + 'px'; }""")
        pg.screenshot(path=a.out, type="jpeg", quality=92)
        br.close()
    print(a.out)


if __name__ == "__main__":
    main()
