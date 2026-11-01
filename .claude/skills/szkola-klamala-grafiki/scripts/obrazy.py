"""
Obrazy-bohaterowie okładek rolek „Szkoła kłamała” (decyzja 1.11: pierwsza klatka musi mieć co oglądać).

Wektorowe ilustracje w palecie marki, rysowane w kodzie – bez cudzych grafik i bez twarzy.
Każda ma animację CSS (silnik ustawia czas klatki, więc ruch jest deterministyczny),
a główny kształt jest widoczny od klatki 0. Użycie w slajdzie `cover`: "obraz": "<nazwa>".

Nazwy: polska (+ "obraz_opcje": {"granica": "CZE", "przekreslona": "DEU"}), torba, suwak,
dowod, monety. Nowy obraz: dopisz funkcję i dodaj do OBRAZY.
"""
import json
import math
import os

Y, B, R, N, N2, W = "#FFC727", "#2F6BFF", "#E53935", "#0A0E18", "#16203A", "#F4F6FB"
HERE = os.path.dirname(os.path.abspath(__file__))

CSS = f"""
.hero-ill{{position:absolute;left:-20px;right:-20px;top:0;height:{{h}}px;display:flex;align-items:center;justify-content:center;z-index:3;pointer-events:none}}
.hero-ill svg{{height:100%;width:auto;max-width:100%;overflow:visible;filter:drop-shadow(0 24px 40px rgba(0,0,0,.45))}}
.ob-in{{animation:obIn .7s cubic-bezier(.2,.9,.25,1.15) 0s both;transform-box:fill-box;transform-origin:center}}
.ob-draw{{stroke-dasharray:1;stroke-dashoffset:1;animation:obDraw .9s ease-out .25s forwards}}
.ob-pulse{{animation:obPulse 1.2s ease-in-out .9s infinite;transform-box:fill-box;transform-origin:center}}
.ob-slide{{animation:obSlide .8s cubic-bezier(.2,.9,.25,1) .1s both}}
.ob-drop{{animation:obDrop .5s cubic-bezier(.3,1.4,.5,1) both;transform-box:fill-box}}
.ob-car{{animation:obCar 2.4s linear infinite}}
.ob-merge{{animation:obMerge 2.4s ease-in-out infinite}}
.cstamp{{position:absolute;z-index:7;right:40px;top:{{st}}px;font-family:'Inter Display','Inter';font-weight:900;font-style:italic;
  font-size:84px;line-height:1;color:{R};border:9px solid {R};border-radius:14px;padding:8px 26px 4px;letter-spacing:3px;
  transform:rotate(-12deg);background:rgba(10,14,24,.55);box-shadow:0 0 40px rgba(229,57,53,.45);white-space:nowrap}}
@keyframes obIn{{from{{transform:scale(1.14) rotate(-2deg)}}to{{transform:none}}}}
@keyframes obDraw{{to{{stroke-dashoffset:0}}}}
@keyframes obPulse{{0%,100%{{transform:none}}50%{{transform:scale(1.06)}}}}
@keyframes obSlide{{from{{transform:translate(260px,140px) rotate(25deg)}}to{{transform:none}}}}
@keyframes obDrop{{from{{transform:translateY(-260px)}}to{{transform:none}}}}
@keyframes obCar{{from{{transform:translateY(-260px)}}to{{transform:translateY(260px)}}}}
@keyframes obMerge{{0%,30%{{transform:translate(0,-240px)}}70%,100%{{transform:translate(-150px,240px)}}}}
"""


def _svg(vb, body):
    return f"<svg viewBox='{vb}' xmlns='http://www.w3.org/2000/svg'>{body}</svg>"


def polska(granica="CZE", przekreslona="DEU", **_):
    d = json.load(open(os.path.join(HERE, "..", "assets", "mapa_polska.json")))
    k, g = d["kraje"], d["granice"]
    sas = "".join(f"<path d='{k[c]}' fill='{N2}' stroke='rgba(47,107,255,.45)' stroke-width='2'/>"
                  for c in k if c != "POL")
    body = (f"<defs><linearGradient id='plg' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#3D7BFF'/>"
            f"<stop offset='1' stop-color='#1E4FD8'/></linearGradient>"
            f"<filter id='glow'><feGaussianBlur stdDeviation='9' result='b'/><feMerge><feMergeNode in='b'/>"
            f"<feMergeNode in='SourceGraphic'/></feMerge></filter></defs>"
            f"<g class='ob-in'>{sas}<path d='{k['POL']}' fill='url(#plg)' stroke='{W}' stroke-width='4'/></g>")
    if przekreslona and g.get(przekreslona):
        body += (f"<path d='{g[przekreslona]}' fill='none' stroke='{R}' stroke-width='12' stroke-linecap='round' "
                 f"stroke-dasharray='4 22' opacity='.95'/>")
    if granica and g.get(granica):
        body += (f"<path d='{g[granica]}' pathLength='1' class='ob-draw' fill='none' stroke='{Y}' stroke-width='16' "
                 f"stroke-linecap='round' stroke-linejoin='round' filter='url(#glow)'/>")
    return _svg(f"-20 -20 {d['W'] + 40} {d['H'] + 40}", body)


