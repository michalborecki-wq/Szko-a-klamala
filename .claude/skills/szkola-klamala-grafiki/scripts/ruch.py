"""
Ruch „Szkoła kłamała” – biblioteka efektów animowanych Reelsów.

Klatki są renderowane deterministycznie: animacje CSS stoją, a każda klatka ustawia czas
wszystkich animacji i efektów liczonych w JS (window.__setT). Ten sam spec = ten sam film.

Warianty (wybierane per rolka i per plansza funkcją `styl()`, nadpisywane w spec polem "fx"):
  naglowek:  maska | litery | zoom | przesun          – wejście nagłówków
  haczyk:    uderzenie | blysk                         – plansza 1 (widoczna od klatki 0)
  tresc:     rozmycie | marker                         – wejście tekstu i żółtych wyróżnień
  liczba:    licznik | slot                            – duża liczba (+ pasek postępu dla %)
  mit:       kreska | pieczatka                        – przekreślenie mitu
  tlo:       gwiazdy | siatka | kule | 3d (z pola "tlo3d")                   – warstwa tła (domyślnie wg przedmiotu)
  przejscie: smuga | zoom | paski | blysk | kierunek | przeslona | warstwy | swiatlo – cięcie między planszami
  otwarcie:  uderzenie | blysk | zoomout | ciecie | skan | ramka | kinowe | rgb – plansza 1 (DVE)
  rgb, glebia: rozszczepienie RGB przy uderzeniach; pochylenie 2.5D + paralaksa (DVE 9.11)
  moc:       mocna (domyślnie) | spokojna              – najazd kamery 4,5%/planszę, puls na bicie, wstrząsy ×1,6
Każde wejście zgłasza zdarzenia (uderzenie, przekreślenie, marker…) – trafiają do <id>_zdarzenia.json
i synchronizują efekty dźwiękowe w muzyka.py.
"""
import hashlib

WARIANTY = {
    "naglowek": ["maska", "litery", "zoom", "przesun"],
    "haczyk": ["uderzenie", "blysk"],
    "tresc": ["rozmycie", "marker"],
    "liczba": ["licznik", "slot"],
    "mit": ["kreska", "pieczatka"],
    "przejscie": ["smuga", "zoom", "paski", "blysk", "kierunek", "przeslona", "warstwy", "swiatlo"],
    # Dynamic Visual Engine (8.11): otwarcie rolki (pierwsze 2 s), akcent na wielkiej liczbie
    "otwarcie": ["uderzenie", "blysk", "zoomout", "ciecie", "skan", "ramka", "kinowe", "rgb"],
    "akcent": ["ramka", "ostrosc"],
}
# Dobór animacji do rodzaju treści (pole posta "ton" albo przedmiot) – z tych list styl() losuje deterministycznie.
# Nie jeden styl dla wszystkich tematów: prawo/polityka = dokument i ramki, historia = skan i kino, nauka = zoom i ostrość,
# kontrowersja = cięcie, uderzenie, szybkie przejścia kierunkowe.
PRESETY = {
    "PRAWO":        {"otwarcie": ["ramka", "skan", "kinowe"], "przejscie": ["kierunek", "warstwy", "swiatlo", "paski", "przeslona", "smuga"], "akcent": ["ramka"]},
    "POLITYKA":     {"otwarcie": ["ramka", "skan", "ciecie", "rgb"], "przejscie": ["kierunek", "paski", "smuga"], "akcent": ["ramka"]},
    "HISTORIA":     {"otwarcie": ["skan", "kinowe"], "przejscie": ["przeslona", "warstwy", "swiatlo", "zoom", "smuga"], "akcent": ["ostrosc"]},
    "KOSMOS":       {"otwarcie": ["zoomout", "kinowe", "blysk"], "przejscie": ["przeslona", "swiatlo", "zoom", "blysk"], "akcent": ["ostrosc"]},
    "NAUKA":        {"otwarcie": ["zoomout", "skan", "blysk"], "przejscie": ["zoom", "przeslona", "paski"], "akcent": ["ostrosc", "ramka"]},
    "MOTORYZACJA":  {"otwarcie": ["ciecie", "uderzenie", "ramka", "rgb"], "przejscie": ["kierunek", "smuga", "blysk"], "akcent": ["ramka"]},
    "FINANSE":      {"otwarcie": ["ramka", "zoomout", "skan"], "przejscie": ["paski", "kierunek", "zoom"], "akcent": ["ramka", "ostrosc"]},
    "KONTROWERSJA": {"otwarcie": ["rgb", "ciecie", "uderzenie", "ramka"], "przejscie": ["kierunek", "warstwy", "blysk", "paski"], "akcent": ["ramka"]},
    "CIEKAWOSTKA":  {"otwarcie": ["zoomout", "blysk", "kinowe"], "przejscie": ["przeslona", "swiatlo", "zoom", "smuga"], "akcent": ["ostrosc"]},
}
PRESET_PRZEDMIOTU = {"PRAWO": "PRAWO", "POLITYKA": "POLITYKA", "HISTORIA": "HISTORIA", "KOSMOS": "KOSMOS",
                     "FIZYKA": "NAUKA", "CHEMIA": "NAUKA", "BIOLOGIA": "NAUKA", "CIAŁO": "NAUKA", "MÓZG": "NAUKA",
                     "MEDYCYNA": "NAUKA", "TECHNOLOGIA": "NAUKA", "MATEMATYKA": "NAUKA", "MOTORYZACJA": "MOTORYZACJA",
                     "FINANSE": "FINANSE", "EKONOMIA": "FINANSE", "GEOGRAFIA": "CIEKAWOSTKA"}


def preset(post):
    """Nazwa presetu animacji: jawne "ton" (np. "kontrowersja") > seria SPÓR > przedmiot > CIEKAWOSTKA."""
    ton = (post.get("ton") or "").upper()
    if ton in PRESETY:
        return ton
    if "SPÓR" in post.get("series", "").upper():
        return "KONTROWERSJA"
    return PRESET_PRZEDMIOTU.get(post.get("subject", "").upper(), "CIEKAWOSTKA")
TLO_PRZEDMIOTU = {"KOSMOS": "gwiazdy", "MATEMATYKA": "siatka", "FIZYKA": "siatka", "TECHNOLOGIA": "siatka",
                  "CHEMIA": "siatka", "FINANSE": "siatka", "EKONOMIA": "siatka"}


# nastrój muzyki i tempo (BPM) wg przedmiotu – cięcia plansz wypadają na bicie
NASTROJE = {"kosmos": 92, "elektro": 120, "napiecie": 100, "lekki": 120, "spokojny": 90}
NASTROJ_PRZEDMIOTU = {"KOSMOS": "kosmos", "MATEMATYKA": "elektro", "FIZYKA": "elektro", "TECHNOLOGIA": "elektro",
                      "CHEMIA": "elektro", "MOTORYZACJA": "elektro", "HISTORIA": "napiecie", "FINANSE": "spokojny",
                      "EKONOMIA": "spokojny", "PRAWO": "spokojny"}


def nastroj(post):
    m = post.get("muzyka") or {}
    if m.get("nastroj"):
        return m["nastroj"]
    if "SPÓR" in post.get("series", "").upper():
        return "napiecie"
    if "QUIZ" in post.get("series", "").upper():
        return "lekki"
    return NASTROJ_PRZEDMIOTU.get(post.get("subject", "").upper(), "lekki")


def bpm(post):
    """Tempo rolki: jawne muzyka.bpm albo tempo nastroju, gdy rolka ma mieć muzykę (pole "muzyka")."""
    m = post.get("muzyka")
    if m is None:
        return post.get("bpm")
    return m.get("bpm") or NASTROJE[nastroj(post)]


def _h(*parts):
    return int(hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest(), 16)


