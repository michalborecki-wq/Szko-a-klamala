#!/usr/bin/env python3
"""
Zakłada komplet folderów i szablonów dla nowej rolki fabryki „Szkoła kłamała”.

Użycie: python3 nowa_rolka.py <id> --tytul "..." [--data RRRR-MM-DD] [--kategoria A-E] [--lektor]

Tworzy (id rolki = RRRR-MM-DD_<id>):
  SCRIPTS/<rid>/scenariusz.md   – 3 warianty (kontrowersyjny / ciekawostkowy / emocjonalny), rekomendacja, karta 20 pkt,
                                   tekst lektorski, sceny z czasem, opis obrazu, napisy, muzyka i SFX, przejścia
  SCRIPTS/<rid>/spec.json       – szkielet dla silnika (wersja A, B do Rolki próbnej, opcjonalnie wersja z lektorem)
  SCRIPTS/<rid>/opis.md         – tytuł, opisy IG i TikTok, hashtagi, pytanie, przypięty komentarz, relacja
  SCRIPTS/<rid>/zrodla.md       – źródła z datami (min. 2 niezależne)
  IMAGES/<rid>/prompty.md       – prompty do obrazów/wideo AI (gdy rolka ich używa) + wybrany obraz okładki
  VOICEOVER/<rid>/, SUBTITLES/<rid>/, VIDEOS/<rid>/ – miejsce na pliki z produkcji
"""
import argparse
import datetime as dt
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCEN = """# {tytul}

Rolka: `{rid}` · kategoria {kategoria} · data publikacji: {data} · lektor: {lektor}

## 1. Fakty (wypełnij przed pisaniem)
- Fakt główny: …
- Liczby (policzone w kodzie): …
- Źródła (min. 2 niezależne, z datami): zob. `zrodla.md`
- Rodzaj: fakt / opinia / przypuszczenie (do rolki tylko fakty; opinie podpisane, czyje)
- Granice (CLAUDE.md): ok / polityka jako fakty (ustawa, liczby, skutek – bez ocen i bez stron)

## 2. Trzy warianty
| | A – kontrowersyjny | B – ciekawostkowy | C – emocjonalny |
|---|---|---|---|
| Haczyk (0–3 s, ≤8 słów) | … | … | … |
| Teza / oś | mocna teza + prowokacyjne pytanie | zaskoczenie + storytelling | historia, która wywołuje reakcję |
| Potencjał (1–10) | … | … | … |

**Rekomendacja:** wariant … – bo …  (do Rolki próbnej idzie drugi najlepszy jako `_wariantB`).

## 3. Sceny (szablon C „ujawnienie”; zwrot akcji najpóźniej ok. 12–14 s)
| # | Czas | Plansza (napis ekranowy, ≤12 słów) | Lektor (gdy jest) | Obraz / ruch | Przejście / SFX |
|---|---|---|---|---|---|
| 1 | 0–3 s | HOOK: … | … | okładka: obraz `…` + pieczątka `…` | uderzenie, start podkładu |
| 2 | 3–8 s | KONTEKST / dokument: … | … | liczba + tag instytucji | świst na cięciu |
| 3 | 8–13 s | ROZWINIĘCIE / stawka: … | … | … | riser |
| 4 | 13–18 s | KULMINACJA / TWIST: … | … | … | talerz, ducking |
| 5 | 18–24 s | CTA: pytanie + „Wyślij komuś, kto…” | … | outro | → logo (2,8 s) |

Zmiana obrazu co 2–4 s zapewnia silnik (`"moc": "mocna"`). Muzyka: oryginalny podkład z `muzyka.py` (nastrój: …).

## 4. Tekst lektorski (pełny, liczby słowami, skróty rozwinięte)
…

## 5. Karta 20 pkt (skill szkola-klamala-viral, sekcja 7)
| Kryterium | pkt |
|---|---|
| … | … |
| **Suma** | **…/20** (min. 15) |
"""

