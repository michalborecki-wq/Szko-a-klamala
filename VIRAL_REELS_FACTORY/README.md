# VIRAL REELS FACTORY – „Szkoła kłamała”

Autonomiczna fabryka rolek: codzienny przegląd wiadomości → ranking TOP 10 → TOP 3 ze scenariuszami (3 warianty) → produkcja (4K, TikTok 1080, okładki, lektor w teście) → opisy → paczka do publikacji → analityka. **Nic nie jest publikowane automatycznie** – Michał zatwierdza i publikuje ręcznie (IG + crosspost FB, TikTok).

Zasady treści: `CLAUDE.md` (pierwszeństwo przed tym plikiem). Decyzje Michała z 4.11:
- **Polityka tylko jako fakty:** ustawa, liczby, skutek dla widza; bez ocen, bez stawania po stronie partii, bez atakowania osób, zawsze min. 2 niezależne źródła (najlepiej pierwotne: Sejm/ISAP, KPRP, GUS, NIK). Wojny i konflikty zbrojne, religia, szczepionki, migracja, płeć – nadal poza fabryką.
- **Lektor – test:** 1 rolka dziennie w wersji z lektorem (Piper, offline), druga bez; porównanie po 7 dniach.
- **Budżet 0 zł na start:** bez płatnych API.

## 1. Co już mamy (analiza narzędzi)

| Obszar | Narzędzie | Status | Koszt |
|---|---|---|---|
| Research | `narzedzia/research.py` – RSS (Google News PL: ogólne, prawo, pieniądze, nauka; Rzeczpospolita; TVN24; Google News świat), ostatnie 72 h, deduplikacja | ✅ działa | 0 |
| Weryfikacja | WebSearch/WebFetch, API Sejmu (druki, ELI, ISAP), teksty ustaw w `zrodla/prawo/`, GUS/NBP/NASA/NIK/RPO | ✅ | 0 |
| Ranking | `narzedzia/ranking.py` – 6 kryteriów × 1–10, filtr „fakt + ≥2 źródła + w granicach” | ✅ | 0 |
| Scenariusz | skille `szkola-klamala-viral` (szablon C, karta 20 pkt), `ig-reel` (26 formuł haczyków) | ✅ | 0 |
| Obraz | silnik `render.py` (4K, animacje „mocne”, 11 obrazów okładek), Blender 3D, Remotion (opcja) | ✅ | 0 |
| Obrazy AI | Canva `generate-image` (konektor podłączony), Hugging Face (darmowe modele) – tylko styl nie-fotorealistyczny, bez twarzy i logo instytucji | 🟡 gotowe do testu | 0 (limity planu) |
| Wideo AI | Canva `create-video` (konektor) – do testu; płatne (Kling, Runway, Higgsfield) – poza budżetem | 🟡 / ⛔ | 0 / płatne |
| Muzyka i SFX | `muzyka.py` – oryginalny podkład + efekty zsynchronizowane z cięciami, −14 LUFS | ✅ | 0 |
| Lektor | `lektor.py` – Piper (głos `mc_speech`), napisy SRT; fabryka miksuje go z podkładem (`produkcja.py`) | ✅ MVP | 0 |
| Lepszy głos | ElevenLabs (polski, naturalny) – po zgodzie Michała, klucz w ustawieniach środowiska | ⛔ budżet | płatny abonament – cenę sprawdzić przed zakupem |
| Napisy | plansze tekstowe (domyślnie) + SRT z lektora; faster-whisper do nagrań | ✅ | 0 |
| Opisy | skille `ig-caption`, `ig-human`, `ig-story`, `ig-reply` | ✅ | 0 |
| Statystyki IG | Composio (tylko odczyt) – podłączone do zadania dziennego | ✅ | 0 |
| Statystyki TikTok/FB | brak API w budżecie → zrzuty ekranu albo `analityka.py dodaj` | 🟡 ręcznie | 0 |
| Autonomia | zadanie codzienne `trig_01SeXEiKGkqsPEVp6gZ8TnTi` (7:13) + skill `szkola-klamala-agent` | ✅ | w ramach planu Claude |
| Publikacja | ręcznie (decyzja) – paczka w `READY_TO_PUBLISH/` | ✅ | 0 |

## 2. Architektura (przepływ dzienny)

