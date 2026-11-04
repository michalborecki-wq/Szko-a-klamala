"""
Obrazy-bohaterowie okładek rolek „Szkoła kłamała” (decyzja 1.11: pierwsza klatka musi mieć co oglądać).

Wektorowe ilustracje w palecie marki, rysowane w kodzie – bez cudzych grafik i bez twarzy.
Każda ma animację CSS (silnik ustawia czas klatki, więc ruch jest deterministyczny),
a główny kształt jest widoczny od klatki 0. Użycie w slajdzie `cover`: "obraz": "<nazwa>".

Nazwy: opona, polska (+ "obraz_opcje": {"granica": "CZE", "przekreslona": "DEU"}), torba, suwak,
dowod, monety, zegar, licznik, ruletka, saturn, odznaka. Nowy obraz: dopisz funkcję i dodaj do OBRAZY.
"""
import json
import math
import os

Y, B, R, N, N2, W = "#FFC727", "#2F6BFF", "#E53935", "#0A0E18", "#16203A", "#F4F6FB"
HERE = os.path.dirname(os.path.abspath(__file__))

CSS = f"""
.hero-ill{{position:absolute;left:0;right:0;top:0;overflow:hidden;height:{{h}}px;display:flex;align-items:center;justify-content:center;z-index:3;pointer-events:none}}
.hero-ill svg{{height:100%;width:auto;max-width:100%;overflow:visible}}
.ob-in{{animation:obIn .7s cubic-bezier(.2,.9,.25,1.15) 0s both;transform-box:fill-box;transform-origin:center}}
.ob-draw{{stroke-dasharray:1;stroke-dashoffset:1;animation:obDraw .9s ease-out .25s forwards}}
.ob-pulse{{animation:obPulse 1.2s ease-in-out .9s infinite;transform-box:fill-box;transform-origin:center}}
.ob-slide{{animation:obSlide .8s cubic-bezier(.2,.9,.25,1) .1s both}}
.ob-drop{{animation:obDrop .5s cubic-bezier(.3,1.4,.5,1) both;transform-box:fill-box}}
.ob-car{{animation:obCar 2.4s linear infinite}}
.ob-merge{{animation:obMerge 2.4s ease-in-out infinite}}
.ob-spin{{animation:obSpin 3.2s linear infinite;transform-box:fill-box;transform-origin:center}}
.cstamp{{position:absolute;z-index:7;right:40px;top:{{st}}px;font-family:'Inter Display','Inter';font-weight:900;font-style:italic;
  font-size:84px;line-height:1;color:{R};border:9px solid {R};border-radius:14px;padding:8px 26px 4px;letter-spacing:3px;
  transform:rotate(-12deg);background:rgba(10,14,24,.55);box-shadow:0 0 40px rgba(229,57,53,.45);white-space:nowrap}}
@keyframes obSpin{{from{{transform:rotate(0)}}to{{transform:rotate(360deg)}}}}
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
            f"</defs>"
            f"<g class='ob-in'>{sas}<path d='{k['POL']}' fill='url(#plg)' stroke='{W}' stroke-width='4'/></g>")
    if przekreslona and g.get(przekreslona):
        body += (f"<path d='{g[przekreslona]}' fill='none' stroke='{R}' stroke-width='12' stroke-linecap='round' "
                 f"stroke-dasharray='4 22' opacity='.95'/>")
    if granica and g.get(granica):
        # poświata bez filtra rozmycia (tanio w 4K): szeroka półprzezroczysta linia pod właściwą
        body += (f"<path d='{g[granica]}' pathLength='1' class='ob-draw' fill='none' stroke='{Y}' stroke-width='40' "
                 f"stroke-linecap='round' stroke-linejoin='round' opacity='.28'/>"
                 f"<path d='{g[granica]}' pathLength='1' class='ob-draw' fill='none' stroke='{Y}' stroke-width='16' "
                 f"stroke-linecap='round' stroke-linejoin='round'/>")
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


def opona(**_):
    # opona zimowa z bieżnikiem (kręci się) + płatek śniegu na znaczku
    import math as _m
    bloki = "".join(
        f"<rect x='-26' y='-318' width='52' height='70' rx='10' fill='#46527A' transform='rotate({k * 15})'/>"
        for k in range(24))
    lamele = "".join(
        f"<path d='M0 -300 L0 -262' stroke='#0A0E18' stroke-width='6' transform='rotate({k * 15 + 7.5})'/>"
        for k in range(24))
    szprychy = "".join(
        f"<path d='M0 -40 L0 -165' stroke='#C9D3EA' stroke-width='34' stroke-linecap='round' transform='rotate({k * 72})'/>"
        for k in range(5))
    kolo = (f"<g class='ob-spin'><circle r='300' fill='#2B3350' stroke='#4A5578' stroke-width='6'/>{bloki}{lamele}"
            f"<circle r='215' fill='#1B2236'/><circle r='190' fill='#8FA1C7'/><circle r='178' fill='#1B2236'/>"
            f"{szprychy}<circle r='52' fill='#C9D3EA'/><circle r='22' fill='#1B2236'/></g>")
    ramie = lambda a: (f"<g transform='rotate({a})'><path d='M0 0 V-92' stroke='{W}' stroke-width='16' stroke-linecap='round'/>"
                       f"<path d='M0 -58 L-24 -80 M0 -58 L24 -80' stroke='{W}' stroke-width='12' stroke-linecap='round'/></g>")
    platek = (f"<g transform='translate(250 -250)' class='ob-pulse'><circle r='120' fill='{B}'/>"
              + "".join(ramie(a) for a in range(0, 360, 60)) + "</g>")
    return _svg("-340 -400 760 760", f"<g class='ob-in'>{kolo}</g>{platek}")


def zegar(**_):
    # tarcza zegara z biegnącą wskazówką i łukiem „48 h”
    ticks = "".join(f"<path d='M0 -270 V-{240 if k % 3 else 215}' stroke='{W}' stroke-width='{10 if k % 3 else 18}' "
                    f"stroke-linecap='round' transform='rotate({k * 30})'/>" for k in range(12))
    luk = (f"<circle r='320' fill='none' stroke='{Y}' stroke-width='34' stroke-linecap='round' pathLength='1' "
           f"class='ob-draw' transform='rotate(-90)'/>")
    wsk = (f"<g class='ob-spin'><path d='M0 30 V-235' stroke='{R}' stroke-width='16' stroke-linecap='round'/></g>"
           f"<path d='M0 0 V-150' stroke='{W}' stroke-width='24' stroke-linecap='round' transform='rotate(60)'/>"
           f"<circle r='26' fill='{W}'/>")
    return _svg("-380 -380 760 760", f"<g class='ob-in'><circle r='290' fill='{N2}' stroke='{B}' stroke-width='18'/>"
                f"{ticks}{wsk}</g>{luk}")


def licznik(**_):
    # prędkościomierz: łuk, czerwona strefa i wskazówka wbijająca się w czerwone
    kreski = "".join(f"<path d='M0 -300 V-262' stroke='{W}' stroke-width='10' stroke-linecap='round' "
                     f"transform='rotate({-120 + k * 20})'/>" for k in range(13))
    czerw = (f"<path d='M{300*math.sin(math.radians(60)):.1f} {-300*math.cos(math.radians(60)):.1f} "
             f"A300 300 0 0 1 {300*math.sin(math.radians(120)):.1f} {-300*math.cos(math.radians(120)):.1f}' "
             f"fill='none' stroke='{R}' stroke-width='40'/>")
    wsk = (f"<g style='transform-box:view-box;transform-origin:0 0;animation:obNeedle 1.4s cubic-bezier(.3,1.5,.5,1) .2s both'>"
           f"<path d='M-14 0 L0 -250 L14 0 Z' fill='{Y}'/></g><circle r='34' fill='{W}'/>"
           f"<style>@keyframes obNeedle{{from{{transform:rotate(-120deg)}}to{{transform:rotate(95deg)}}}}</style>")
    return _svg("-380 -360 760 620", f"<g class='ob-in'><path d='M-260 150 A300 300 0 1 1 260 150' fill='none' "
                f"stroke='{N2}' stroke-width='70'/>{czerw}{kreski}{wsk}</g>")


def ruletka(**_):
    pola = ""
    for k in range(37):
        a0, a1 = math.radians(k * 360 / 37), math.radians((k + 1) * 360 / 37)
        col = "#1FA35A" if k == 0 else (R if k % 2 else "#141A2B")
        pola += (f"<path d='M0 0 L{300*math.sin(a0):.1f} {-300*math.cos(a0):.1f} A300 300 0 0 1 "
                 f"{300*math.sin(a1):.1f} {-300*math.cos(a1):.1f} Z' fill='{col}' stroke='{Y}' stroke-width='2'/>")
    kolo = (f"<g class='ob-spin'>{pola}<circle r='170' fill='#7A4A1A'/><circle r='150' fill='#5C3510'/>"
            + "".join(f"<path d='M0 -40 V-140' stroke='{Y}' stroke-width='16' stroke-linecap='round' transform='rotate({k*90})'/>" for k in range(4))
            + f"<circle r='40' fill='{Y}'/></g>")
    return _svg("-360 -360 720 720", f"<g class='ob-in'><circle r='330' fill='#5C3510'/>{kolo}"
                f"<circle cx='0' cy='-250' r='22' fill='{W}' class='ob-pulse'/></g>")


def saturn(**_):
    ring = lambda op, back: (f"<ellipse rx='380' ry='92' fill='none' stroke='{Y}' stroke-width='30' opacity='{op}' "
                             f"transform='rotate(-18)' {'clip-path="url(#tyl)"' if back else ''}/>")
    planeta = (f"<defs><clipPath id='tyl'><rect x='-500' y='-500' width='1000' height='500'/></clipPath>"
               f"<linearGradient id='sat' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#F2D38A'/>"
               f"<stop offset='.5' stop-color='#D9A94E'/><stop offset='1' stop-color='#B8812F'/></linearGradient></defs>"
               f"{ring(.55, True)}<circle r='200' fill='url(#sat)'/>"
               + "".join(f"<path d='M-200 {y} Q0 {y+18} 200 {y}' stroke='#B8812F' stroke-width='10' fill='none' opacity='.5'/>" for y in (-90, -20, 60))
               + f"<ellipse rx='380' ry='92' fill='none' stroke='{Y}' stroke-width='30' transform='rotate(-18)' "
               f"stroke-dasharray='600 1800' stroke-dashoffset='-300'/>")
    woda = (f"<path d='M-420 250 Q-320 220 -210 250 T0 250 T210 250 T420 250 V420 H-420 Z' fill='{B}' opacity='.75'/>")
    return _svg("-440 -330 880 760", f"<g class='ob-in'><g style='animation:obPulse 2.4s ease-in-out infinite;"
                f"transform-box:fill-box;transform-origin:center'>{planeta}</g>{woda}</g>")


def odznaka(**_):
    # ogólna tarcza „służb” (bez godła i bez logo Policji)
    tarcza = (f"<path d='M0 -300 L240 -210 V20 C240 180 120 270 0 320 C-120 270 -240 180 -240 20 V-210 Z' "
              f"fill='{B}' stroke='{W}' stroke-width='18'/>"
              f"<path d='M0 -220 L170 -155 V20 C170 130 90 200 0 235 C-90 200 -170 130 -170 20 V-155 Z' fill='{N2}'/>")
    gw = "M0 -120 L32 -40 L118 -38 L50 14 L74 98 L0 50 L-74 98 L-50 14 L-118 -38 L-32 -40 Z"
    return _svg("-320 -340 640 700", f"<g class='ob-in'>{tarcza}<path d='{gw}' fill='{Y}' class='ob-pulse'/></g>")


OBRAZY = {"polska": polska, "torba": torba, "suwak": suwak, "dowod": dowod, "monety": monety, "opona": opona, "zegar": zegar,
          "licznik": licznik, "ruletka": ruletka, "saturn": saturn, "odznaka": odznaka}


def html(nazwa, opcje=None, wysokosc=520, pieczatka=None):
    """Warstwa obrazu do wstawienia na początku .content okładki (rolka)."""
    if nazwa not in OBRAZY:
        raise KeyError(f"nieznany obraz: {nazwa} (dostępne: {', '.join(OBRAZY)})")
    css = CSS.replace("{h}", str(wysokosc)).replace("{st}", str(int(wysokosc * .62)))
    st = f"<div class='cstamp'>{pieczatka}</div>" if pieczatka else ""
    return f"<style>{css}</style><div class='hero-ill'>{OBRAZY[nazwa](**(opcje or {}))}</div>{st}"
