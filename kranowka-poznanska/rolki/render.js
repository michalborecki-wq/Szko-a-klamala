#!/usr/bin/env node
/* Render rolek do MP4 (klatka po klatce, deterministycznie).
   node rolki/render.js            – wszystkie rolki, 1080×1920, 30 kl./s
   node rolki/render.js 2          – tylko rolka 2
   node rolki/render.js sheet      – arkusze klatek kontrolnych (PNG) zamiast wideo
   Wymaga: playwright, ffmpeg. */
const { chromium } = require("playwright");
const { spawn, execFileSync } = require("child_process");
const http = require("http"), fs = require("fs"), path = require("path");

const ROOT = path.resolve(__dirname, ".."), OUT = path.join(ROOT, "gotowe");
const FPS = 30, NAMES = { 1: "rolka-1-odcisk", 2: "rolka-2-lej-tej", 3: "rolka-3-nie-dzwigaj" };
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".svg": "image/svg+xml", ".png": "image/png", ".woff2": "font/woff2", ".jpg": "image/jpeg", ".mp4": "video/mp4" };

function serve() {
  return new Promise((res) => {
    const s = http.createServer((q, r) => {
      const f = path.join(ROOT, decodeURIComponent(q.url.split("?")[0]));
      if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); return r.end(); }
      r.writeHead(200, { "Content-Type": MIME[path.extname(f)] || "application/octet-stream" });
      fs.createReadStream(f).pipe(r);
    }).listen(0, "127.0.0.1", () => res(s));
  });
}

(async () => {
  const arg = process.argv[2], sheet = arg === "sheet", only = /^[123]$/.test(arg || "") ? [+arg] : [1, 2, 3];
  fs.mkdirSync(OUT, { recursive: true });
  const srv = await serve(), port = srv.address().port;
  const browser = await chromium.launch();
  for (const r of only) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
    page.on("pageerror", (e) => console.error("BŁĄD STRONY:", e.message));
    await page.goto(`http://127.0.0.1:${port}/rolki/rolka.html?r=${r}&render=1`, { waitUntil: "load", timeout: 30000 });
    await page.evaluate(() => document.fonts.ready.then(() => true));
    const dur = await page.evaluate(() => window.KP_DUR);
    if (sheet) {
      const dir = process.argv[3] || OUT, step = +(process.argv[4] || 0.4);
      for (let t = 0, i = 0; t < dur; t += step, i++) {
        await page.evaluate((t) => window.seek(t), t);
        await page.screenshot({ path: path.join(dir, `r${r}_${String(i).padStart(3, "0")}.jpg`), type: "jpeg", quality: 80 });
      }
      console.log(`rolka ${r}: ${dur.toFixed(2)} s – klatki kontrolne`);
    } else {
      const file = path.join(OUT, NAMES[r] + ".mp4"), n = Math.round(dur * FPS);
      const ff = spawn("ffmpeg", ["-v", "error", "-y", "-f", "image2pipe", "-framerate", String(FPS), "-i", "-",
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest", "-c:v", "libx264", "-preset", "slow", "-crf", "15",
        "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.1", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", file],
        { stdio: ["pipe", "inherit", "inherit"] });
      for (let i = 0; i < n; i++) {
        await page.evaluate((t) => window.seek(t), i / FPS);
        const buf = await page.screenshot({ type: "png" });
        if (!ff.stdin.write(buf)) await new Promise((ok) => ff.stdin.once("drain", ok));
      }
      ff.stdin.end();
      await new Promise((ok) => ff.on("close", ok));
      console.log(`rolka ${r}: ${dur.toFixed(2)} s, ${n} klatek → ${path.relative(ROOT, file)}`);
    }
    await page.close();
  }
  await browser.close(); srv.close();
})();
