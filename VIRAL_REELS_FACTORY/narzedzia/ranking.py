#!/usr/bin/env python3
"""
Ranking tematów dnia (TOP 10 i TOP 3) dla fabryki rolek.

Wejście: TOPICS/RRRR-MM-DD/tematy.json – lista tematów przygotowana przez agenta po researchu:
  {"id": "krotka-nazwa", "tytul": "...", "kategoria": "A|B|C|D|E",
   "oceny": {"emocje": 1-10, "dyskusja": 1-10, "aktualnosc": 1-10, "zaskoczenie": 1-10, "film": 1-10, "udostepnienia": 1-10},
   "zrodla": [{"nazwa": "...", "url": "...", "data": "RRRR-MM-DD"}, ...],
   "weryfikacja": "potwierdzone|czesciowo|niepotwierdzone",
   "rodzaj": "fakt|opinia|przypuszczenie|satyra",
   "granice": "ok|polityka-fakty|odrzucone: <powód>",
   "haczyk": "...", "uwagi": "..."}

Zasady (CLAUDE.md, decyzja 4.11): do TOP 3 trafiają tylko tematy potwierdzone w min. 2 niezależnych źródłach,
rodzaj „fakt”, granice ≠ „odrzucone”. Polityka tylko jako fakty (ustawa, liczby, skutek), bez ocen i bez stron.

Wynik: TOPICS/RRRR-MM-DD/TOP10.md i top3.json.
Użycie: python3 ranking.py [--data RRRR-MM-DD]
"""
import argparse
import datetime as dt
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KRYT = ["emocje", "dyskusja", "aktualnosc", "zaskoczenie", "film", "udostepnienia"]
KAT = {"A": "Kontrowersje i bieżące wydarzenia", "B": "Ciekawostki, które szokują",
       "C": "Społeczeństwo i codzienne życie", "D": "Technologia i przyszłość", "E": "Tematy do dyskusji"}


def dopuszczony(t):
    return (t.get("weryfikacja") == "potwierdzone" and len(t.get("zrodla", [])) >= 2
            and t.get("rodzaj") == "fakt" and not str(t.get("granice", "")).startswith("odrzucone"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=dt.date.today().isoformat())
    a = ap.parse_args()
    folder = os.path.join(ROOT, "TOPICS", a.data)
    tematy = json.load(open(os.path.join(folder, "tematy.json"), encoding="utf-8"))
    for t in tematy:
        o = t.get("oceny", {})
        brak = [k for k in KRYT if k not in o]
        if brak:
            raise SystemExit(f"{t.get('id')}: brak ocen {brak}")
        t["suma"] = sum(int(o[k]) for k in KRYT)
        t["dopuszczony"] = dopuszczony(t)
    ranking = sorted(tematy, key=lambda t: (t["dopuszczony"], t["suma"]), reverse=True)
    top10, top3 = ranking[:10], [t for t in ranking if t["dopuszczony"]][:3]
    json.dump(top3, open(os.path.join(folder, "top3.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(folder, "TOP10.md"), "w", encoding="utf-8") as f:
        f.write(f"# TOP 10 tematów – {a.data}\n\nSuma 6 kryteriów (max 60): emocje, dyskusja, aktualność, zaskoczenie, "
                "potencjał filmu, udostępnienia. ✅ = dopuszczony do produkcji (fakt, ≥2 źródła, w granicach).\n\n")
        f.write("| # | Temat | Kat. | Suma | E | D | A | Z | F | U | Weryfikacja | Granice |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n")
        for i, t in enumerate(top10, 1):
            o = t["oceny"]
            f.write(f"| {i} | {'✅ ' if t['dopuszczony'] else '⛔ '}{t['tytul']} | {t.get('kategoria','')} | **{t['suma']}** | "
                    + " | ".join(str(o[k]) for k in KRYT) + f" | {t.get('weryfikacja','')} ({len(t.get('zrodla',[]))} źr.) | {t.get('granice','')} |\n")
        f.write("\n## TOP 3 do produkcji\n\n")
        for i, t in enumerate(top3, 1):
            f.write(f"### {i}. {t['tytul']} ({KAT.get(t.get('kategoria'), '')}, {t['suma']}/60)\n- Haczyk: {t.get('haczyk','')}\n")
            for z in t.get("zrodla", []):
                f.write(f"- Źródło: [{z['nazwa']}]({z['url']}) · {z.get('data','')}\n")
            if t.get("uwagi"):
                f.write(f"- Uwagi: {t['uwagi']}\n")
            f.write("\n")
    print(f"TOP10 → {folder}/TOP10.md; TOP3: {', '.join(t['id'] for t in top3) or 'brak dopuszczonych'}")


if __name__ == "__main__":
    main()