```
RSS + wyszukiwanie ──► RESEARCH/<data>/naglowki.md
        │  agent: wybór ok. 15 kandydatów, weryfikacja w źródłach pierwotnych, oceny 1–10
        ▼
TOPICS/<data>/tematy.json ──ranking.py──► TOP10.md + top3.json
        │  agent: dla TOP 3 – 3 warianty (kontrowersyjny / ciekawostkowy / emocjonalny), rekomendacja, karta 20 pkt
        ▼
SCRIPTS/<rid>/ (nowa_rolka.py)  scenariusz.md · spec.json (A, B, opcjonalnie _lektor) · opis.md · zrodla.md · meta.json
IMAGES/<rid>/prompty.md         okładka (obraz silnika) + prompty AI (opcja)
        │  produkcja.py (każda rolka osobno, w tle)
        ▼
VIDEOS/<rid>/     4K + TikTok 1080 (A, B, lektor)      VOICEOVER/<rid>/ wav      SUBTITLES/<rid>/ srt
        ▼
READY_TO_PUBLISH/<rid>/  pliki IG/TikTok, okładki, opis.md, zrodla.md, LISTA.md  ──► push do Michała
        │  Michał publikuje → `analityka.py opublikowano <rid>`
        ▼
PUBLISHED/<rid>/  +  ANALYTICS/wyniki.csv (Composio + zrzuty)  ──analityka.py raport──► ANALYTICS/raport.md
        └──────────────► wnioski → skill szkola-klamala-viral (sekcja 0) → wybór tematów jutro
```

Każda rolka ma własny folder `<rid>` (= `RRRR-MM-DD_<nazwa>`) w każdym katalogu etapu. Pliki MP4/WAV nie trafiają do gita (rozmiar) – Michał dostaje je przez wiadomość z plikami.

## 3. Co działa automatycznie, a co nie

| Krok | Auto | Uwagi |
|---|---|---|
| Przegląd wiadomości, ranking, scenariusze, render, okładki, opisy, paczka | ✅ | codziennie 7:13 (zadanie) |
| Weryfikacja faktów | ✅ z zastrzeżeniem | strony blokujące boty (np. TVN24 – 403) wymagają innego źródła; temat bez 2 źródeł nie przechodzi |
| Statystyki IG, komentarze IG | ✅ | Composio (odczyt) |
| Statystyki TikTok i Facebook | ❌ | zrzuty od Michała → `analityka.py dodaj` |
| Publikacja, odpowiedzi na komentarze | ❌ (celowo) | Michał zatwierdza; agent przygotowuje szkice |
| Dźwięk z trendów TikToka | ❌ | Michał wybiera w aplikacji |

## 4. Etapy wdrożenia

1. **MVP (4.11, ten commit):** struktura, research, ranking, szablony, produkcja z lektorem, paczka, analityka; pierwsze TOP 10 i TOP 3 z 4.11.
2. **Tydzień 1 (5–11.11):** agent dzienny pracuje według fabryki; test lektora (1 rolka/dzień z lektorem); dane do `ANALYTICS/wyniki.csv`.
3. **Tydzień 2:** raport A/B (haczyki A vs B, lektor vs bez, kategorie) → korekta wag rankingu; test obrazów AI z Canvy jako tła 1 planszy.
4. **Tydzień 3–4:** jeśli lektor wygrywa – decyzja o lepszym głosie (ElevenLabs, płatny); jeśli obrazy AI podnoszą czas oglądania – stałe użycie; formularz do wpisywania statystyk TikToka na telefonie (strona Artifact).

## 5. Narzędzia – szybka ściąga

```bash
cd VIRAL_REELS_FACTORY/narzedzia
python3 research.py                                   # nagłówki z 72 h
python3 ranking.py                                    # po zapisaniu TOPICS/<data>/tematy.json
python3 nowa_rolka.py zus_umorzenie --tytul "…" --lektor
python3 produkcja.py 2026-11-04_zus_umorzenie         # w tle (10–45 min)
python3 analityka.py dodaj 2026-11-04_zus_umorzenie --siec tt --wyswietlenia 1200 --sr-czas 6.1
python3 analityka.py opublikowano 2026-11-04_zus_umorzenie
python3 analityka.py raport
```