def torba(**_):
    body = (f"<g class='ob-in'>"
            f"<path d='M330 300 Q330 170 500 170 Q670 170 670 300' fill='none' stroke='{W}' stroke-width='34' stroke-linecap='round'/>"
            f"<path d='M230 300 H770 L820 760 Q822 800 782 800 H218 Q178 800 180 760 Z' fill='{Y}'/>"
            f"<path d='M230 300 H770 L778 372 H222 Z' fill='#E0A800'/>"
            f"<rect x='455' y='340' width='90' height='70' rx='14' fill='{N}'/>"
            f"<path d='M300 520 H700' stroke='rgba(10,14,24,.25)' stroke-width='14' stroke-linecap='round'/></g>"
            f"<g class='ob-slide'><circle cx='770' cy='560' r='120' fill='rgba(244,246,251,.10)' stroke='{W}' stroke-width='30'/>"
            f"<path d='M855 645 L960 750' stroke='{W}' stroke-width='42' stroke-linecap='round'/></g>"
            f"<circle cx='740' cy='600' r='215' fill='none' stroke='{R}' stroke-width='34' pathLength='1' class='ob-draw'/>"
            f"<path d='M588 448 L892 752' stroke='{R}' stroke-width='34' stroke-linecap='round' pathLength='1' class='ob-draw'/>")
    return _svg("120 120 900 760", body)


def suwak(**_):
    # widok z góry: dwa pasy, lewy się kończy; auta łączą się na zmianę tuż przed końcem pasa
    road = (f"<rect x='250' y='0' width='500' height='1000' fill='#1B2236'/>"
            f"<path d='M250 0 V560 L500 760 V1000' fill='none' stroke='{W}' stroke-width='10'/>"
            f"<path d='M750 0 V1000' stroke='{W}' stroke-width='10'/>"
            f"<path d='M500 0 V560' stroke='{W}' stroke-width='10' stroke-dasharray='50 40'/>"
            f"<path d='M250 560 L500 760 L250 1000 Z' fill='{N}'/>"
            f"<path d='M380 520 Q380 640 560 700' fill='none' stroke='{Y}' stroke-width='14' stroke-linecap='round' "
            f"pathLength='1' class='ob-draw'/>"
            f"<path d='M545 672 L575 706 L530 716' fill='none' stroke='{Y}' stroke-width='14' stroke-linecap='round' stroke-linejoin='round'/>")
    car = lambda x, y, col, cls, delay: (
        f"<g class='{cls}' style='animation-delay:{delay}s'><rect x='{x}' y='{y}' width='120' height='190' rx='26' fill='{col}'/>"
        f"<rect x='{x + 18}' y='{y + 30}' width='84' height='44' rx='10' fill='rgba(10,14,24,.55)'/></g>")
    cars = (car(565, 330, Y, "ob-car", 0) + car(565, 330, W, "ob-car", -1.2)
            + car(315, 330, B, "ob-merge", -.6) + car(315, 330, B, "ob-merge", -1.8))
    return _svg("150 0 700 1000", f"<g class='ob-in'>{road}</g><g clip-path='url(#cl)'>{cars}</g>"
                                  f"<clipPath id='cl'><rect x='250' y='0' width='500' height='1000'/></clipPath>")


def dowod(**_):
    body = (f"<g class='ob-in'><rect x='120' y='220' width='760' height='480' rx='44' fill='{W}'/>"
            f"<rect x='120' y='220' width='760' height='110' rx='44' fill='{B}'/><rect x='120' y='290' width='760' height='40' fill='{B}'/>"
            f"<rect x='175' y='385' width='210' height='260' rx='20' fill='#C9D3EA'/>"
            f"<circle cx='280' cy='475' r='58' fill='#8FA1C7'/><path d='M190 645 Q280 520 370 645 Z' fill='#8FA1C7'/>"
            + "".join(f"<rect x='430' y='{y}' width='{w}' height='30' rx='15' fill='#C9D3EA'/>"
                      for y, w in ((400, 380), (460, 300), (520, 340), (580, 240)))
            + f"</g><g class='ob-pulse'><circle cx='820' cy='250' r='120' fill='{R}'/>"
            f"<text x='820' y='300' font-family='Inter Display,Inter' font-weight='900' font-style='italic' font-size='150' "
            f"fill='{W}' text-anchor='middle'>?</text></g>")
    return _svg("80 100 900 680", body)


def monety(**_):
    coin = lambda x, y, d: (f"<g class='ob-drop' style='animation-delay:{d}s'>"
                            f"<ellipse cx='{x}' cy='{y + 34}' rx='150' ry='48' fill='#B88A00'/>"
                            f"<rect x='{x - 150}' y='{y}' width='300' height='34' fill='#B88A00'/>"
                            f"<ellipse cx='{x}' cy='{y}' rx='150' ry='48' fill='{Y}'/>"
                            f"<ellipse cx='{x}' cy='{y}' rx='100' ry='30' fill='none' stroke='#E0A800' stroke-width='10'/></g>")
    stack = "".join(coin(420, 760 - i * 62, .05 * i) for i in range(7))
    arrow = (f"<path d='M640 330 A250 250 0 1 1 330 210' fill='none' stroke='{B}' stroke-width='40' stroke-linecap='round' "
             f"pathLength='1' class='ob-draw'/><path d='M300 150 L345 215 L270 245' fill='none' stroke='{B}' "
             f"stroke-width='40' stroke-linecap='round' stroke-linejoin='round'/>")
    return _svg("130 80 820 820", f"<g class='ob-in'>{stack}</g>{arrow}")


OBRAZY = {"polska": polska, "torba": torba, "suwak": suwak, "dowod": dowod, "monety": monety}


def html(nazwa, opcje=None, wysokosc=520, pieczatka=None):
    """Warstwa obrazu do wstawienia na początku .content okładki (rolka)."""
    if nazwa not in OBRAZY:
        raise KeyError(f"nieznany obraz: {nazwa} (dostępne: {', '.join(OBRAZY)})")
    css = CSS.replace("{h}", str(wysokosc)).replace("{st}", str(int(wysokosc * .62)))
    st = f"<div class='cstamp'>{pieczatka}</div>" if pieczatka else ""
    return f"<style>{css}</style><div class='hero-ill'>{OBRAZY[nazwa](**(opcje or {}))}</div>{st}"
