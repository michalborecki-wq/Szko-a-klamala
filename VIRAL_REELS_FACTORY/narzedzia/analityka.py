#!/usr/bin/env python3
"""
Analityka fabryki rolek: wprowadzanie wyników i raport, co działa.

  python3 analityka.py dodaj <rid> --siec ig|tt|fb --wyswietlenia N [--sr-czas S] [--do-konca PROC]
        [--polubienia N] [--komentarze N] [--udostepnienia N] [--zapisy N] [--obserwujacy N] [--pominiecia PROC]
        [--data RRRR-MM-DD]                       – dopisuje wiersz (np. ze zrzutu z aplikacji albo z Composio)
  python3 analityka.py import plik.json           – lista słowników z tymi samymi polami (np. zrzut z Composio)
  python3 analityka.py opublikowano <rid>         – przenosi paczkę z READY_TO_PUBLISH do PUBLISHED
  python3 analityka.py raport                     – ANALYTICS/raport.md: średnie wg kategorii, typu haczyka,
                                                    długości, lektora, wariantu (A/B) i sieci + wnioski

Metadane rolki (kategoria, typ haczyka, długość, lektor) czyta z SCRIPTS/<rid>/meta.json, jeśli istnieje:
  {"kategoria": "A", "haczyk": "…", "typ_haczyka": "ujawnienie|liczba|zakaz|pytanie|…", "dlugosc_s": 26, "lektor": false}
"""
import argparse
import csv
import datetime as dt
import json
import os
import shutil
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "ANALYTICS", "wyniki.csv")
POLA = ["data", "rid", "siec", "wariant", "wyswietlenia", "sr_czas", "do_konca", "pominiecia", "polubienia",
        "komentarze", "udostepnienia", "zapisy", "obserwujacy"]


def zapisz(wiersze):
    nowy = not os.path.exists(CSV)
    with open(CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=POLA)
        if nowy:
            w.writeheader()
        for r in wiersze:
            w.writerow({k: r.get(k, "") for k in POLA})


def meta(rid):
    base = rid.replace("_wariantB", "").replace("_lektor", "")
    for r in (rid, base):
        p = os.path.join(ROOT, "SCRIPTS", r, "meta.json")
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8"))
    return {}


def liczba(x):
    try:
        return float(str(x).replace(",", ".").replace("%", ""))
    except ValueError:
        return None


def raport():
    if not os.path.exists(CSV):
        raise SystemExit("Brak danych – najpierw `dodaj` albo `import`.")
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    grupy = defaultdict(lambda: defaultdict(list))
    for r in rows:
        m = meta(r["rid"])
        d = liczba(m.get("dlugosc_s", ""))
        klucze = {"sieć": r["siec"], "wariant": r.get("wariant") or "A", "kategoria": m.get("kategoria", "?"),
                  "typ haczyka": m.get("typ_haczyka", "?"), "lektor": "tak" if m.get("lektor") else "nie",
                  "długość": "?" if d is None else ("<20 s" if d < 20 else "20–29 s" if d < 30 else "30–45 s")}
        for wymiar, wart in klucze.items():
            grupy[wymiar][wart].append(r)
    out = [f"# Raport analityki – {dt.date.today().isoformat()}\n", f"Wierszy: {len(rows)}\n"]
    for wymiar, g in grupy.items():
        out.append(f"## Wg: {wymiar}\n\n| {wymiar} | rolek | śr. wyświetlenia | śr. czas | śr. pominięcia | śr. udostępnienia |\n|---|---|---|---|---|---|")
        wyniki = []
        for wart, rs in g.items():
            def sr(k):
                v = [liczba(x[k]) for x in rs if liczba(x[k]) is not None]
                return sum(v) / len(v) if v else None
            wyniki.append((sr("wyswietlenia") or 0, wart, len(rs), sr("sr_czas"), sr("pominiecia"), sr("udostepnienia")))
        for w, wart, n, c, p, u in sorted(wyniki, reverse=True):
            f = lambda x, s="": "–" if x is None else f"{x:.1f}{s}"
            out.append(f"| {wart} | {n} | {w:.0f} | {f(c, ' s')} | {f(p, '%')} | {f(u)} |")
        out.append("")
    top = sorted(rows, key=lambda r: liczba(r["wyswietlenia"]) or 0, reverse=True)[:5]
    out.append("## TOP 5 rolek\n")
    for r in top:
        out.append(f"- {r['rid']} ({r['siec']}): {r['wyswietlenia']} wyśw., śr. czas {r['sr_czas'] or '–'} s, haczyk: {meta(r['rid']).get('haczyk', '?')}")
    p = os.path.join(ROOT, "ANALYTICS", "raport.md")
    open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("Raport:", p)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dodaj")
    d.add_argument("rid")
    d.add_argument("--siec", required=True, choices=["ig", "tt", "fb"])
    d.add_argument("--wariant", default="")
    d.add_argument("--data", default=dt.date.today().isoformat())
    for k in POLA[4:]:
        d.add_argument("--" + k.replace("_", "-"), dest=k, default="")
    i = sub.add_parser("import")
    i.add_argument("plik")
    o = sub.add_parser("opublikowano")
    o.add_argument("rid")
    sub.add_parser("raport")
    a = ap.parse_args()
    if a.cmd == "dodaj":
        zapisz([{k: getattr(a, k, "") for k in POLA}])
        print("dodano:", a.rid, a.siec)
    elif a.cmd == "import":
        dane = json.load(open(a.plik, encoding="utf-8"))
        zapisz(dane)
        print("zaimportowano:", len(dane))
    elif a.cmd == "opublikowano":
        src, dst = os.path.join(ROOT, "READY_TO_PUBLISH", a.rid), os.path.join(ROOT, "PUBLISHED", a.rid)
        if not os.path.isdir(src):
            raise SystemExit(f"Brak paczki {src}")
        shutil.move(src, dst)
        open(os.path.join(dst, "opublikowano.txt"), "w").write(dt.datetime.now().isoformat() + "\n")
        print("przeniesiono do", dst)
    else:
        raport()


if __name__ == "__main__":
    main()
