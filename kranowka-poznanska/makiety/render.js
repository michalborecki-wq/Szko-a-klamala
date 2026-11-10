#!/usr/bin/env node
/* Eksport makiet do PNG (2×) i zrzutu całej prezentacji.  node makiety/render.js */
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const fs = require("fs"), path = require("path");
const ROOT = path.resolve(__dirname, ".."), OUT = path.join(ROOT, "gotowe", "makiety"), PORT = 8766;

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const srv = spawn("python3", ["-m", "http.server", String(PORT), "--bind", "127.0.0.1"], { cwd: ROOT, stdio: "ignore" });
  await new Promise((r) => setTimeout(r, 900));
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: 2100, height: 1800 }, deviceScaleFactor: 2 });
    page.on("pageerror", (e) => console.error("BŁĄD STRONY:", e.message));
    const url = (m) => `http://127.0.0.1:${PORT}/makiety/makieta.html?render=1&m=${m}`;
    await page.goto(url("plakat-lej-tej"), { waitUntil: "load" });
    const names = await page.evaluate(() => window.KP_MAKIETY);
    for (const n of names) {
      await page.goto(url(n), { waitUntil: "load" });
      await page.evaluate(() => document.fonts.ready.then(() => true));
      await page.locator("#m").screenshot({ path: path.join(OUT, n + ".png") });
      console.log("makieta:", n);
    }
    await page.close();
    for (const [w, file] of [[1440, "prezentacja-desktop.png"], [390, "prezentacja-mobile.png"]]) {
      const p = await browser.newPage({ viewport: { width: w, height: 900 }, deviceScaleFactor: w < 500 ? 2 : 1, reducedMotion: "reduce" });
      p.on("pageerror", (e) => console.error("BŁĄD STRONY:", e.message));
      await p.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: "load" });
      await p.evaluate(() => document.fonts.ready.then(() => true));
      await p.waitForTimeout(800);
      await p.screenshot({ path: path.join(ROOT, "gotowe", file), fullPage: true });
      console.log("prezentacja:", file);
      await p.close();
    }
  } finally { await browser.close(); srv.kill(); }
})();
