#!/usr/bin/env python3
"""
Dziennikarz śledczy „Szkoła kłamała” – wybór tematów z BIEŻĄCYCH wiadomości.

  python3 sledczy.py [--godziny 48] [--data RRRR-MM-DD] [--top 10]

1. Uruchamia research.py (RSS: Google News PL, PAP, Reuters, Rzeczpospolita, TVN24…), jeśli na dziś nie ma nagłówków.
2. Odrzuca tematy zakazane w CLAUDE.md (wojny, religia, szczepionki, płeć, migracja, teorie spiskowe, tragedie i przemoc).
3. Punktuje to, co działa na koncie: sprawa z życia widza (podatki, ZUS, mandaty, prawo jazdy, ceny, nowe przepisy),
   nagłówek-straszak do rozbrojenia („pilny komunikat”, „od dziś”, „uwaga”), liczba źródeł, świeżość.
4. Zapisuje RESEARCH/<data>/sledczy.md – TOP N kandydatów z proponowanym kątem i listą „co sprawdzić w źródle pierwotnym”.

To tylko lista kandydatów. Fakt do rolki = dokument pierwotny (ISAP/API Sejmu, gov.pl, komunikat instytucji) + drugie
niezależne źródło. Procedura: skill .claude/skills/szkola-klamala-sledczy/SKILL.md.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ZAKAZ = r"wojn|wojsk|ukrain|rosj|putin|izrael|gaz[ay]\b|hamas|iran|nato|dron|rakiet|ostrzał|front\b|religi|kości[oó]ł|papie|bisk|ksi[eę]dz|" \
        r"szczepi|aborc|gender|transpł|lgbt|migra|imigra|uchodźc|granic[ay] z białoru|spisk|" \
        r"zamach|strzelanin|zabój|zabit|zginęł|zgin[aą]ł|nie żyje|ofiar|morderst|gwałt|samobój|wypad[ek]+ śmierteln|katastrof|pożar|" \
        r"sprawc[ay] ataku|atak (w|na)|żałob|pogrzeb|terror|lotto|losowani|kasyn|zakład(y|ów) bukmach"
POLITYKA = r"\bpis\b|\bpo\b|konfederac|tusk|kaczyń|nawrock|hołown|czarzast|kosiniak|mentzen|bosak|wybor|sondaż|partia|klub poselski"
ZYCIE = r"podat|\bpit\b|\bvat\b|zus|emerytur|rent[ay]|składk|mandat|punkt(y|ów) karn|prawo jazdy|kierowc|fotoradar|opłat|cen[ay]|" \
        r"drożej|tańsz|pensj|płac[ay] minimaln|wynagrodz|800 plus|świadczen|nfz|lekarz|recept|kaucj|abonament|rachunk|prąd|gaz\b|" \
        r"czynsz|kredyt|rat[ay]|bank|konsument|uokik|reklamac|zwrot|urząd skarbow|e-urząd|mobywatel|dowód osobist|paszport|" \
        r"ustaw[aęy]|przepis|nowelizac|rozporządzen|prezydent podpisał|sejm uchwalił|od (dziś|jutra|1 |stycznia|nowego roku)"
STRASZAK = r"pilny|pilne|uwaga|ważny komunikat|komunikat|przed chwilą|ostrzega|alarm|nie wszyscy wiedzą|sprawdź|od dziś|zmiany od|" \
           r"koniec z|rewolucja|szok|musisz|obowiązek|kara do|grzywna do"
# kontrowersja (decyzja Michała 11.11): spór, niesprawiedliwość, podwójny standard, kontrola władzy
KONTROWERSJA = r"nik\b|najwyższa izba|rpo\b|rzecznik praw|uokik|kontrol[ai] wykazał|nieprawidłow|wyrok|sąd uznał|trybunał|skarg|" \
               r"niesprawiedliw|przywilej|podwójn|luk[ai] w przepis|absurd|bezprawn|nadużyc|odszkodowan|kara dla|ukaran|" \
               r"zabior[aą]|strac[ąi]|dopłac|podwyżk|zakaz|obowiązk|bez zgody|bez wyroku|spór|oburz|protestuj[ąe] (kierowc|pacjen|rolnic|nauczyciel)"
PIERWOTNE = [
    (r"podat|pit|vat|urząd skarbow|e-urząd", "podatki.gov.pl (komunikat MF/KAS), ISAP – ustawa o PIT/VAT"),
    (r"zus|emerytur|składk|świadczen|rent", "zus.pl (komunikat), gov.pl/rodzina, ISAP – ustawa o systemie ubezpieczeń"),
    (r"mandat|punkt|prawo jazdy|kierowc|fotoradar", "ISAP – Prawo o ruchu drogowym, taryfikator; gov.pl/infrastruktura; policja.pl"),
    (r"ustaw|nowelizac|sejm|prezydent podpisał|przepis", "API Sejmu (druk + uzasadnienie/OSR), prezydent.pl, ISAP (Dz.U.)"),
    (r"cen|drożej|tańsz|kaucj|konsument|uokik|reklamac|zwrot", "uokik.gov.pl, GUS (stat.gov.pl), ISAP – ustawa"),
    (r"nfz|lekarz|recept", "nfz.gov.pl, gov.pl/zdrowie (bez porad medycznych – zasada „Medycyna”)"),
]


def wczytaj(data, godziny):
    p = os.path.join(ROOT, "RESEARCH", data, "naglowki.json")
    if not os.path.exists(p):
        subprocess.run([sys.executable, os.path.join(HERE, "research.py"), "--godziny", str(godziny), "--data", data], check=False)
    if not os.path.exists(p):
        sys.exit("Brak nagłówków – research.py nie pobrał kanałów (sieć?).")
    return json.load(open(p, encoding="utf-8"))["wpisy"]


def ocena(w, teraz):
    t = w["tytul"].lower()
    if re.search(ZAKAZ, t) or re.search(r"\bkrak[oó]w", t) and re.search(r"atak|strzel|ofiar|sprawc", t):
        return None, "zakazany temat"
    pkt, powody = 0, []
    if re.search(ZYCIE, t):
        pkt += 4; powody.append("sprawa z życia widza")
    if re.search(STRASZAK, t):
        pkt += 3; powody.append("nagłówek-straszak do rozbrojenia (treść vs tytuł)")
    if re.search(KONTROWERSJA, t):
        pkt += 3; powody.append("kontrowersja: spór / niesprawiedliwość / kontrola władzy")
    if 1 + len(w.get("inne_zrodla", [])) >= 3:
        pkt += 2; powody.append("temat z pierwszych stron (3+ redakcje)")
    if re.search(POLITYKA, t):
        pkt -= 3; powody.append("polityka – tylko fakty (ustawa, liczby, skutek), bez ocen")
    zr = 1 + len(w.get("inne_zrodla", []))
    pkt += min(3, zr - 1); powody.append(f"{zr} źródł(a/o) w RSS")
    if w.get("data"):
        h = (teraz - dt.datetime.fromisoformat(w["data"])).total_seconds() / 3600
        pkt += 2 if h < 24 else (1 if h < 48 else 0)
    return pkt, "; ".join(powody)


def kat(t):
    t = t.lower()
    if re.search(STRASZAK, t):
        return "„Nagłówek straszy, treść – nie”: co NAPRAWDĘ się zmienia, dla kogo, od kiedy, ile kosztuje (wzór: rolka PIT 10.11)"
    if re.search(r"ustaw|nowelizac|sejm|prezydent podpisał", t):
        return "„Ukryta stawka” z druku/uzasadnienia: koszt dla obywatela, przepis na końcu ustawy, sprzeczność z zapowiedzią (wzór: ZUS 9.11)"
    if re.search(r"mandat|punkt|kara|grzywn", t):
        return "„Porównanie niesprawiedliwości”: X karane surowiej niż Y – oba człony z przepisu"
    return "Liczba + porównanie do Polski + „dlaczego” (szablon B) albo ukryta reguła jak przeciek (szablon C)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--godziny", type=int, default=48)
    ap.add_argument("--data", default=dt.date.today().isoformat())
    ap.add_argument("--top", type=int, default=10)
    a = ap.parse_args()
    teraz = dt.datetime.now(dt.timezone.utc)
    kand, odrz = [], 0
    for w in wczytaj(a.data, a.godziny):
        p, pow_ = ocena(w, teraz)
        if p is None:
            odrz += 1; continue
        if p >= 4:
            kand.append((p, w, pow_))
    kand.sort(key=lambda x: -x[0])
    out = os.path.join(ROOT, "RESEARCH", a.data, "sledczy.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# Dziennikarz śledczy – kandydaci {a.data}\n\nOdrzucone jako zakazane (wojny, religia, tragedie itd.): {odrz}. "
                "Kandydat ≠ fakt: przed scenariuszem dokument pierwotny + drugie niezależne źródło.\n\n")
        for i, (p, w, pow_) in enumerate(kand[:a.top], 1):
            sp = [s for r, s in PIERWOTNE if re.search(r, w["tytul"].lower())] or ["źródło pierwotne instytucji, której dotyczy news"]
            f.write(f"## {i}. {w['tytul']}\n- punkty: {p} ({pow_})\n- link: {w['link']}\n- data: {(w.get('data') or '')[:16]}\n"
                    f"- kąt: {kat(w['tytul'])}\n- sprawdź w: {'; '.join(sp)}\n\n")
    print(out)
    for i, (p, w, _) in enumerate(kand[:a.top], 1):
        print(f"{i:2}. [{p}] {w['tytul'][:110]}")


if __name__ == "__main__":
    main()