OPIS = """# Opis publikacji – {tytul}

**Tytuł (wewnętrzny):** …

**Instagram (A):**
```
<haczyk – ≤125 znaków> <emoji>

<fraza wyszukiwania + rozwinięcie, fakty z artykułami/liczbami>

<pytanie z rolki> 👇
Wyślij komuś, kto …

<seria / dopisek: To nie jest porada prawna. / inwestycyjna. / medyczna…>
Źródła: …

#szkolaklamala #… #… #… #…
```
**Instagram (B, Rolka próbna):** ten sam opis, pierwsza linia: `…`

**TikTok:**
```
<150–300 znaków, jeden akapit, 3–5 hashtagów, bez #fyp>
```

**Przypięty komentarz (dyskusja):** …
**Relacja:** ankieta „…” – Tak / Nie
**Godzina:** IG …, TikTok 1–2 h później · okładka ręcznie · „Udostępnij na Facebooku” włączone
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--tytul", required=True)
    ap.add_argument("--data", default=dt.date.today().isoformat())
    ap.add_argument("--kategoria", default="C")
    ap.add_argument("--lektor", action="store_true")
    a = ap.parse_args()
    slug = re.sub(r"[^a-z0-9_]+", "_", a.id.lower()).strip("_")
    rid = f"{a.data}_{slug}"
    d = {k: os.path.join(ROOT, k, rid) for k in ("SCRIPTS", "IMAGES", "VOICEOVER", "SUBTITLES", "VIDEOS")}
    for p in d.values():
        os.makedirs(p, exist_ok=True)
    kw = dict(tytul=a.tytul, rid=rid, data=a.data, kategoria=a.kategoria, lektor="tak" if a.lektor else "nie")
    pliki = {
        os.path.join(d["SCRIPTS"], "scenariusz.md"): SCEN.format(**kw),
        os.path.join(d["SCRIPTS"], "opis.md"): OPIS.format(**kw),
        os.path.join(d["SCRIPTS"], "zrodla.md"): f"# Źródła – {a.tytul}\n\n| Fakt | Źródło | URL | Data publikacji | Sprawdzone |\n|---|---|---|---|---|\n",
        os.path.join(d["IMAGES"], "prompty.md"): f"# Obrazy – {a.tytul}\n\n- Okładka: obraz silnika `…` + pieczątka `…`\n"
                                                  "- Obrazy/wideo AI (opcjonalnie, styl nie-fotorealistyczny, paleta marki, bez twarzy, bez logo instytucji):\n  1. …\n",
    }
    for p, txt in pliki.items():
        if not os.path.exists(p):
            open(p, "w", encoding="utf-8").write(txt)
    spec_p = os.path.join(d["SCRIPTS"], "spec.json")
    if not os.path.exists(spec_p):
        slajdy = [{"type": "cover", "obraz": "…", "pieczatka": "…", "title": "…", "accent": "…"},
                  {"type": "number", "tag": "…", "big": "…", "count": False, "title": "…", "accent": "…", "body": "…", "source": "…"},
                  {"type": "number", "tag": "…", "big": "…", "count": False, "title": "…", "accent": "…", "body": "…", "source": "…"},
                  {"type": "text", "tag": "TWIST", "title": "…", "accent": "…", "body": "…", "source": "…"},
                  {"type": "outro", "question": "…", "sub": "Wyślij komuś, kto …", "sources": "…", "partner_slot": False}]
        posts = [{"id": slug, "format": "reel", "subject": "…", "muzyka": {}, "durations": [3.5, 4.5, 4.5, 4.5, 6.0], "slides": slajdy},
                 {"id": slug + "_wariantB", "format": "reel", "subject": "…", "muzyka": {}, "durations": [3.5, 4.5, 4.5, 4.5, 6.0],
                  "slides": [dict(slajdy[0], uklad="zolty")] + slajdy[1:]}]
        if a.lektor:
            posts.append({"id": slug + "_lektor", "format": "reel", "subject": "…", "muzyka": {}, "durations": [3.5, 4.5, 4.5, 4.5, 6.0],
                          "slides": [dict(s, lektor="…") for s in slajdy]})
        json.dump({"handle": "@szkola_klamala", "posts": posts}, open(spec_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(rid)


if __name__ == "__main__":
    main()
