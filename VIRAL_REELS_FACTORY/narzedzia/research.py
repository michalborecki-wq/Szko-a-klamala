#!/usr/bin/env python3
"""
Poranny przegląd wiadomości dla fabryki rolek „Szkoła kłamała”.

Pobiera kanały RSS z zrodla_rss.json, zostawia wpisy z ostatnich N godzin (domyślnie 72), usuwa duplikaty
(po podobieństwie tytułów) i zapisuje:
  RESEARCH/RRRR-MM-DD/naglowki.json  – lista wpisów (tytuł, źródło, link, data)
  RESEARCH/RRRR-MM-DD/naglowki.md    – czytelna lista dla agenta

Nagłówki to TYLKO punkt wyjścia. Fakt do rolki = sprawdzony w źródle pierwotnym (min. 2 niezależne źródła).

Użycie: python3 research.py [--godziny 72] [--data RRRR-MM-DD]
"""
import argparse
import datetime as dt
import email.utils
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UA = "Mozilla/5.0 (compatible; szkola-klamala-research/1.0)"


def pobierz(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def data_wpisu(txt):
    if not txt:
        return None
    try:
        d = email.utils.parsedate_to_datetime(txt)
    except (TypeError, ValueError):
        try:
            d = dt.datetime.fromisoformat(txt.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d


def parsuj(xml, zrodlo):
    out = []
    root = ET.fromstring(xml)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for it in root.iter("item"):
        tyt = (it.findtext("title") or "").strip()
        src = it.find("source")
        out.append({"tytul": tyt, "link": (it.findtext("link") or "").strip(),
                    "data": it.findtext("pubDate"),
                    "zrodlo": (src.text.strip() if src is not None and src.text else zrodlo)})
    for it in root.findall("a:entry", ns):
        link = it.find("a:link", ns)
        out.append({"tytul": (it.findtext("a:title", default="", namespaces=ns) or "").strip(),
                    "link": link.get("href") if link is not None else "",
                    "data": it.findtext("a:updated", default="", namespaces=ns), "zrodlo": zrodlo})
    return out


def norm(t):
    t = re.sub(r"\s+-\s+[^-]{2,40}$", "", t)          # Google News dopisuje „ - Nazwa portalu”
    return re.sub(r"[^\w ]", "", t.lower()).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--godziny", type=int, default=72)
    ap.add_argument("--data", default=dt.date.today().isoformat())
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(HERE, "zrodla_rss.json"), encoding="utf-8"))
    granica = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=a.godziny)
    wpisy, bledy = [], []
    for k in cfg["kanaly"]:
        try:
            for w in parsuj(pobierz(k["url"]), k["nazwa"]):
                d = data_wpisu(w["data"])
                if d and d < granica:
                    continue
                w["data"] = d.isoformat() if d else None
                w["kanal"] = k["nazwa"]
                wpisy.append(w)
        except Exception as e:  # jeden padnięty kanał nie zatrzymuje przeglądu
            bledy.append(f"{k['nazwa']}: {e}")
    unik = []
    for w in sorted(wpisy, key=lambda x: x["data"] or "", reverse=True):
        n = norm(w["tytul"])
        if not n:
            continue
        podobny = next((u for u in unik if SequenceMatcher(None, n, u["_n"]).ratio() > 0.82), None)
        if podobny:
            podobny["inne_zrodla"].append(w["zrodlo"])
            continue
        w["_n"], w["inne_zrodla"] = n, []
        unik.append(w)
    for u in unik:
        u.pop("_n", None)
    folder = os.path.join(ROOT, "RESEARCH", a.data)
    os.makedirs(folder, exist_ok=True)
    json.dump({"data": a.data, "godziny": a.godziny, "bledy": bledy, "wpisy": unik},
              open(os.path.join(folder, "naglowki.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(folder, "naglowki.md"), "w", encoding="utf-8") as f:
        f.write(f"# Nagłówki {a.data} (ostatnie {a.godziny} h)\n\n")
        f.write("Punkt wyjścia do wyboru tematów. Każdy fakt sprawdzić w źródle pierwotnym.\n\n")
        if bledy:
            f.write("Kanały z błędem: " + "; ".join(bledy) + "\n\n")
        for i, w in enumerate(unik, 1):
            extra = f" (+{len(w['inne_zrodla'])} źródeł)" if w["inne_zrodla"] else ""
            f.write(f"{i}. {w['tytul']} — {w['zrodlo']}{extra} · {(w['data'] or '')[:16]} · {w['link']}\n")
    print(f"{len(unik)} nagłówków (z {len(wpisy)}), błędy kanałów: {len(bledy)} → {folder}")
    if not unik:
        sys.exit(1)


if __name__ == "__main__":
    main()
