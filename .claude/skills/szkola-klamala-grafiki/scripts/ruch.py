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
  tlo:       gwiazdy | siatka | kule                   – warstwa tła (domyślnie wg przedmiotu)
  przejscie: smuga | zoom | paski | blysk              – cięcie między planszami
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
    "przejscie": ["smuga", "zoom", "paski", "blysk"],
}
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
    fx = {}
    for k, opts in WARIANTY.items():
        if k == "przejscie":
            # pierwsze cięcie zawsze markową smugą, kolejne rotują
            fx[k] = "smuga" if i <= 1 else opts[(base + i) % len(opts)]   # przejście DO planszy i
        else:
            fx[k] = opts[(base // (7 + len(k)) + i) % len(opts)]
    fx["tlo"] = TLO_PRZEDMIOTU.get(post.get("subject", "").upper(), "kule")
    fx["kontur"] = True
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
.kontur{{position:absolute;left:50%;top:50%;white-space:nowrap;font-family:'Inter Display','Inter';font-weight:900;
  font-style:italic;font-size:560px;line-height:1;color:transparent;-webkit-text-stroke:3px rgba(47,107,255,.22);
  letter-spacing:-12px;text-transform:uppercase}}
.wipe{{position:absolute;inset:0;z-index:20;pointer-events:none;overflow:hidden}}
.wipe i{{position:absolute;top:-25%;height:150%;transform:skewX(-18deg)}}
.wipe .wb{{width:220%;left:-60%;background:linear-gradient(90deg,#1E4FD8,{TOK['blue']} 40%,#5B8CFF);box-shadow:0 0 80px rgba(47,107,255,.6)}}
.wipe .wy2{{width:9%;left:-74%;background:{TOK['yellow']};box-shadow:0 0 50px rgba(255,199,39,.7)}}
.wipe .wy{{width:9%;left:164%;background:{TOK['yellow']};box-shadow:0 0 50px rgba(255,199,39,.7)}}
.slats{{position:absolute;inset:0;z-index:20;pointer-events:none}}
.slats i{{position:absolute;left:0;width:100%;background:linear-gradient(90deg,#1E4FD8,{TOK['blue']})}}
.slats i:nth-child(3n){{background:{TOK['yellow']}}}
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
.sl .col{{display:block}} .sl .col i{{display:block;height:1.6em;font-style:inherit}}
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
@keyframes kStamp{{0%{{opacity:0;transform:rotate(-12deg) scale(2.8)}}55%{{opacity:1;transform:rotate(-12deg) scale(.9)}}100%{{opacity:1;transform:rotate(-12deg) scale(1)}}}}
@keyframes kShake{{0%,100%{{transform:none}}20%{{transform:translateX(-16px)}}40%{{transform:translateX(14px)}}60%{{transform:translateX(-9px)}}80%{{transform:translateX(5px)}}}}
@keyframes kDim{{from{{opacity:1}}to{{opacity:.45}}}}
.big,.num{{transform-origin:left center}} .center .big{{transform-origin:center}}
.row .fill{{transform-origin:left center}}
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
  if (fx.tlo === 'gwiazdy' || fx.tlo === 'siatka') {
    cv = document.createElement('canvas'); cv.width = W; cv.height = H; bg.appendChild(cv); ctx = cv.getContext('2d');
    let s2 = 9173; const r2 = () => { s2 = (s2 * 1664525 + 1013904223) >>> 0; return s2 / 4294967296; };
    for (let k = 0; k < 170; k++) stars.push({x: r2() * W, y: r2() * H, z: .25 + r2() * .75, ph: r2() * 6.28, sp: .6 + r2() * 2});
  } else {
    [['rgba(47,107,255,.34)', 520], ['rgba(255,199,39,.10)', 380], ['rgba(91,140,255,.22)', 440]].forEach(([col, sz], k) => {
      const d = document.createElement('div'); d.className = 'orb';
      Object.assign(d.style, {width: sz + 'px', height: sz + 'px', background: col}); bg.appendChild(d); orbs.push({d, k, sz});
    });
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
  const addCounter = (el, start, dur) => {
    if (!o.count) return;
    const nodes = []; const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    while (tw.nextNode()) if (/\d/.test(tw.currentNode.textContent)) nodes.push({node: tw.currentNode, orig: tw.currentNode.textContent});
    if (nodes.length) window.__counters.push({nodes, start, dur});
  };
  const impact = (el, t0, amp) => {
    window.__shakes.push({t0, amp});
    const sp = [];
    for (let k = 0; k < 16; k++) {
      const s = document.createElement('i'); s.className = 'spark'; document.body.appendChild(s);
      sp.push({s, a: rnd() * 6.283, d: 160 + rnd() * 260, len: .55 + rnd() * .5});
    }
    window.__sparks.push({el, t0, sp});
    ev.push({t: t0, typ: 'uderzenie'});
  };

  let t = 0;
  if (!o.enter) {
    c.querySelectorAll('.cd').forEach(el => { anim(el, 'kPop', .45, 0); ev.push({t: 0, typ: 'tik'}); });
    c.querySelectorAll('.opt.bad').forEach(el => { anim(el, 'kShake', .5, .1); ev.push({t: .1, typ: 'zle'}); });
    c.querySelectorAll('.opt.dim').forEach(el => anim(el, 'kDim', .4, .1));
  } else {
    const hw = [...c.querySelectorAll('h1,h2')].reduce((a, e) => a + e.innerText.split(/\s+/).length, 0) || 1;
    const hc = [...c.querySelectorAll('h1,h2')].reduce((a, e) => a + e.innerText.replace(/\s/g, '').length, 0) || 1;
    const bw = [...c.querySelectorAll('.sub,.body,.opt')].reduce((a, e) => a + e.innerText.split(/\s+/).length, 0) || 1;
    const sh = Math.min(.075, .55 / hw), sc = Math.min(.032, .7 / hc), sb = Math.min(.035, .75 / bw);
    c.querySelectorAll('.chip,.tag,.num,h1,h2,.brush,.big,.myth,.sub,.body,.opt,.row,.cd,.note,.src,.partner').forEach(el => {
      if (el.matches('.chip,.tag')) {
        if (!o.first) { anim(el, 'kChip', .38, t); ev.push({t, typ: 'etykieta'}); t += .14; }
      } else if (el.matches('h1,h2')) {
        if (o.first) {                                  // haczyk widoczny od klatki 0
          el.style.transformOrigin = 'left center'; anim(el, 'kPunch', .55, 0); ev.push({t: 0, typ: 'start'});
          if (fx.haczyk === 'blysk') {
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
                window.__slots.push({col, n: seq.length - 1, start: t0 + .05 + ci * .12, dur: .9 + ci * .08});
                land = Math.max(land, t0 + .05 + ci * .12 + .9 + ci * .08); ci++;
              } else { const s = document.createElement('span'); s.className = 'nd'; s.textContent = chr; frag.appendChild(s); }
            });
            nd.replaceWith(frag);
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
          anim(st, 'kStamp', .38, t + .75); window.__shakes.push({t0: t + .96, amp: 14}); ev.push({t: t + .96, typ: 'pieczatka'});
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

  // ── przejścia
  const wipe = document.createElement('div'); wipe.className = 'wipe';
  wipe.innerHTML = '<i class="wb"></i><i class="wy"></i><i class="wy2"></i>'; document.body.appendChild(wipe);
  const slats = document.createElement('div'); slats.className = 'slats';
  for (let k = 0; k < 7; k++) { const s = document.createElement('i'); s.style.top = (k * H / 7 - 1) + 'px'; s.style.height = (H / 7 + 2) + 'px'; slats.appendChild(s); }
  document.body.appendChild(slats);
  const flash = document.createElement('div'); flash.className = 'flash'; document.body.appendChild(flash);
  const io = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  const clamp = x => Math.min(1, Math.max(0, x));
  let rects = null;
  window.__layout = () => {                          // pozycje po dopasowaniu tekstu (stan końcowy)
    rects = window.__sparks.map(s => { const r = s.el.getBoundingClientRect(); return {x: r.left + r.width / 2, y: r.top + r.height / 2}; });
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
    let scale = push ? 1 + .025 * Math.min(1, t / dur) : 1, blur = 0, op = 1, tx = 0;
    wipe.style.display = 'none'; slats.style.display = 'none'; flash.style.opacity = 0;
    const kind = pOut !== null ? exitT : (pIn !== null ? enterT : null), q = pOut !== null ? pOut : pIn, isOut = pOut !== null;
    if (kind === 'smuga') {
      wipe.style.display = ''; const x = isOut ? -1 + q : q;
      [...wipe.children].forEach(e => e.style.translate = `${x * W * 2.4}px 0`);
    } else if (kind === 'zoom') {
      if (isOut) { scale *= 1 + .45 * q; blur = 18 * q; op = 1 - q; } else { scale *= .8 + .2 * q; blur = 18 * (1 - q); op = q; }
      flash.style.opacity = (isOut ? q : 1 - q) * .25;
    } else if (kind === 'paski') {
      slats.style.display = '';
      [...slats.children].forEach((s, k) => {
        const d = k % 2 ? 1 : -1, st = clamp(isOut ? (q * 1.35 - k * .05) : (q * 1.35 - k * .05));
        const x = isOut ? d * (1 - io(st)) : -d * io(st);
        s.style.transform = `translateX(${x * W * 1.02}px)`;
      });
    } else if (kind === 'blysk') {
      if (isOut) { tx = -W * .55 * q; blur = 22 * q; op = 1 - q; } else { tx = W * .55 * (1 - q); blur = 22 * (1 - q); op = q; }
      flash.style.opacity = (isOut ? q : 1 - q) * .3;
    }
    c.style.transform = scale !== 1 ? `scale(${scale})` : '';
    c.style.filter = blur ? `blur(${blur.toFixed(1)}px)` : '';
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
