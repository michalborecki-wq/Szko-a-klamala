# Zespół marketingu: 0 pracowników, 42 agentów

> **25.11 (decyzja Michała „zbuduj cały zespół marketingowy… promocja marki, budowa wizerunku, reklama”):** dodany 7. dział **Promocja i wizerunek** – strateg marki, reklama płatna (tylko plany do decyzji Michała), PR i media, współprace z twórcami, profil i wyszukiwanie, kampanie i akcje. Tryb: `/zespol promocja`. Wyniki: `docs/zespol/promocja/`.

Wzór: schemat „A marketing team with 0 employees: 36 Claude agents” (TikTok, zrzut Michała 17.11). Został przerobiony na zasady konta @szkola_klamala.

- **Michał jest w środku pętli.** Tylko on publikuje, wysyła, odpowiada i podpisuje.
- Agenci przygotowują pliki i szkice.
- Dyrygentem jest główna sesja Claude Code ze skillem `zespol-marketingu` (polecenie `/zespol`), bo podagent nie może uruchamiać innych podagentów.

```
        RESEARCH (6)                         CONTENT (6)
  zwiadowca-trendow                     grafik
  sluchacz-odbiorcow                    karuzele
  gornik-komentarzy      ┌────────┐     lektor (wstrzymany)
  obserwator-konkurencji │ Claude │     montazysta
  scenarzysta            │  Code  │     straznik-marki
  autor-maili            │/zespol │     biurko-akceptacji
                         └───┬────┘
        THE LOOP (6)         │ MICHAŁ      PUBLISH (6) – paczki, NIE publikacja
  analityk-postow            │ (akceptuje  planista
  przychody                  │  i publikuje) paczka-tiktok
  tracker-rozmow             │             paczka-reels
  analityk-maili             │             paczka-karuzela (zamiast Shorts)
  raport-tygodniowy          │             paczka-relacja (zamiast X)
  karmienie-petli            │             newsletter (uśpiony)

        SALES (6) – sponsorzy                COMMUNITY (6) – szkice
  ocena-leadow                          odpowiedzi-komentarze
  umawianie-rozmow                      dm
  przypominacz                          baza-faq
  follow-up                             pytanie-dyskusji (zamiast próśb o opinie)
  oferta-i-platnosc (płatności: NIE)    lowca-leadow
  crm                                   eskalacja
```

Wszyscy agenci mają prefiks `zm-` i pliki w `.claude/agents/`. Pełna tabela jest w `AGENCI.md`. Zasady wspólne są w `ZASADY.md`.

## Co zmieniliśmy względem schematu i dlaczego

| Schemat | U nas | Powód |
|---|---|---|
| TikTok / Reels / Shorts / X Poster | „Paczka …” – plik + opis do skopiowania | Michał publikuje ręcznie (CLAUDE.md) |
| Shorts Poster, X Poster | karuzela 13:00 na TikToku, relacja IG | nie prowadzimy YouTube ani X |
| Newsletter | uśpiony, tylko szkic | newsletter nie jest uruchomiony |
| Review Asker | pytanie do dyskusji (przypięty komentarz) | prośby o oceny i polubienia to engagement bait |
| Payment Link | oferta + przypomnienie o podatku; bez linków płatności | brak systemu płatności – NIEUKOŃCZONE, decyzja Michała |
| Call Booker | szkic z terminami | kalendarz zmienia tylko Michał albo agent za jego zgodą |
| Voiceover | tylko na prośbę | test lektora wstrzymany 4.11 |
| Comment Replier / DM Agent | szkice do wklejenia | nie odpowiadamy z konta automatycznie |

## Przepływy (kto po kim)

1. **Rolka (dostawa 9:00 / 18:00):** zwiadowca-trendow → scenarzysta → straznik-marki → grafik → montazysta → paczka-reels + paczka-tiktok + paczka-relacja + pytanie-dyskusji → straznik-marki → biurko-akceptacji → Michał. To jest ta sama praca, którą robi zadanie cykliczne. Zespół jej nie dubluje, tylko dzieli na role.
2. **Post 13:00 (TikTok):** scenarzysta → karuzele → paczka-karuzela → straznik-marki → biurko-akceptacji.
3. **Społeczność (po publikacji):** odpowiedzi-komentarze + dm (równolegle) → lowca-leadow / eskalacja → straznik-marki → szkice dla Michała.
4. **Sponsor:** lowca-leadow → ocena-leadow → umawianie-rozmow → tracker-rozmow → oferta-i-platnosc → crm. W tle przypominacz i follow-up.
5. **Tydzień (niedziela):** analityk-postow + przychody + analityk-maili (równolegle) → raport-tygodniowy → karmienie-petli → zwiadowca/obserwator na nowy tydzień.

## Gdzie co leży

| Folder | Zawartość |
|---|---|
| `docs/zespol/research/` | trendy, odbiorcy |
| `docs/zespol/kontrola/` | werdykty strażnika marki |
| `docs/zespol/akceptacja.md` | kolejka do Michała |
| `docs/zespol/spolecznosc/` | szkice odpowiedzi i DM, `faq.md`, `eskalacje.md` |
| `docs/zespol/sprzedaz/` | `crm.md`, `maile/`, `rozmowy/`, `oferty/` |
| `docs/zespol/petla/` | `przychody.md` |
| `docs/zespol/skrzynka/` | wklejki od Michała (zrzuty z TikToka, DM, maile) |
| `publikacje/RRRR-MM-DD/`, `VIRAL_REELS_FACTORY/DOSTAWA/` | materiały do publikacji (bez zmian) |

## Zmiany w zespole

Edytuj definicje w `scripts/zespol/generuj_agentow.py`, potem uruchom `python3 scripts/zespol/generuj_agentow.py`. Skrypt nadpisuje `.claude/agents/zm-*.md` i `AGENCI.md`.