def styl(post, i, n):
    """Kombinacja efektów dla planszy i. Różna między rolkami (hash id), różna między planszami
    tej samej rolki (przesunięcie indeksu), zawsze z tej samej palety ruchów marki."""
    pid = post["id"]
    base = _h(pid)
    pr = PRESETY[preset(post)]
    fx = {}
    for k, opts in WARIANTY.items():
        opts = pr.get(k, opts)
        if k == "przejscie":
            # pierwsze cięcie zawsze markową smugą, kolejne rotują
            # przejście DO planszy i: pierwsze zawsze markową smugą, potem rotacja pozostałych wariantów
            # (kolejność zależna od rolki – dwie rolki nie mają tego samego układu)
            reszta = [o for o in opts if o != "smuga"] or ["zoom"]
            perm = [reszta[(base // 5 + j) % len(reszta)] for j in range(len(reszta))]
            if (base // 11) % 2:
                perm.reverse()
            fx[k] = "smuga" if i <= 1 else perm[(i - 2) % len(perm)]
        else:
            fx[k] = opts[(base // (7 + len(k)) + i) % len(opts)]
    fx["tlo"] = TLO_PRZEDMIOTU.get(post.get("subject", "").upper(), "kule")
    fx["kontur"] = True
    # moc ruchu: „mocna” (domyślnie od 1.11 – ciągły najazd kamery, puls na bicie, mocniejsze wstrząsy)
    # albo „spokojna” (dawny styl). Wnioski z rolki ISS: kadr nigdy nie stoi.
    fx["moc"] = post.get("moc", "mocna")
    fx["swiatlo"] = fx["moc"] == "mocna"          # smuga światła i oddychający gradient w tle
    fx["preset"] = preset(post)
    # DVE 9.11: rozszczepienie RGB (czerwień/niebieski marki) przy uderzeniach – tylko tematy „mocne”;
    # głębia 2.5D: lekkie pochylenie treści w perspektywie + paralaksa tła i obrazu-bohatera
    fx["rgb"] = fx["preset"] in ("KONTROWERSJA", "MOTORYZACJA", "POLITYKA")
    fx["glebia"] = fx["moc"] == "mocna"
    fx["bpm"] = bpm(post) or 0
    if post.get("tlo3d"):        # tło z renderu 3D (skill szkola-klamala-3d) zamiast warstw rysowanych w przeglądarce
        fx["tlo"], fx["kontur"] = "3d", False
    fx.update(post.get("fx", {}))                       # nadpisanie dla całej rolki
    fx.update(post["slides"][i].get("fx", {}))          # nadpisanie dla planszy
    return fx


def css(TOK):
    return f"""
.w{{display:inline-block}} .ch{{display:inline-block}}
.m{{display:inline-block;vertical-align:top;padding:0 .14em .34em 0;margin:0 -.14em -.34em 0}}
.fxbg{{position:absolute;inset:0;z-index:1;pointer-events:none;overflow:hidden}}
.fxbg canvas{{position:absolute;inset:0}}
.orb{{position:absolute;border-radius:50%;filter:blur(60px)}}
.t3d{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.t3dv{{position:absolute;inset:0;background:radial-gradient(ellipse 95% 50% at 50% 47%,rgba(10,14,24,.58) 0%,rgba(10,14,24,.36) 62%,rgba(10,14,24,.18) 100%)}}
.kontur{{position:absolute;left:50%;top:50%;white-space:nowrap;font-family:'Inter Display','Inter';font-weight:900;
  font-style:italic;font-size:560px;line-height:1;color:transparent;-webkit-text-stroke:3px rgba(47,107,255,.22);
  letter-spacing:-12px;text-transform:uppercase}}
.wipe{{position:absolute;inset:0;z-index:20;pointer-events:none;overflow:hidden}}
.wipe i{{position:absolute;top:-25%;height:150%;transform:skewX(-18deg)}}
.wipe .wb{{width:220%;left:-60%;background:linear-gradient(90deg,#1E4FD8,{TOK['blue']} 40%,#5B8CFF);box-shadow:0 0 80px rgba(47,107,255,.6)}}
.wipe .wy2{{width:9%;left:-74%;background:{TOK['yellow']};box-shadow:0 0 50px rgba(255,199,39,.7)}}
.wipe .wy{{width:9%;left:164%;background:{TOK['yellow']};box-shadow:0 0 50px rgba(255,199,39,.7)}}
.slats{{position:absolute;inset:0;z-index:20;pointer-events:none}}
.slats i{{position:absolute;left:0;width:100%;background:linear-gradient(90deg,#1E4FD8,{TOK['blue']} 70%,#5B8CFF);
  border-right:12px solid {TOK['yellow']};box-shadow:12px 0 40px rgba(255,199,39,.45)}}
.flash{{position:absolute;inset:0;z-index:19;pointer-events:none;background:radial-gradient(circle at 50% 45%,rgba(255,255,255,.95),rgba(91,140,255,.55) 40%,rgba(47,107,255,0) 72%);opacity:0}}
.spark{{position:absolute;z-index:6;width:8px;height:26px;border-radius:4px;background:{TOK['yellow']};
  box-shadow:0 0 14px rgba(255,199,39,.9);pointer-events:none;opacity:0}}
.spark:nth-child(3n){{background:#fff}}
.bar{{height:18px;border-radius:9px;background:rgba(255,255,255,.08);margin:6px 0 34px;overflow:hidden;width:100%}}
.bar i{{display:block;height:100%;width:0;border-radius:9px;background:linear-gradient(90deg,#E0A800,{TOK['yellow']});
  box-shadow:0 0 22px rgba(255,199,39,.7)}}
.stampbox{{position:relative}}
.stamp{{position:absolute;right:46px;top:-128px;z-index:6;font-family:'Inter Display','Inter';font-weight:900;font-style:italic;
  font-size:66px;line-height:1;color:{TOK['red']};border:7px solid {TOK['red']};border-radius:12px;padding:6px 20px 4px;
  transform:rotate(-12deg);letter-spacing:3px;text-shadow:none;background:rgba(10,14,24,.35)}}
.mk{{background-image:linear-gradient({TOK['yellow']},{TOK['yellow']});background-repeat:no-repeat;background-size:0% 100%;
  border-radius:6px;padding:0 .14em;margin:0 -.04em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.sheen{{position:absolute;inset:0;pointer-events:none;background:linear-gradient(100deg,transparent 35%,rgba(255,255,255,.95) 50%,transparent 65%);
  background-size:300% 100%;background-position:150% 0;-webkit-background-clip:text;background-clip:text}}
.sheen,.sheen *{{color:transparent!important;-webkit-text-fill-color:transparent;text-shadow:none!important}}
.big.slotbig{{display:flex;align-items:flex-start;text-shadow:none;filter:drop-shadow(0 0 34px rgba(255,199,39,.45))}}
.sl,.nd{{display:inline-block;height:1.2em;line-height:1.05em;overflow:hidden;text-shadow:0 10px 0 {TOK['blue']}}}
.sl{{-webkit-mask-image:linear-gradient(transparent 0,#000 14%,#000 86%,transparent 100%);mask-image:linear-gradient(transparent 0,#000 14%,#000 86%,transparent 100%)}}
.sl .col{{display:block}} .sl .col i{{display:block;height:1.6em;font-style:inherit;text-align:center;margin:0 -.3em}}
@keyframes kUp{{from{{opacity:0;transform:translateY(.42em);filter:blur(10px)}}to{{opacity:1;transform:none;filter:none}}}}
@keyframes kRise{{from{{transform:translateY(118%) rotate(4deg)}}to{{transform:none}}}}
@keyframes kMask{{0%,99.9%{{clip-path:inset(-1em -1em 0 -1em)}}100%{{clip-path:none}}}}
@keyframes kDrop{{from{{opacity:0;transform:translateY(-.7em) rotate(-14deg)}}to{{opacity:1;transform:none}}}}
@keyframes kZoom{{from{{opacity:0;transform:scale(1.9);filter:blur(16px)}}to{{opacity:1;transform:none;filter:none}}}}
@keyframes kSkewIn{{from{{opacity:0;transform:translateX(1.3em) skewX(-22deg)}}to{{opacity:1;transform:none}}}}
@keyframes kFlash{{0%,100%{{filter:none}}35%{{filter:brightness(1.4) drop-shadow(0 0 28px rgba(255,199,39,.75))}}}}
@keyframes kChip{{from{{opacity:0;transform:skew(-8deg) translateX(-70px)}}to{{opacity:1;transform:skew(-8deg)}}}}
@keyframes kBrush{{from{{clip-path:inset(0 100% 0 0)}}to{{clip-path:inset(0 0 0 0)}}}}
@keyframes kStrike{{from{{background-size:0% 4px}}to{{background-size:100% 4px}}}}
@keyframes kPop{{0%{{opacity:0;transform:scale(.55)}}60%{{opacity:1;transform:scale(1.07)}}100%{{opacity:1;transform:none}}}}
@keyframes kPunch{{from{{transform:scale(1.12)}}to{{transform:none}}}}
@keyframes kSheen{{from{{background-position:150% 0}}to{{background-position:-50% 0}}}}
@keyframes kFade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes kSlide{{from{{opacity:0;transform:translateX(-80px)}}to{{opacity:1;transform:none}}}}
@keyframes kGrow{{from{{transform:scaleX(0)}}to{{transform:none}}}}
@keyframes kHi{{from{{color:{TOK['text']};text-shadow:none}}50%{{text-shadow:0 0 34px rgba(255,199,39,.95)}}to{{color:{TOK['yellow']}}}}}
@keyframes kMarker{{0%{{background-size:0% 100%;color:{TOK['text']}}}45%{{color:{TOK['text']}}}100%{{background-size:100% 100%;color:{TOK['bg0']}}}}}
@keyframes kRysuj{{from{{stroke-dashoffset:1;fill-opacity:0}}70%{{stroke-dashoffset:0;fill-opacity:0}}to{{stroke-dashoffset:0;fill-opacity:1}}}}
@keyframes kWyr{{from{{fill:rgba(47,107,255,.16);stroke:{TOK['blue']}}}to{{fill:{TOK['yellow']};stroke:{TOK['yellow']}}}}}
@keyframes kPkt{{0%{{transform:scale(0)}}60%{{transform:scale(1.35)}}100%{{transform:scale(1)}}}}
@keyframes kPing{{from{{r:16;opacity:.9}}to{{r:70;opacity:0}}}}
@keyframes kMarkerDoc{{0%{{background-size:0% 100%;color:#121826}}100%{{background-size:100% 100%;color:#121826}}}}
@keyframes kStamp{{0%{{opacity:0;transform:rotate(-12deg) scale(2.8)}}55%{{opacity:1;transform:rotate(-12deg) scale(.9)}}100%{{opacity:1;transform:rotate(-12deg) scale(1)}}}}
@keyframes kShake{{0%,100%{{transform:none}}20%{{transform:translateX(-16px)}}40%{{transform:translateX(14px)}}60%{{transform:translateX(-9px)}}80%{{transform:translateX(5px)}}}}
@keyframes kDim{{from{{opacity:1}}to{{opacity:.45}}}}
.big,.num{{transform-origin:left center}} .center .big{{transform-origin:center}}
.beam{{position:absolute;top:-30%;left:0;width:46%;height:160%;transform-origin:center;pointer-events:none;
  background:linear-gradient(90deg,transparent,rgba(91,140,255,.20) 35%,rgba(255,255,255,.13) 50%,rgba(91,140,255,.20) 65%,transparent);filter:blur(10px)}}
.grad{{position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse 80% 55% at 50% 38%,rgba(47,107,255,.30),transparent 70%)}}
.brk{{position:absolute;z-index:7;pointer-events:none;opacity:0}}
.brk i{{position:absolute;width:64px;height:64px;border:0 solid {TOK['yellow']};filter:drop-shadow(0 0 12px rgba(255,199,39,.6))}}
.brk i:nth-child(1){{left:0;top:0;border-left-width:9px;border-top-width:9px}}
.brk i:nth-child(2){{right:0;top:0;border-right-width:9px;border-top-width:9px}}
.brk i:nth-child(3){{left:0;bottom:0;border-left-width:9px;border-bottom-width:9px}}
.brk i:nth-child(4){{right:0;bottom:0;border-right-width:9px;border-bottom-width:9px}}
.lbox{{position:absolute;left:0;width:100%;z-index:18;background:#05070D;pointer-events:none}}
.scanl{{position:absolute;left:0;width:100%;height:10px;z-index:8;pointer-events:none;
  background:linear-gradient(90deg,transparent,{TOK['yellow']} 20%,#fff 50%,{TOK['yellow']} 80%,transparent);
  box-shadow:0 0 40px 10px rgba(255,199,39,.55),0 -120px 120px -40px rgba(255,199,39,.18)}}
.tl{{position:relative;margin-top:10px;padding-left:64px}}
.tl-line{{position:absolute;left:18px;top:12px;bottom:12px;width:6px;border-radius:3px;transform-origin:top;
  background:linear-gradient(180deg,{TOK['yellow']},{TOK['blue']})}}
.tl-it{{position:relative;margin:0 0 34px}}
.tl-dot{{position:absolute;left:-58px;top:.35em;width:30px;height:30px;border-radius:50%;background:{TOK['yellow']};
  box-shadow:0 0 0 7px rgba(255,199,39,.22),0 0 26px rgba(255,199,39,.7)}}
.q-mark{{font-family:'Inter Display','Inter';font-weight:900;font-style:italic;font-size:240px;line-height:1;color:{TOK['yellow']};
  text-shadow:0 10px 0 {TOK['blue']};height:150px;margin:-60px 0 18px;overflow:visible;transform-origin:left center}}
@keyframes kZoomOut{{from{{transform:scale(1.14);filter:blur(2px)}}to{{transform:none;filter:none}}}}
@keyframes kCutL{{0%,100%{{transform:none}}45%{{transform:translateX(-46px) skewX(-6deg)}}}}
@keyframes kCutR{{0%,100%{{transform:none}}45%{{transform:translateX(46px) skewX(-6deg)}}}}
@keyframes kBrk{{0%{{opacity:0;transform:scale(1.45)}}70%{{opacity:1;transform:scale(.97)}}100%{{opacity:1;transform:none}}}}
@keyframes kLbox{{from{{height:16%}}to{{height:0}}}}
@keyframes kScan{{from{{top:18%;opacity:1}}85%{{opacity:1}}to{{top:74%;opacity:0}}}}
@keyframes kSrc{{from{{clip-path:inset(0 100% 0 0);transform:translateX(-12px)}}to{{clip-path:inset(0 0 0 0);transform:none}}}}
@keyframes kGrowY{{from{{transform:scaleY(0)}}to{{transform:none}}}}
@keyframes kDocIn{{from{{opacity:0;transform:perspective(1400px) rotateX(28deg) translateY(120px) scale(.9)}}to{{opacity:1;transform:none}}}}
@keyframes kFotoIn{{from{{clip-path:inset(0 0 100% 0);opacity:.2}}to{{clip-path:inset(0 0 0 0);opacity:1}}}}
@keyframes kFotoPel{{from{{clip-path:inset(50% 0 50% 0)}}to{{clip-path:inset(0 0 0 0)}}}}
.row .fill{{transform-origin:left center}}
.leak{{position:absolute;top:-10%;left:-100%;width:300%;height:120%;z-index:19;pointer-events:none;display:none;mix-blend-mode:screen;
  background:linear-gradient(105deg,transparent 30%,rgba(255,170,40,.35) 40%,rgba(255,214,90,.9) 47%,#fff 50%,rgba(255,199,39,.85) 53%,rgba(229,57,53,.25) 60%,transparent 70%)}}
.wsk-svg{{position:absolute;left:0;top:0;overflow:visible;pointer-events:none;z-index:4}}
.wsk-svg path{{fill:none;stroke:{TOK['yellow']};stroke-width:6;stroke-linecap:round;stroke-linejoin:round;
  filter:drop-shadow(0 0 10px rgba(255,199,39,.7))}}
.wsk-svg circle{{fill:{TOK['yellow']};filter:drop-shadow(0 0 12px rgba(255,199,39,.9))}}
"""


PREP = r"""
(o) => {
  const fx = o.fx, c = document.querySelector('.content'), W = innerWidth, H = innerHeight;
  const EASE = 'cubic-bezier(.2,.8,.2,1)';
  const ev = [];                                   // zdarzenia do synchronizacji dźwięku
  const anim = (el, name, dur, delay, add) => {
    const a = `${name} ${dur}s ${EASE} ${delay.toFixed(3)}s both`;
    el.style.animation = add && el.style.animation ? el.style.animation + ', ' + a : a;
  };
  // deterministyczny generator liczb losowych (ten sam spec = te same gwiazdy i iskry)
  let seed = o.seed >>> 0;
  const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };

  const split = (el, mode) => {                     // mode: 'w' słowa, 'm' słowa w masce, 'c' litery
    const walk = (n) => [...n.childNodes].forEach(ch => {
      if (ch.nodeType === 3) {
        const frag = document.createDocumentFragment();
        ch.textContent.split(/( +)/).forEach(p => {
          if (!p) return;
          if (/^ +$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
          const s = document.createElement('span'); s.className = 'w';
          if (mode === 'c') [...p].forEach(L => { const q = document.createElement('span'); q.className = 'ch'; q.textContent = L; s.appendChild(q); });
          else s.textContent = p;
          if (mode === 'm') { const m = document.createElement('span'); m.className = 'm'; m.appendChild(s); frag.appendChild(m); }
          else frag.appendChild(s);
        });
        n.replaceChild(frag, ch);
      } else if (ch.nodeType === 1 && ch.tagName !== 'BR' && !ch.classList.contains('m') && !ch.classList.contains('w')) walk(ch);
    });
    walk(el);
    return [...el.querySelectorAll(mode === 'c' ? '.ch' : '.w')];
  };

  // ── tło: warstwa efektów (ciągła między planszami – liczona z czasu globalnego g)
  const bg = document.createElement('div'); bg.className = 'fxbg';
  document.querySelector('.vig').before(bg);
  let cv = null, ctx = null, stars = [], orbs = [];
  if (fx.tlo === '3d') {
    // klatka renderu 3D podmieniana z Pythona dla każdej klatki filmu (czas globalny g); przyciemnienie pod tekstem
    const im = document.createElement('img'); im.className = 't3d'; bg.appendChild(im);
    const sh = document.createElement('div'); sh.className = 't3dv'; bg.appendChild(sh);
    // drobne podpisy (źródło, dopisek prawny) czytelne także na jasnej felgi/śniegu
    const st3 = document.createElement('style');
    st3.textContent = '.src{color:#D5DCEC!important;text-shadow:0 0 4px rgba(0,0,0,.95),0 2px 14px rgba(0,0,0,.9)}.src:before{background:#D5DCEC!important}';
    document.head.appendChild(st3);
    window.__t3d = (src, op) => { im.style.opacity = op; im.src = src; return im.decode().catch(() => {}); };
  } else if (fx.tlo === 'gwiazdy' || fx.tlo === 'siatka') {
    const dpr = devicePixelRatio || 1;            // 4K: płótno w pełnej rozdzielczości, rysowanie w px CSS
    cv = document.createElement('canvas'); cv.width = W * dpr; cv.height = H * dpr;
    cv.style.width = W + 'px'; cv.style.height = H + 'px'; bg.appendChild(cv); ctx = cv.getContext('2d'); ctx.scale(dpr, dpr);
    let s2 = 9173; const r2 = () => { s2 = (s2 * 1664525 + 1013904223) >>> 0; return s2 / 4294967296; };
    for (let k = 0; k < 170; k++) stars.push({x: r2() * W, y: r2() * H, z: .25 + r2() * .75, ph: r2() * 6.28, sp: .6 + r2() * 2});
  } else {
    [['rgba(47,107,255,.34)', 520], ['rgba(255,199,39,.10)', 380], ['rgba(91,140,255,.22)', 440]].forEach(([col, sz], k) => {
      const d = document.createElement('div'); d.className = 'orb';
      Object.assign(d.style, {width: sz + 'px', height: sz + 'px', background: col}); bg.appendChild(d); orbs.push({d, k, sz});
    });
  }
  let beam = null, grad = null;
  if (fx.swiatlo) {
    grad = document.createElement('div'); grad.className = 'grad'; bg.appendChild(grad);
    beam = document.createElement('div'); beam.className = 'beam'; bg.appendChild(beam);
  }
  let kontur = null;
  if (fx.kontur) {
    kontur = document.createElement('div'); kontur.className = 'kontur';
    const big = c.querySelector('.big');
    kontur.textContent = big ? big.textContent.trim() : (o.subject || '');
    bg.appendChild(kontur);
  }

  // ── liczniki, iskry, wstrząsy
  window.__counters = []; window.__slots = []; window.__bars = []; window.__sparks = []; window.__shakes = [];
  window.__brk = []; window.__focus = []; window.__rgb = []; window.__dolly = null; window.__wsk = null; window.__flashes = [];
  const addCounter = (el, start, dur) => {
    if (!o.count) return;
    const nodes = []; const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    while (tw.nextNode()) if (/\d/.test(tw.currentNode.textContent)) nodes.push({node: tw.currentNode, orig: tw.currentNode.textContent});
    if (nodes.length) window.__counters.push({nodes, start, dur});
  };
  const impact = (el, t0, amp) => {
    window.__shakes.push({t0, amp: fx.moc === 'mocna' ? amp * 1.6 : amp});
    const sp = [];
    for (let k = 0; k < 16; k++) {
      const s = document.createElement('i'); s.className = 'spark'; document.body.appendChild(s);
      sp.push({s, a: rnd() * 6.283, d: 160 + rnd() * 260, len: .55 + rnd() * .5});
    }
    window.__sparks.push({el, t0, sp});
    if (fx.rgb) window.__rgb.push({t0, amp: 10});
    ev.push({t: t0, typ: 'uderzenie'});
  };

  let t = 0;
  if (o.first) c.querySelectorAll('.cstamp').forEach(st => {       // pieczątka na okładce – wbita w 0,55 s
    anim(st, 'kStamp', .38, .55); window.__shakes.push({t0: .76, amp: fx.moc === 'mocna' ? 24 : 14}); ev.push({t: .76, typ: 'pieczatka'});
  });
  if (!o.enter) {
    c.querySelectorAll('.cd').forEach(el => { anim(el, 'kPop', .45, 0); ev.push({t: 0, typ: 'tik'}); });
    c.querySelectorAll('.opt.bad').forEach(el => { anim(el, 'kShake', .5, .1); ev.push({t: .1, typ: 'zle'}); });
    c.querySelectorAll('.opt.dim').forEach(el => anim(el, 'kDim', .4, .1));
  } else {
    const hw = [...c.querySelectorAll('h1,h2')].reduce((a, e) => a + e.innerText.split(/\s+/).length, 0) || 1;
    const hc = [...c.querySelectorAll('h1,h2')].reduce((a, e) => a + e.innerText.replace(/\s/g, '').length, 0) || 1;
    const bw = [...c.querySelectorAll('.sub,.body,.opt')].reduce((a, e) => a + e.innerText.split(/\s+/).length, 0) || 1;
    const sh = Math.min(.075, .55 / hw), sc = Math.min(.032, .7 / hc), sb = Math.min(.035, .75 / bw);
    c.querySelectorAll('.chip,.tag,.num,h1,h2,.brush,.big,.myth,.sub,.body,.opt,.row,.cd,.note,.src,.partner,.tl,.q-mark,.q-txt,.q-who,.doc,.doc-wsk,.foto,.foto-pod,.mapa').forEach(el => {
      if (el.matches('.chip,.tag')) {
        if (!o.first) { anim(el, 'kChip', .38, t); ev.push({t, typ: 'etykieta'}); t += .14; }
      } else if (el.matches('h1,h2')) {
        if (o.first) {                                  // haczyk widoczny od klatki 0
          el.style.transformOrigin = 'left center'; anim(el, 'kPunch', .55, 0); ev.push({t: 0, typ: 'start'});
          const ot = fx.otwarcie || fx.haczyk;
          if (ot === 'zoomout') { el.style.transformOrigin = 'center center'; anim(el, 'kZoomOut', .45, 0, true); }
          else if (ot === 'ciecie') {                   // cięcie liniami: pytanie z lewej, żółty akcent z prawej – czytelne od klatki 0
            const ac = el.querySelector('.y'); split(el, 'w').forEach(w => anim(w, ac && ac.contains(w) ? 'kCutR' : 'kCutL', .34, .22));
            window.__shakes.push({t0: .56, amp: fx.moc === 'mocna' ? 14 : 8}); ev.push({t: .56, typ: 'uderzenie'}); }
          else if (ot === 'skan') {
            const sl = document.createElement('div'); sl.className = 'scanl'; document.body.appendChild(sl);
            anim(sl, 'kScan', .75, .05); ev.push({t: .05, typ: 'marker'});
          } else if (ot === 'ramka') {
            window.__brk.push({el, t0: .3}); window.__shakes.push({t0: .55, amp: fx.moc === 'mocna' ? 16 : 9}); ev.push({t: .55, typ: 'uderzenie'});
          } else if (ot === 'rgb') {                  // rozszczepienie kanałów (czerwień/niebieski marki): od klatki 0 czytelne, 2 uderzenia
            window.__rgb.push({t0: 0, amp: 16, k: 6}); window.__rgb.push({t0: .52, amp: 15, k: 6}); window.__rgb.push({t0: 1.45, amp: 8});
            anim(el, 'kPunch', .45, .52, true);          // drugie uderzenie: haczyk „uderza” w ekran
            window.__shakes.push({t0: .52, amp: fx.moc === 'mocna' ? 18 : 10}); ev.push({t: .52, typ: 'uderzenie'});
            ev.push({t: 1.45, typ: 'tik'});
          } else if (ot === 'kinowe') {
            ['top', 'bottom'].forEach(side => { const b = document.createElement('div'); b.className = 'lbox'; b.style[side] = 0;
              document.body.appendChild(b); anim(b, 'kLbox', .7, .1); });
            ev.push({t: .1, typ: 'start'});
          }
          if (ot === 'blysk') {
            el.style.position = 'relative';
            const sh2 = document.createElement('span'); sh2.className = 'sheen'; sh2.innerHTML = el.innerHTML;
            el.appendChild(sh2); anim(sh2, 'kSheen', .9, .35);
          }
        } else {
          ev.push({t, typ: 'naglowek'});
          if (fx.naglowek === 'litery') {
            split(el, 'c').forEach((L, k) => anim(L, 'kDrop', .42, t + k * sc)); t += hc * sc + .2;
          } else if (fx.naglowek === 'zoom') {
            split(el, 'w').forEach((w, k) => anim(w, 'kZoom', .5, t + k * sh)); t += hw * sh + .2;
          } else if (fx.naglowek === 'przesun') {
            split(el, 'w').forEach((w, k) => anim(w, 'kSkewIn', .48, t + k * sh)); t += hw * sh + .18;
          } else {
            split(el, 'm').forEach((w, k) => { anim(w, 'kRise', .55, t + k * sh); anim(w.parentNode, 'kMask', .55, t + k * sh); });
            t += hw * sh + .15;
          }
        }
      } else if (el.matches('.brush')) {
        anim(el, 'kBrush', .42, o.first ? .12 : t); t += .12;
      } else if (el.matches('.big')) {
        const t0 = o.first ? 0 : t;
        const txt = el.textContent, val = parseFloat((txt.match(/\d+(?:[.,]\d+)?/) || ['0'])[0].replace(',', '.'));
        if (!o.first) anim(el, 'kPop', .5, t0);
        let land = t0 + .35;
        if (o.count && fx.liczba === 'slot' && /\d/.test(txt)) {
          // licznik jak w jednorękim bandycie: każda cyfra kręci się i ląduje, od lewej do prawej
          el.classList.add('slotbig');
          const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), nodes = [];
          while (tw.nextNode()) nodes.push(tw.currentNode);
          let ci = 0; const digits = (txt.match(/\d/g) || []).length;
          nodes.forEach(nd => {
            const frag = document.createDocumentFragment();
            [...nd.textContent].forEach(chr => {
              if (/\d/.test(chr)) {
                const d = +chr, spins = 1 + (digits - ci - 1 > 0 ? 1 : 0), seq = [];
                for (let s = 0; s < spins * 10 + d + 1; s++) seq.push(s % 10);
                const sl = document.createElement('span'); sl.className = 'sl';
                const col = document.createElement('span'); col.className = 'col';
                col.innerHTML = seq.map(x => `<i>${x}</i>`).join(''); sl.appendChild(col); frag.appendChild(sl);
                window.__slots.push({col, n: seq.length - 1, start: t0 + .05 + ci * .12, dur: .9 + ci * .08, sl, d});
                land = Math.max(land, t0 + .05 + ci * .12 + .9 + ci * .08); ci++;
              } else { const s = document.createElement('span'); s.className = 'nd'; s.textContent = /\s/.test(chr) ? '\u00a0' : chr; frag.appendChild(s); }
            });
            nd.replaceWith(frag);
          });
          // każda kolumna ma szerokość swojej docelowej cyfry (w em) – „1” nie zostawia dziury jak „1 00”
          window.__slots.filter(q => q.sl && el.contains(q.sl)).forEach(q => {
            const m = document.createElement('span'); m.className = 'nd'; m.textContent = String(q.d); el.appendChild(m);
            q.sl.style.width = (m.offsetWidth / parseFloat(getComputedStyle(m).fontSize)).toFixed(4) + 'em';
            m.remove();
          });
        } else {
          addCounter(el, t0, .9); if (o.count && /\d/.test(txt)) land = t0 + .9;
        }
        if (/%/.test(txt) && val > 0 && val <= 100) {   // pasek postępu dla procentów
          const bar = document.createElement('div'); bar.className = 'bar'; bar.innerHTML = '<i></i>'; el.after(bar);
          window.__bars.push({i: bar.firstChild, val, start: t0 + .05, dur: land - t0 - .05});
        }
        anim(el, 'kFlash', .6, land - .05, true);
        impact(el, land, o.first ? 6 : 12);
        if (!o.first && fx.akcent === 'ramka') window.__brk.push({el, t0: land - .12});
        if (!o.first && fx.akcent === 'ostrosc') window.__focus.push(land);
        t += .32;
      } else if (el.matches('.num,.cd')) {
        anim(el, 'kPop', .5, t); ev.push({t, typ: 'pop'}); t += .32;
      } else if (el.matches('.myth')) {
        anim(el, 'kFade', .3, t);
        el.querySelectorAll('span').forEach(s => anim(s, 'kStrike', .5, t + .3));
        ev.push({t: t + .3, typ: 'przekreslenie'});
        if (fx.mit === 'pieczatka') {
          el.classList.add('stampbox');
          const st = document.createElement('div'); st.className = 'stamp'; st.textContent = 'MIT'; el.appendChild(st);
          anim(st, 'kStamp', .38, t + .75); window.__shakes.push({t0: t + .96, amp: fx.moc === 'mocna' ? 22 : 14}); ev.push({t: t + .96, typ: 'pieczatka'});
          t += .5;
        }
        t += .75;
      } else if (el.matches('.sub,.body,.opt')) {
        if (o.first) t = Math.max(t, .35);
        if (el.matches('.opt')) { anim(el, 'kSlide', .4, t); ev.push({t, typ: 'etykieta'}); t += .16; return; }
        const ws = split(el, 'w');
        ws.forEach((w, k) => anim(w, 'kUp', .42, t + k * sb));
        if (!o.first) ev.push({t, typ: 'tekst'});
        el.querySelectorAll('b').forEach(b => {
          const k = Math.max(0, ws.indexOf(b.querySelector('.w'))), tb = t + k * sb + .3;
          if (fx.tresc === 'marker') { b.classList.add('mk'); anim(b, 'kMarker', .5, tb); ev.push({t: tb, typ: 'marker'}); }
          else anim(b, 'kHi', .55, tb);
        });
        t += ws.length * sb + .1;
      } else if (el.matches('.tl')) {                 // oś czasu: linia się rysuje, punkty wskakują po kolei
        const ln = el.querySelector('.tl-line'); if (ln) anim(ln, 'kGrowY', .9, t);
        el.querySelectorAll('.tl-it').forEach((it, k) => {
          const tk = t + .15 + k * .32;
          anim(it, 'kSlide', .42, tk); const d = it.querySelector('.tl-dot'); if (d) anim(d, 'kPop', .4, tk);
          ev.push({t: tk, typ: 'pop'});
        });
        t += .15 + el.querySelectorAll('.tl-it').length * .32 + .2;
      } else if (el.matches('.doc')) {                // odsłonięcie dokumentu: wjazd w perspektywie, potem marker na wyróżnieniach
        anim(el, 'kDocIn', .7, t); ev.push({t: t + .5, typ: 'uderzenie'}); window.__shakes.push({t0: t + .62, amp: 6});
        const tx2 = el.querySelector('.doc-t'), ws = tx2 ? split(tx2, 'w') : [];
        let tb = t + .8;
        el.querySelectorAll('.doc-t b').forEach(b => { b.classList.add('mk'); anim(b, 'kMarkerDoc', .55, tb);   // ciemny tekst na jasnej karcie – słowo widoczne także przed markerem
 ev.push({t: tb, typ: 'marker'}); tb += .45; });
        const fb2 = el.querySelector('.doc-t b');
        if (fb2) window.__dolly = {el: fb2, t0: tb + .05, amt: fx.moc === 'mocna' ? .13 : .08};   // „kamera” najeżdża na dosłowny fragment
        t = tb + .1;
      } else if (el.matches('.mapa')) {               // mapa: kontury się rysują, wyróżnienie zalewa żółtym, punkty wskakują z falą, kamera na pierwszy punkt
        el.querySelectorAll('.obs').forEach((p, k) => anim(p, 'kRysuj', 1.0, t + Math.min(.5, k * .025)));
        let tm = t + 1.05;
        const wy = [...el.querySelectorAll('.obs.wyr')];
        wy.forEach(p => anim(p, 'kWyr', .5, tm, true));
        if (wy.length) { ev.push({t: tm, typ: 'uderzenie'}); window.__shakes.push({t0: tm + .1, amp: 5}); tm += .45; }
        el.querySelectorAll('.pkt').forEach(g => { anim(g, 'kPkt', .45, tm); ev.push({t: tm, typ: 'pop'});
          const r = g.querySelector('.pk-r'); if (r) { r.style.animation = `kPing 1.2s ease-out ${tm.toFixed(2)}s infinite both`; } tm += .35; });
        const cel = el.querySelector('.pkt .pk-d') || wy[0];
        if (cel) window.__dolly = {el: cel, t0: tm, amt: fx.moc === 'mocna' ? .22 : .12};
        t = tm + .1;
      } else if (el.matches('.foto')) {               // odbitka zdjęcia: odsłonięcie maską od góry + krótki błysk
        anim(el, 'kFotoIn', .6, t); ev.push({t: t + .35, typ: 'uderzenie'}); window.__flashes.push(t + .35); t += .55;
      } else if (el.matches('.foto-pod')) {
        anim(el, 'kSrc', .45, t); t += .15;
      } else if (el.matches('.doc-wsk')) {            // wskazanie szczegółu: linia rysuje się od wyróżnienia do etykiety
        const fb3 = c.querySelector('.doc-t b');
        if (fb3) {
          const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); svg.setAttribute('class', 'wsk-svg');
          svg.innerHTML = '<path pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/><circle r="11"/>'; c.appendChild(svg);
          window.__wsk = {svg, from: fb3, to: el, t0: t};
          ev.push({t, typ: 'marker'});
        }
        anim(el, 'kPop', .45, t + .42); ev.push({t: t + .45, typ: 'pop'});
        t += .7;
      } else if (el.matches('.q-mark')) {
        anim(el, 'kStamp', .4, t); window.__shakes.push({t0: t + .22, amp: 8}); ev.push({t: t + .22, typ: 'pieczatka'}); t += .3;
      } else if (el.matches('.q-txt')) {
        const ws = split(el, 'w'); ws.forEach((w, k) => anim(w, 'kUp', .42, t + k * sb)); ev.push({t, typ: 'tekst'});
        el.querySelectorAll('b').forEach(b => { const k = Math.max(0, ws.indexOf(b.querySelector('.w'))); b.classList.add('mk'); anim(b, 'kMarker', .5, t + k * sb + .3); });
        t += ws.length * sb + .15;
      } else if (el.matches('.q-who')) {
        anim(el, 'kSlide', .42, t); t += .2;
      } else if (el.matches('.src')) {                 // znacznik źródła: odsłonięcie od lewej
        anim(el, 'kSrc', .5, t); t += .1;
      } else if (el.matches('.row')) {
        anim(el, 'kFade', .3, t);
        el.querySelectorAll('.fill').forEach(f => anim(f, 'kGrow', .65, t + .05));
        el.querySelectorAll('.n').forEach(n => addCounter(n, t + .05, .65));
        ev.push({t, typ: 'pop'}); t += .14;
      } else {
        anim(el, 'kFade', .4, t); t += .08;
      }
    });
  }

  // ── stop-klatka na zwrocie akcji: krótkie zatrzymanie – błysk, przyciemnienie tła, najazd (fx.zwrot = "stop" | "brak")
  window.__stop = [];
  const isTwist = [...c.querySelectorAll('.tag')].some(e => /TWIST|ZWROT/i.test(e.textContent));
  if (!o.first && o.enter && isTwist && (fx.zwrot || 'stop') === 'stop') {
    const ts2 = Math.max(.35, t - .25); window.__stop.push(ts2); window.__rgb.push({t0: ts2, amp: 9}); ev.push({t: ts2, typ: 'uderzenie'});
  }

  // ── drugi akcent w trakcie czytania (co 2–3 s coś się dzieje): najazd kamery + błysk liczby / żółtego słowa
  window.__pulse = [];
  if (fx.moc === 'mocna' && !o.first && o.enter) {
    const tp = Math.max(t + 1.6, 2.2);
    window.__pulse.push(tp);
    const hi = c.querySelector('.big') || c.querySelector('h2 .y, .q-txt b, .tl-it:last-child .tl-y, .body b');
    if (hi) { anim(hi, 'kFlash', .6, tp, true); ev.push({t: tp, typ: 'tik'}); }
  }

  // ── przejścia
  const wipe = document.createElement('div'); wipe.className = 'wipe';
  wipe.innerHTML = '<i class="wb"></i><i class="wy"></i><i class="wy2"></i>'; document.body.appendChild(wipe);
  const slats = document.createElement('div'); slats.className = 'slats';
  for (let k = 0; k < 5; k++) { const s = document.createElement('i'); s.style.top = (k * H / 5 - 1) + 'px'; s.style.height = (H / 5 + 2) + 'px'; slats.appendChild(s); }
  document.body.appendChild(slats);
  const flash = document.createElement('div'); flash.className = 'flash'; document.body.appendChild(flash);
  const leak = document.createElement('div'); leak.className = 'leak'; document.body.appendChild(leak);
  const hero = c.querySelector('.hero-ill');
  // zdjęcie (plansza „foto”): dwie warstwy – tył rozmyty i wolniejszy, przód ostry i szybszy → złudzenie głębi
  const fpel = document.querySelector('.fpel');
  if (fpel && o.enter) { fpel.style.animation = `kFotoPel .55s cubic-bezier(.2,.7,.2,1) 0s both`; ev.push({t: 0, typ: 'uderzenie'}); }
  const fB = document.querySelector('.foto-b'), fF = document.querySelector('.foto-f'), fPel = !!fpel;
  const fCala = document.querySelector('.foto-f.cala');   // CC BY-SA: całe zdjęcie bez kadrowania – rusza się cała odbitka, nie obraz w niej
  const fKarta = document.querySelector('.foto');
  const io = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  const clamp = x => Math.min(1, Math.max(0, x));
  let rects = null;
  window.__layout = () => {                          // pozycje po dopasowaniu tekstu (stan końcowy)
    const sv = [c.style.transform, c.style.translate, c.style.filter]; c.style.transform = ''; c.style.translate = '';
    const cr = c.getBoundingClientRect();
    if (window.__dolly) {                             // punkt najazdu = wyróżnienie, ale karta nie może wyjść z kadru
      const dl = window.__dolly, r = dl.el.getBoundingClientRect(), dc = (dl.el.closest('.doc') || c).getBoundingClientRect();
      const ox = dc.left + dc.width / 2, oy = r.top + r.height / 2, m = 50;   // poziomo środek karty, pionowo wyróżnienie
      const lim = [ox > dc.left ? (ox - m) / (ox - dc.left) : 9, dc.right > ox ? (W - m - ox) / (dc.right - ox) : 9,
                   oy > dc.top ? (oy - m) / (oy - dc.top) : 9];
      dl.amt = Math.max(0, Math.min(dl.amt, Math.min(...lim) - 1));
      dl.org = `${(ox - cr.left).toFixed(1)}px ${(oy - cr.top).toFixed(1)}px`; }
    if (window.__wsk) {                               // łamana: spod wyróżnienia w dół, w bok, do etykiety
      const a = window.__wsk.from.getBoundingClientRect(), b = window.__wsk.to.getBoundingClientRect();
      const dk = window.__wsk.from.closest('.doc'), db = dk ? dk.getBoundingClientRect().bottom : a.bottom;
      // start na dolnej krawędzi karty pod wyróżnieniem – linia nie przecina tekstu dokumentu
      const x1 = a.left - cr.left + a.width / 2, y1 = db - cr.top + 2, x2 = b.left - cr.left + 40, y2 = b.top - cr.top - 6;
      const ym = Math.max(y1 + 30, y2 - 60);
      const s = window.__wsk.svg; s.setAttribute('width', cr.width); s.setAttribute('height', cr.height);
      s.querySelector('path').setAttribute('d', `M${x1.toFixed(1)} ${y1.toFixed(1)} L${x1.toFixed(1)} ${ym.toFixed(1)} L${x2.toFixed(1)} ${ym.toFixed(1)} L${x2.toFixed(1)} ${y2.toFixed(1)}`);
      const ci = s.querySelector('circle'); ci.setAttribute('cx', x1.toFixed(1)); ci.setAttribute('cy', y1.toFixed(1));
    }
    c.style.transform = sv[0]; c.style.translate = sv[1];
    rects = window.__sparks.map(s => { const r = s.el.getBoundingClientRect(); return {x: r.left + r.width / 2, y: r.top + r.height / 2}; });
    window.__brk.forEach(b => {                       // ramka ostrości wokół elementu (stan końcowy, z zapasem)
      const r = b.el.getBoundingClientRect(), pad = 26;
      if (!b.box) { b.box = document.createElement('div'); b.box.className = 'brk'; b.box.innerHTML = '<i></i><i></i><i></i><i></i>'; document.body.appendChild(b.box); }
      Object.assign(b.box.style, {left: (r.left - pad) + 'px', top: (r.top - pad) + 'px', width: (r.width + 2 * pad) + 'px', height: (r.height + 2 * pad) + 'px'});
    });
  };

  window.__setT = (t, g, dur, exitT, enterT, push) => {
    document.getAnimations().forEach(a => { a.pause(); a.currentTime = t * 1000; });
    const tq = Math.floor(t * 30 + 1e-6) / 30;
    const RE = /\d{1,3}(?:[  ]\d{3})+|\d+(?:[.,]\d+)?/g;
    const fmt = (m, e) => {
      const grp = /[  ]/.test(m) ? m.match(/[  ]/)[0] : null;
      const dec = (m.match(/[.,](\d+)$/) || [, ''])[1].length, sep = dec ? m[m.length - dec - 1] : '';
      let s = (parseFloat(m.replace(/[  ]/g, '').replace(',', '.')) * e).toFixed(dec);
      if (sep === ',') s = s.replace('.', ',');
      if (grp) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, grp);
      return s;
    };
    window.__counters.forEach(cn => {
      const p = clamp((tq - cn.start) / cn.dur), e = 1 - Math.pow(1 - p, 3);
      cn.nodes.forEach(n => { n.node.textContent = p >= 1 ? n.orig : n.orig.replace(RE, m => fmt(m, e)); });
    });
    window.__slots.forEach(s => {
      const p = clamp((t - s.start) / s.dur), e = 1 - Math.pow(1 - p, 4);
      s.col.style.transform = `translateY(${-e * s.n * 1.6}em)`;
    });
    window.__bars.forEach(b => { const p = clamp((t - b.start) / b.dur); b.i.style.width = ((1 - Math.pow(1 - p, 3)) * b.val) + '%'; });
    // iskry: wylatują z liczby w chwili lądowania
    window.__sparks.forEach((s, k) => {
      const o0 = rects ? rects[k] : {x: W / 2, y: H / 2};
      s.sp.forEach(q => {
        const p = (t - s.t0) / q.len;
        if (p < 0 || p > 1) { q.s.style.opacity = 0; return; }
        const d = q.d * (1 - Math.pow(1 - p, 3));
        q.s.style.opacity = (1 - p).toFixed(3);
        q.s.style.transform = `translate(${o0.x + Math.cos(q.a) * d - 4}px,${o0.y + Math.sin(q.a) * d - 13}px) rotate(${q.a * 57.3 + 90}deg) scaleY(${1 - .6 * p})`;
      });
    });
    // wstrząs kadru przy uderzeniu (tłumiony)
    let sx = 0, sy = 0;
    window.__shakes.forEach(s => { const u = t - s.t0; if (u >= 0 && u < .35) { const a = s.amp * Math.exp(-u * 12); sx += a * Math.sin(u * 95); sy += a * .6 * Math.cos(u * 80); } });

    // przejścia: wyjście w ostatnich WT s planszy, wejście w pierwszych WT s następnej
    const WT = .24;
    const pOut = exitT && t > dur - WT ? io(clamp((t - (dur - WT)) / WT)) : null;     // 0 → 1
    const pIn = enterT && t < WT ? io(clamp(t / WT)) : null;                           // 0 → 1
    const mocna = fx.moc === 'mocna';
    let scale = push ? 1 + (mocna ? .045 : .025) * Math.min(1, t / dur) : 1, blur = 0, op = 1, tx = 0;
    if (mocna && fx.bpm) {          // puls na bicie muzyki – kadr „oddycha” z rytmem
      const bt = 60 / fx.bpm, ph = ((g % bt) + bt) % bt;
      scale *= 1 + .012 * Math.exp(-ph * 9);
    }
    wipe.style.display = 'none'; slats.style.display = 'none'; flash.style.opacity = 0; c.style.clipPath = '';
    // zmiana ostrości: przy lądowaniu liczby tło na chwilę rozmyte, uwaga na liczbie
    let fb = 0; window.__focus.forEach(f0 => { const u = t - f0; if (u > -.15) fb += 9 * Math.exp(-Math.max(0, u) * 2.2) * clamp((u + .15) / .15); });
    bg.style.filter = fb > .2 ? `blur(${fb.toFixed(1)}px)` : '';
    const kind = pOut !== null ? exitT : (pIn !== null ? enterT : null), q = pOut !== null ? pOut : pIn, isOut = pOut !== null;
    if (kind === 'smuga') {
      wipe.style.display = ''; const x = isOut ? -1 + q : q;
      [...wipe.children].forEach(e => e.style.translate = `${x * W * 2.4}px 0`);
    } else if (kind === 'zoom') {
      if (isOut) { scale *= 1 + .45 * q; blur = 18 * q; op = 1 - q; } else { scale *= .8 + .2 * q; blur = 18 * (1 - q); op = q; }
      flash.style.opacity = (isOut ? q : 1 - q) * .25;
    } else if (kind === 'paski') {
      slats.style.display = '';
      // jeden kierunek (z lewej w prawo), minimalne przesunięcie pasów – czyste zakrycie i odsłonięcie
      [...slats.children].forEach((s, k) => {
        const e = io(clamp(q * 1.15 - k * .03));
        const x = isOut ? -(1 - e) : e;
        s.style.transform = `translateX(${x * (W + 60)}px)`;
      });
    } else if (kind === 'blysk') {
      if (isOut) { tx = -W * .55 * q; blur = 22 * q; op = 1 - q; } else { tx = W * .55 * (1 - q); blur = 22 * (1 - q); op = q; }
      flash.style.opacity = (isOut ? q : 1 - q) * .3;
    } else if (kind === 'kierunek') {                 // szybki „obrót kamery” w lewo z rozmyciem ruchu
      if (isOut) { tx = -W * 1.15 * q; blur = 26 * q; } else { tx = W * 1.15 * (1 - q); blur = 26 * (1 - q); }
      wipe.style.display = ''; const x = isOut ? -1 + q : q;
      [...wipe.children].forEach((e, k) => e.style.translate = `${x * W * 2.4}px 0`);
      wipe.style.opacity = .55;
    } else if (kind === 'przeslona') {                // przesłona: kadr zamyka się i otwiera okręgiem
      const r = isOut ? 120 * (1 - q) : 120 * q;
      c.style.clipPath = `circle(${r.toFixed(1)}% at 50% 46%)`;
      flash.style.opacity = (isOut ? q : 1 - q) * .22;
    }
    let bright = 0;
    leak.style.display = 'none';
    if (kind === 'swiatlo') {                         // prześwietlenie złotym światłem (poświata z logo) – przejście „przez światło”
      leak.style.display = 'block'; const x = isOut ? (-1.2 + 1.2 * q) : 1.2 * q;
      leak.style.translate = `${(x * W).toFixed(1)}px 0`;
      if (isOut) { bright = 1.4 * q; blur = 7 * q; op = 1 - .85 * q; } else { bright = 1.4 * (1 - q); blur = 7 * (1 - q); op = .15 + .85 * q; }
    }
    const kids = [...c.children];
    if (kind === 'warstwy') {
      kids.forEach((e, k) => { const sp = 1 + k * .45, x = isOut ? -q * W * .9 * sp : (1 - q) * W * .9 * sp;
        e.style.translate = `${x.toFixed(1)}px 0`; e.style.opacity = (isOut ? 1 - q * .8 : .2 + .8 * q).toFixed(3); });
      blur = 8 * (isOut ? q : 1 - q);
    } else if (kids.length && kids[0].style.translate) kids.forEach(e => { e.style.translate = ''; e.style.opacity = ''; });
    if (kind !== 'kierunek') wipe.style.opacity = '';
    // ramki ostrości: wskakują z powiększenia, „oddychają” i znikają razem z treścią w przejściu
    let vis = pOut !== null ? 1 - pOut : (pIn !== null ? pIn : 1);
    if (kind === 'warstwy' || kind === 'swiatlo') vis = Math.pow(vis, 3);   // ramka nie zostaje „w powietrzu”, gdy treść odjeżdża
    window.__brk.forEach(b => { if (!b.box) return; const u = t - b.t0;
      if (u < 0) { b.box.style.opacity = 0; return; }
      const p = clamp(u / .35), e = 1 - Math.pow(1 - p, 3);
      b.box.style.opacity = (Math.min(1, p * 1.6) * vis).toFixed(3);
      // w przejściu „warstwy” ramka jedzie razem ze swoją warstwą (tą, w której jest liczba)
      if (b.kid === undefined) b.kid = [...c.children].find(k => k.contains(b.el)) || null;
      const lx = kind === 'warstwy' && b.kid ? parseFloat(b.kid.style.translate) || 0 : 0;
      b.box.style.translate = (tx || sx || sy || lx) ? `${(tx + sx + lx).toFixed(1)}px ${sy.toFixed(1)}px` : '';
      b.box.style.transform = `scale(${((1.45 - .45 * e + .012 * Math.sin(u * 4)) * scale).toFixed(4)})`; });
    let stopDim = 0;
    window.__stop.forEach(ts2 => { const u = t - ts2; if (u >= 0 && u < .9) {
      scale *= 1 + .06 * Math.exp(-u * 5); stopDim = Math.max(stopDim, .55 * Math.exp(-u * 3.5));
      flash.style.opacity = Math.max(+flash.style.opacity || 0, .5 * Math.exp(-u * 9)); } });
    bg.style.opacity = stopDim > .02 ? (1 - stopDim).toFixed(3) : '';
    window.__pulse.forEach(tp => { const u = t - tp; if (u > 0 && u < 1.2) scale *= 1 + .04 * Math.sin(Math.min(1, u / .18) * Math.PI / 2) * Math.exp(-u * 3.2); });
    // najazd „kamery” na dosłowny fragment dokumentu (punkt zaczepienia = wyróżnienie)
    const dl = window.__dolly;
    if (dl && dl.org) { const p = io(clamp((t - dl.t0) / 1.1)); scale *= 1 + dl.amt * p; c.style.transformOrigin = dl.org; }
    // linia wskazania: rysuje się w 0,45 s, kropka pulsuje
    const wk = window.__wsk;
    if (wk) { const p = clamp((t - wk.t0) / .45); wk.svg.querySelector('path').setAttribute('stroke-dashoffset', (1 - io(p)).toFixed(4));
      const ci = wk.svg.querySelector('circle'); ci.style.opacity = p > 0 ? 1 : 0; ci.setAttribute('r', (9 + 3 * Math.sin(t * 6)).toFixed(2)); }
    // głębia 2.5D: treść lekko pochylona w perspektywie (≤1,4°), tło przesuwa się w przeciwną stronę (paralaksa)
    let rx = 0, ry = 0;
    if (fx.glebia) { rx = .9 * Math.sin(g * .53); ry = 1.4 * Math.sin(g * .37); }
    const tf = (rx || ry ? `perspective(1800px) rotateX(${rx.toFixed(3)}deg) rotateY(${ry.toFixed(3)}deg) ` : '') + (scale !== 1 ? `scale(${scale})` : '');
    c.style.transform = tf;
    bg.style.translate = fx.glebia ? `${(-ry * 16).toFixed(1)}px ${(rx * 12).toFixed(1)}px` : '';
    if (hero) {                                       // obraz-bohater okładki na „bliższym planie”: rusza się szybciej niż tekst
      const u = push ? Math.min(1, t / dur) : 0;
      hero.style.scale = (1 + .07 * u).toFixed(4);
      hero.style.translate = `${(ry * 10).toFixed(1)}px ${(-26 * u + rx * 8).toFixed(1)}px`;
    }
    if (fB && fF) {                                   // paralaksa zdjęcia: tył 1,08→1,14, przód 1,00→1,10 i przesuw
      const u = clamp(t / Math.max(1, dur)), k = fPel ? 1.6 : 1;
      fB.style.transform = `scale(${(1.08 + .06 * u).toFixed(4)}) translate(${(ry * 6).toFixed(1)}px, ${((-10 + 20 * u) * k).toFixed(1)}px)`;
      fF.style.transform = `scale(${(1 + .10 * u).toFixed(4)}) translate(${((-30 * u) * k + ry * 12).toFixed(1)}px, ${((20 - 50 * u) * k + rx * 8).toFixed(1)}px)`;
      if (fpel) fpel.style.opacity = vis.toFixed(3);
    }
    if (fCala && fKarta) { const u = clamp(t / Math.max(1, dur));
      fKarta.style.translate = `${(ry * 8 - 12 * u).toFixed(1)}px ${(14 - 28 * u + rx * 6).toFixed(1)}px`; }
    window.__flashes.forEach(tf2 => { const u = t - tf2; if (u >= 0 && u < .4) flash.style.opacity = Math.max(+flash.style.opacity || 0, .35 * Math.exp(-u * 10)); });
    // rozszczepienie RGB w kolorach marki przy uderzeniach (gaśnie w ~0,3 s)
    let rg = 0; window.__rgb.forEach(r => { const u = t - r.t0; if (u >= 0 && u < .6) rg += r.amp * Math.exp(-u * (r.k || 9)); });
    const fl = [];
    if (blur) fl.push(`blur(${blur.toFixed(1)}px)`);
    if (bright > .01) fl.push(`brightness(${(1 + bright).toFixed(3)})`);
    if (rg > .4) fl.push(`drop-shadow(${rg.toFixed(1)}px 0 0 rgba(229,57,53,.8)) drop-shadow(${(-rg).toFixed(1)}px 0 0 rgba(47,107,255,.85))`);
    c.style.filter = fl.join(' ');
    c.style.opacity = op < 1 ? op.toFixed(3) : '';
    c.style.translate = (tx || sx || sy) ? `${(tx + sx).toFixed(1)}px ${sy.toFixed(1)}px` : '';

    // tło: gwiazdy / siatka / kule + wielki kontur, wszystko z czasu globalnego g
    if (ctx) {
      ctx.clearRect(0, 0, W, H);
      if (fx.tlo === 'gwiazdy') {
        stars.forEach(s => {
          const y = (s.y + g * 14 * s.z) % H, a = .25 + .55 * s.z * (.6 + .4 * Math.sin(g * s.sp + s.ph));
          ctx.fillStyle = `rgba(${s.z > .8 ? '255,236,180' : '210,225,255'},${a.toFixed(3)})`;
          ctx.beginPath(); ctx.arc(s.x, y, .6 + 1.9 * s.z, 0, 6.283); ctx.fill();
        });
      } else {
        ctx.strokeStyle = 'rgba(47,107,255,.16)'; ctx.lineWidth = 2;
        const hz = H * .62, off = (g * 40) % 90;
        for (let k = -12; k <= 12; k++) { ctx.beginPath(); ctx.moveTo(W / 2 + k * 40, hz); ctx.lineTo(W / 2 + k * 260, H); ctx.stroke(); }
        for (let k = 0; k < 14; k++) { const y = hz + Math.pow((k * 90 + off) / 1260, 2) * (H - hz) * 1.0; if (y > H) break;
          ctx.globalAlpha = Math.min(1, (y - hz) / 200); ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }
        ctx.globalAlpha = 1;
        ctx.strokeStyle = 'rgba(47,107,255,.07)';
        for (let x = (g * 12) % 120; x < W; x += 120) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, hz); ctx.stroke(); }
        for (let y = (g * 8) % 120; y < hz; y += 120) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }
      }
    }
    orbs.forEach(o2 => {
      const x = W * (.2 + .6 * (.5 + .5 * Math.sin(g * .35 + o2.k * 2.1))) - o2.sz / 2;
      const y = H * (.25 + .5 * (.5 + .5 * Math.cos(g * .28 + o2.k * 1.7))) - o2.sz / 2;
      o2.d.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px)`;
    });
    if (beam) beam.style.transform = `translateX(${((g * .11) % 1.6 * W * 1.6 - W * .9).toFixed(1)}px) rotate(18deg)`;
    if (grad) grad.style.opacity = (.55 + .45 * Math.sin(g * .7)).toFixed(3);
    if (kontur) kontur.style.transform = `translate(calc(-50% + ${(60 - g * 22).toFixed(1)}px), -58%) rotate(-8deg)`;
    document.querySelectorAll('.bg').forEach(e => e.style.transform = `scale(${1 + .004 * g})`);
    const gr = document.querySelector('.grain');
    if (gr) gr.style.backgroundPosition = `${(g * 7919) % 240}px ${(g * 6271) % 240}px`;
    document.querySelectorAll('.st').forEach((e, i) =>
      e.style.translate = `${Math.sin(g * .5 + i * 1.7) * 16}px ${Math.cos(g * .4 + i) * 8}px`);
  };
  return {t, ev};
}
"""
