import json, os, re, sys
from playwright.sync_api import sync_playwright
from PIL import Image

OUT = os.environ.get("OUT","/home/claude/sk/out")
os.makedirs(OUT, exist_ok=True)
HANDLE = "@szkola_klamala"

def nbsp(t):
    # twarde spacje po jednoliterowych spójnikach/przyimkach
    return re.sub(r"(?<![\w&;])([aAiIoOuUwWzZ])\s", r"\1&nbsp;", t)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:%(W)dpx;height:%(H)dpx;overflow:hidden;font-family:Inter,sans-serif;color:#E8E8E8;
background:radial-gradient(ellipse at 50%% 35%%,#16203A 0%%,#0A0E18 70%%);position:relative}
.sm{position:absolute;width:900px;height:120px;background:#2F6BFF;border-radius:60px;transform:rotate(-24deg);filter:blur(6px)}
.sm.a{left:-420px;top:60px;opacity:.5}.sm.b{right:-420px;bottom:80px;opacity:.42}
.sm.a2{left:-380px;top:200px;height:40px;opacity:.4}.sm.b2{right:-380px;bottom:230px;height:40px;opacity:.4}
.wrap{position:absolute;inset:0;padding:%(PAD)s;display:flex;flex-direction:column;justify-content:center;z-index:2}
.top{position:absolute;top:56px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center;z-index:3}
.bar{width:120px;height:14px;background:#FFC727;border-radius:7px}
.cnt{font-weight:800;font-size:30px;color:#FFC727}
.bot{position:absolute;bottom:52px;left:80px;right:80px;display:flex;justify-content:space-between;font-size:30px;z-index:3}
.hd{color:#9AA3B5;font-weight:600}.sw{color:#FFC727;font-weight:800;font-style:italic}
.lbl{display:inline-block;align-self:flex-start;background:#FFC727;color:#0A0E18;font-weight:900;font-style:italic;
font-size:30px;padding:10px 22px;transform:skew(-8deg);letter-spacing:1px;margin-bottom:40px}
h1{font-weight:900;font-style:italic;text-transform:uppercase;color:#fff;text-shadow:0 6px 0 #2F6BFF;line-height:1.02;font-size:%(H1)dpx}
h1 .y{color:#FFC727;text-shadow:0 6px 0 #2F6BFF,0 0 40px rgba(255,199,39,.35);display:block}
.ul{width:420px;height:16px;background:#E53935;border-radius:8px;transform:rotate(-3deg);margin:34px 0 34px}
.sub{font-size:44px;line-height:1.3;color:#E8E8E8}
.num{font-weight:900;font-style:italic;font-size:150px;color:#FFC727;text-shadow:0 0 40px rgba(255,199,39,.45);line-height:1;margin-bottom:20px}
.tag{display:inline-block;align-self:flex-start;font-weight:900;font-style:italic;font-size:34px;padding:8px 22px;transform:skew(-8deg);color:#fff;margin-bottom:18px}
.mit{background:#E53935}.fakt{background:#2F6BFF}.za{background:#2F6BFF}.prz{background:#E53935}.zr{background:#FFC727;color:#0A0E18}
.mt{font-size:42px;line-height:1.3;color:#BFC3CC;text-decoration:line-through;text-decoration-color:#E53935;text-decoration-thickness:4px;margin-bottom:46px}
.tx{font-size:42px;line-height:1.36;color:#E8E8E8}
.tx b{color:#FFC727;font-weight:800}
h2{font-weight:900;font-style:italic;text-transform:uppercase;color:#fff;text-shadow:0 5px 0 #2F6BFF;font-size:66px;line-height:1.05;margin-bottom:34px}
h2 .y{color:#FFC727}
.big{font-weight:900;font-style:italic;font-size:220px;color:#FFC727;text-shadow:0 0 50px rgba(255,199,39,.45);line-height:1}
.partner{margin-top:60px;border:3px dashed rgba(154,163,181,.35);border-radius:20px;height:130px;width:420px}
.chart{margin-top:30px}
.row{display:flex;align-items:center;margin:14px 0;font-size:34px}
.row .k{width:170px;color:#9AA3B5;font-weight:700}
.row .v{height:46px;background:#2F6BFF;border-radius:8px;margin-right:18px}
.row .n{color:#FFC727;font-weight:900;font-style:italic}
.opt{font-size:50px;line-height:1.3;margin:22px 0;padding:26px 30px;background:rgba(255,255,255,.06);border-left:10px solid #2F6BFF;border-radius:10px}
.opt b{color:#FFC727;font-weight:900;font-style:italic;margin-right:14px}
.opt.bad{border-left-color:#E53935;background:rgba(229,57,53,.18)}
.opt.ok{opacity:.55}
.cd{font-weight:900;font-style:italic;font-size:200px;color:#FFC727;text-align:center;text-shadow:0 0 50px rgba(255,199,39,.5);margin-top:30px}
"""

def page(body, W=1080, H=1350, n=None, N=None, last=False, pad="150px 80px 140px", h1=104, chrome=True):
    css = CSS % dict(W=W, H=H, PAD=pad, H1=h1)
    if H == 1920:
        css += ".tx{font-size:56px}.sub{font-size:54px}h2{font-size:88px}.lbl{font-size:36px}.opt{font-size:54px}.tag{font-size:42px}"
    top = bot = ""
    if chrome:
        top = f'<div class="top"><div class="bar"></div><div class="cnt">{n}/{N}</div></div>' if n else ""
        sw = "" if last else '<span class="sw">przesuń →</span>'
        bot = f'<div class="bot"><span class="hd">{HANDLE}</span>{sw}</div>'
    return f"""<html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="sm a"></div><div class="sm a2"></div><div class="sm b"></div><div class="sm b2"></div>
{top}<div class="wrap">{nbsp(body)}</div>{bot}</body></html>"""

def tiktok_wrap(img_path, label, out_path):
    # slajd 4:5 wycentrowany na tle 9:16
    html = f"""<html><head><meta charset="utf-8"><style>{CSS % dict(W=1080,H=1920,PAD='0',H1=100)}
.t{{position:absolute;top:150px;left:0;right:0;text-align:center;z-index:3}}
.t span{{display:inline-block;background:#FFC727;color:#0A0E18;font-weight:900;font-style:italic;font-size:36px;padding:12px 26px;transform:skew(-8deg)}}
.im{{position:absolute;top:285px;left:0;width:1080px;height:1350px;z-index:2}}
.h{{position:absolute;bottom:150px;left:0;right:0;text-align:center;color:#9AA3B5;font-size:36px;font-weight:700;z-index:3}}
</style></head><body><div class="sm a"></div><div class="sm b"></div>
<div class="t"><span>{label}</span></div><img class="im" src="file://{img_path}"><div class="h">{HANDLE}</div></body></html>"""
    return html

def render(pw_page, html, path, W, H):
    pw_page.set_viewport_size({"width": W, "height": H})
    tmp = path.replace(".jpg", ".html")
    open(tmp, "w").write(html)
    pw_page.goto("file://" + tmp)
    pw_page.wait_for_timeout(150)
    png = path.replace(".jpg", ".png")
    pw_page.screenshot(path=png)
    Image.open(png).convert("RGB").save(path, "JPEG", quality=92)
    os.remove(png); os.remove(tmp)

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for post in spec:
            slides = post["slides"]; N = len(slides)
            kind = post.get("kind", "carousel")
            for i, s in enumerate(slides, 1):
                fn = f"{OUT}/{post['id']}_{i:02d}.jpg"
                if kind == "carousel":
                    html = page(s, n=i, N=N, last=(i == N))
                    render(pg, html, fn, 1080, 1350)
                    tk = f"{OUT}/{post['id']}_tt_{i:02d}.jpg"
                    render(pg, tiktok_wrap(fn, post["label"], tk), tk, 1080, 1920)
                elif kind == "tt":
                    html = page(s, W=1080, H=1920, n=i, N=N, last=(i == N), pad="260px 90px 240px", h1=112)
                    render(pg, html, fn, 1080, 1920)
                else:
                    html = page(s, W=1080, H=1920, pad="260px 90px 240px", h1=118, chrome=True, last=True)
                    render(pg, html, fn, 1080, 1920)
        b.close()
