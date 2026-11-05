# Kalendarz dostaw (Europe/Warsaw)

**Od 6.11 (decyzja Michała 5.11): 3 dostawy dziennie – 9:00 rolka (IG + TikTok), 13:00 post tylko na TikTok (karuzela zdjęć 9:16, 4 slajdy), 18:00 rolka (IG + TikTok). Każda dostawa = 1 materiał + opis. Nic więcej** (bez wariantów B, bez wersji z lektorem, bez paczek zbiorczych). Procedura: skill `szkola-klamala-agent`, sekcja „Dostawa”.

Agent czyta ten plik na starcie. Kolumna „Źródło”:
- **spec: plik#post_id** – scenariusz gotowy, tylko render (`dostawa.py`) i opis z podanego pliku;
- **NOWA** – agent sam wybiera temat (fabryka: research → weryfikacja w 2 źródłach → scenariusz C), dopisuje tu spec i opis.

Po wysłaniu agent zmienia status na **wysłane**. Gdy brakuje dni – dopisuje kolejne: 9:00 – prawo/finanse/motoryzacja/medycyna/ciekawostka; 13:00 – karuzela 9:16 z wiedzy ogólnej (kosmos, ciało, mózg, rekordy; szablon B, **nie policja**, temat inny niż rolki tego dnia); 18:00 w pon., śr., pt. – „Co może policja”, w pozostałe dni – temat z fabryki z mocną kontrowersją.

| Data | Pora | Rolka | Źródło (spec) | Opis | Status |
|---|---|---|---|---|---|
| czw. 5.11 | 9:00 | IKE – 28 260 zł przepada 31.12 | `specs/tydzien_4-8.11_r2-9.json#finanse_ike_limit` | `docs/agent/opisy/tydzien_4-8.11.md` (czw. 5.11, IKE) | wysłane (5.11 rano) |
| czw. 5.11 | 18:00 | Co może policja #4 – kontrola osobista | `specs/tydzien_4-8.11_r2-9.json#prawo_policja4_kontrola` | j.w. (Co może policja #4) | do wysłania |
| pt. 6.11 | 9:00 | Punkty karne znikają rok po zapłacie | `specs/tydzien_4-8.11_r2-9.json#moto_punkty_rok` | j.w. (Motoryzacja: punkty karne) | do wysłania |
| pt. 6.11 | 13:00 | NOWA – karuzela 9:16 (TikTok) | NOWA | NOWA | do zrobienia |
| pt. 6.11 | 18:00 | Co może policja #5 – dowód osobisty | `specs/tydzien_4-8.11_r2-9.json#prawo_policja5_dowod` | j.w. (Co może policja #5) | do wysłania |
| sob. 7.11 | 9:00 | Ruletka – 2,7% | `specs/tydzien_4-8.11_r2-9.json#mat_ruletka` | j.w. (Matematyka: ruletka) | do wysłania |
| sob. 7.11 | 13:00 | NOWA – karuzela 9:16 (TikTok) | NOWA | NOWA | do zrobienia |
| sob. 7.11 | 18:00 | Co może policja #6 – +51 km/h | `specs/tydzien_4-8.11_r2-9.json#prawo_policja6_50kmh` | j.w. (Co może policja #6) | do wysłania |
| nd 8.11 | 9:00 | Saturn pływałby w wodzie | `specs/tydzien_4-8.11_r2-9.json#kosmos_saturn_woda` | j.w. (Kosmos: Saturn) | do wysłania |
| nd 8.11 | 13:00 | NOWA – karuzela 9:16 (TikTok) | NOWA | NOWA | do zrobienia |
| nd 8.11 | 18:00 | Co może policja #7 – milczenie | `specs/tydzien_4-8.11_r2-9.json#prawo_policja7_milczenie` | j.w. (Co może policja #7) | do wysłania |
| pon. 9.11 | 9:00 | ZUS daruje 315 mln zł. Jest haczyk. | `VIRAL_REELS_FACTORY/SCRIPTS/2026-11-04_zus_umorzenie/spec.json#zus_umorzenie` | `VIRAL_REELS_FACTORY/SCRIPTS/2026-11-04_zus_umorzenie/opis.md` (bez linii o B i lektorze) | do wysłania |
| pon. 9.11 | 13:00 | NOWA – karuzela 9:16 (TikTok) | NOWA | NOWA | do zrobienia |
| pon. 9.11 | 18:00 | Co może policja #8 | NOWA (`docs/seria-policja.md`) | NOWA | do zrobienia |
| wt. 10.11 | 9:00 | Pod szlabanem tracisz prawo jazdy | `VIRAL_REELS_FACTORY/SCRIPTS/2026-11-04_przejazdy_kolejowe/spec.json#przejazdy_kolejowe` | `…/2026-11-04_przejazdy_kolejowe/opis.md` | do wysłania |
| wt. 10.11 | 13:00 | NOWA – karuzela 9:16 (TikTok) | NOWA | NOWA | do zrobienia |
| wt. 10.11 | 18:00 | Nawigacja w telefonie – 500 zł | `VIRAL_REELS_FACTORY/SCRIPTS/2026-11-04_nawigacja_telefon/spec.json#nawigacja_telefon` | `…/2026-11-04_nawigacja_telefon/opis.md` | do wysłania |
| śr. 11.11 | 9:00 | NOWA (fabryka) | NOWA | NOWA | do zrobienia |
| śr. 11.11 | 13:00 | NOWA – karuzela 9:16 (TikTok) | NOWA | NOWA | do zrobienia |
| śr. 11.11 | 18:00 | Co może policja #9 | NOWA | NOWA | do zrobienia |

Wcześniej (4.11, ręcznie): Co może policja #3 – 48 h – wysłane.
