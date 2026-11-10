/* Kranówka Poznańska – biblioteka marki: logo, zastosowania, system ruchu (GSAP). */
(function () {
  const L = window.KP_LOGO;
  const KP = (window.KP = { base: "" });

  /* ---------- logo ---------- */
  KP.logo = (cls = "") => `<div class="kp-logo ${cls}">${L.logo}</div>`;
  KP.wordmark = (cls = "") => `<div class="kp-wordmark ${cls}">${L.wordmark}</div>`;
  KP.znak = (color = "currentColor") =>
    `<svg viewBox="-125 -250 250 380" style="overflow:visible"><path fill-rule="evenodd" fill="${color}" d="${L.ring}"/>` +
    `<g transform="translate(24,-172) rotate(24) scale(.86)"><path fill="${color}" d="${L.drop}"/></g></svg>`;
  KP.odcisk = (color = "currentColor", alt = false) =>
    `<svg viewBox="-106 -106 212 212" style="overflow:visible"><path fill-rule="evenodd" fill="${color}" d="${alt ? L.ring2 : L.ring}"/></svg>`;
  KP.kaustyka = (naWodzie = false) =>
    `<div class="kp-kaustyka a${naWodzie ? " na-wodzie" : ""}"></div><div class="kp-kaustyka b${naWodzie ? " na-wodzie" : ""}"></div>`;
  KP.partnerzy = () =>
    `<div class="kp-partnerzy"><div class="l"><img class="herb" src="${KP.base}assets/partnerzy/herb-poznan.svg" alt="Herb Poznania">` +
    `<div class="txt">Miasto<br>Poznań</div></div><div class="sep"></div>` +
    `<img class="aq" src="${KP.base}assets/partnerzy/aquanet.svg" alt="Aquanet"></div>`;

  /* ---------- zastosowania ---------- */
  const nb = " ";
  KP.apps = {
    plakat: (a = "Lej,", b = "tej.", sub = "Poznańska kranówka. Prosto z kranu, bez noszenia.") => `
      <div class="app app-plakat">
        <div class="hd kp-cap"><span>Kranówka Poznańska</span><span>Poznań${nb}/${nb}2026</span></div>
        <h2 class="kp-d">${a}<br><em>${b}</em></h2>
        <div class="sub kp-di">${sub}</div>
        <div class="wz"><div class="kp-druk woda"></div></div>
        <div class="ft">${KP.logo()}${KP.partnerzy()}</div>
      </div>`,
    billboard: (a = "Nie dźwigaj.", b = "Odkręć.") => `
      <div class="app app-billboard">
        <div class="znak">${KP.odcisk("#0B1B3F")}</div>
        <h2 class="kp-d"><span>${a}</span><span>${b}</span></h2>
        <div class="ft">${KP.logo()}${KP.partnerzy()}</div>
      </div>`,
    podkladka: () => `
      <div class="app app-podkladka">
        <div class="odcisk">${KP.odcisk("#2EA8FF", true)}</div>
        <div class="in"><div class="kp-d">Tu się<br>leje.</div><div class="kp-cap">Kranówka w${nb}tym lokalu</div>${KP.logo()}</div>
      </div>`,
    naklejka: () => `
      <div class="app app-naklejka">${KP.kaustyka(true)}
        <div class="in"><div class="kp-cap">W tym lokalu</div><div class="kp-d">Lejemy<br>z${nb}kranu.</div>${KP.logo()}</div>
      </div>`,
    post: (a = "Źródło", b = "masz", c = "w kuchni.") => `
      <div class="app app-post">${KP.kaustyka()}
        <div class="hd kp-cap">Kranówka Poznańska</div>
        <h2 class="kp-d">${a}<br>${b}<br><em>${c}</em></h2>
        ${KP.logo()}<div class="znak">${KP.znak("#2EA8FF")}</div>
      </div>`,
    butelka: (body = "#0B1B3F", ink = "#F5F3EE") => `
      <div class="app app-butelka"><svg viewBox="0 0 520 1500">
        <ellipse cx="270" cy="1452" rx="210" ry="22" fill="#0B1B3F" opacity=".22"/>
        <rect x="186" y="40" width="148" height="118" rx="24" fill="${ink}"/>
        <rect x="186" y="118" width="148" height="12" fill="#0B1B3F" opacity=".12"/>
        <rect x="204" y="156" width="112" height="60" fill="${body}"/>
        <rect x="204" y="156" width="112" height="14" fill="#000" opacity=".25"/>
        <path d="M204 212 C204 300 92 292 92 404 L92 1372 Q92 1440 160 1440 L360 1440 Q428 1440 428 1372 L428 404 C428 292 316 300 316 212 Z" fill="${body}"/>
        <path d="M380 330 C420 352 428 380 428 404 L428 1372 Q428 1440 360 1440 L330 1440 Q388 1436 388 1372 L388 420 C388 380 386 350 380 330 Z" fill="#000" opacity=".22"/>
        <rect x="122" y="420" width="16" height="900" rx="8" fill="#fff" opacity=".13"/>
        <rect x="148" y="470" width="6" height="640" rx="3" fill="#fff" opacity=".08"/>
        <g transform="translate(150,1310) rotate(-90)" color="${ink}">${L.wordmark.replace("<svg ", '<svg width="800" height="155" ')}</g>
      </svg></div>`,
  };

  /* ---------- system ruchu ---------- */
  /* 1. Zalanie – odsłonięcie od dołu falującą krawędzią (clip-path). */
  KP.wave = (tl, el, at, dur, o = {}) => {
    const W = o.W || 1080, H = o.H || 1920, amp = o.amp == null ? 46 : o.amp, k = o.k || 2.2, from = o.from || 0, to = o.to == null ? 1 : o.to;
    const st = { p: from };
    const draw = () => {
      const y = (H + amp * 2) * (1 - st.p) - amp;
      const a = amp * Math.sin(Math.PI * Math.min(1, st.p * 1.02));
      let pts = [];
      for (let i = 0; i <= 24; i++) {
        const x = (W * i) / 24;
        pts.push(`${x.toFixed(1)}px ${(y + a * Math.sin((i / 24) * Math.PI * 2 * k + st.p * 9) + a * 0.35 * Math.sin((i / 24) * Math.PI * 2 * k * 2.3 - st.p * 14)).toFixed(1)}px`);
      }
      el.style.clipPath = `polygon(${pts.join(",")},${W}px ${H + 4}px,0px ${H + 4}px)`;
    };
    draw();
    tl.to(st, { p: to, duration: dur, ease: o.ease || "power2.inOut", onUpdate: draw }, at);
    return tl;
  };
  /* 2. Krąg – odsłonięcie kołem od punktu uderzenia kropli. */
  KP.circle = (tl, el, at, dur, x, y, R = 2300) => {
    const st = { r: 0 };
    const draw = () => (el.style.clipPath = `circle(${st.r.toFixed(1)}px at ${x}px ${y}px)`);
    draw();
    tl.to(st, { r: R, duration: dur, ease: "power2.in", onUpdate: draw }, at);
    return tl;
  };
  /* 3. Dryf – wzór kaustyk nigdy nie stoi. */
  KP.drift = (tl, root, total) => {
    root.querySelectorAll(".kp-kaustyka.a").forEach((e) => tl.fromTo(e, { x: 0, y: 0 }, { x: -110, y: -150, duration: total, ease: "none" }, 0));
    root.querySelectorAll(".kp-kaustyka.b").forEach((e) => tl.fromTo(e, { x: 0, y: 0, rotation: 0 }, { x: 120, y: 90, rotation: 4, duration: total, ease: "none" }, 0));
  };
  /* 4. Wynurzenie – wiersze tekstu wypływają spod linii. */
  KP.lines = (el) => {
    const rows = el.innerHTML.split(/<br\s*\/?>/i);
    el.innerHTML = rows.map((r) => `<span class="ln" style="display:block;overflow:hidden;padding:.12em .05em .16em;margin:-.12em -.05em -.16em"><span class="li" style="display:block">${r}</span></span>`).join("");
    return el.querySelectorAll(".li");
  };
  KP.rise = (tl, el, at, o = {}) => {
    const li = el.querySelectorAll(".li").length ? el.querySelectorAll(".li") : KP.lines(el);
    tl.fromTo(li, { yPercent: 118 }, { yPercent: 0, duration: o.dur || 0.7, ease: "expo.out", stagger: o.stagger == null ? 0.09 : o.stagger }, at);
  };
  /* 5. Złożenie logo – litery napływają do odcisku, kropla spada na miejsce. */
  KP.assemble = (tl, logoEl, at, o = {}) => {
    const ls = [...logoEl.querySelectorAll(".kp-l")], ring = logoEl.querySelector(".kp-ring"), drop = logoEl.querySelector(".kp-drop"), sub = logoEl.querySelectorAll(".kp-sub path");
    const left = ls.slice(0, 4).reverse(), right = ls.slice(4);
    gsap.set(ls, { transformBox: "fill-box", transformOrigin: "50% 100%" });
    if (!o.keepRing) tl.fromTo(ring, { scale: 0, transformOrigin: "50% 50%", transformBox: "fill-box" }, { scale: 1, duration: 0.6, ease: "back.out(1.6)" }, at);
    tl.fromTo(left, { x: 520, opacity: 0, scaleY: 0.7 }, { x: 0, opacity: 1, scaleY: 1, duration: 0.75, ease: "expo.out", stagger: 0.06 }, at + 0.12);
    tl.fromTo(right, { x: -520, opacity: 0, scaleY: 0.7 }, { x: 0, opacity: 1, scaleY: 1, duration: 0.75, ease: "expo.out", stagger: 0.06 }, at + 0.12);
    tl.fromTo(drop, { y: -900, opacity: 0, transformBox: "fill-box", transformOrigin: "50% 100%" }, { y: 0, opacity: 1, duration: 0.42, ease: "power3.in" }, at + 0.62);
    tl.fromTo(drop, { scaleY: 0.72, scaleX: 1.25 }, { scaleY: 1, scaleX: 1, duration: 0.5, ease: "elastic.out(1,.45)" }, at + 1.04);
    tl.fromTo(sub, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out", stagger: 0.035 }, at + 0.85);
  };
  /* 6. Kręgi – fala po uderzeniu kropli. */
  KP.ripples = (tl, parent, at, x, y, o = {}) => {
    const n = o.n || 3, size = o.size || 900, color = o.color || "currentColor";
    for (let i = 0; i < n; i++) {
      const d = document.createElement("div");
      d.style.cssText = `position:absolute;left:${x - size / 2}px;top:${y - size / 2}px;width:${size}px;height:${size}px;border-radius:50%;border:${o.w || 5}px solid ${color};opacity:0;pointer-events:none`;
      parent.appendChild(d);
      tl.fromTo(d, { scale: 0.04, opacity: 0.9 }, { scale: 1, opacity: 0, duration: o.dur || 1.1, ease: "power2.out" }, at + i * (o.gap || 0.16));
    }
  };
})();
