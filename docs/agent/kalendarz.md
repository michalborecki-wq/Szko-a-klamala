# Kalendarz dostaw (Europe/Warsaw)

**Od 6.11 (decyzja Michała 5.11): 3 dostawy dziennie – 9:00 rolka (IG + TikTok), 13:00 post tylko na TikTok (karuzela zdjęć 9:16, 4 slajdy), 18:00 rolka (IG + TikTok). Każda dostawa = 1 materiał + opis. Nic więcej** (bez wariantów B, bez wersji z lektorem, bez paczek zbiorczych). Procedura: skill `szkola-klamala-agent`, sekcja „Dostawa”.

Agent czyta ten plik na starcie. Kolumna „Źródło”:
- **spec: plik#post_id** – scenariusz gotowy, tylko render (`dostawa.py`) i opis z podanego pliku;
- **NOWA** – agent sam wybiera temat (fabryka: research → weryfikacja w 2 źródłach → scenariusz C), dopisuje tu spec i opis.

**Od 9.11 (decyzja Michała 8.11):** każda rolka w stylu Dynamic Visual Engine (skill `szkola-klamala-dynamic-visual`) i według zasady dziennikarstwa śledczego (skill `szkola-klamala-redakcja`, sekcja 7a).

**Uwaga 7.11:** po zamachu w Krakowie (7.11) przez kilka dni bez rolek o broni i bez zaczepnych rolek o policji; nigdy treści wykorzystujących to wydarzenie.

Po wysłaniu agent zmienia status na **wysłane**. **Decyzja Michała 8.11: „Masz kontynuować do odwołania”** – gdy brakuje dni, agent sam je dopisuje i robi materiał jako NOWA (pełna weryfikacja). Reguła: 9:00 – prawo/finanse/motoryzacja/medycyna/ciekawostka; 13:00 – karuzela 9:16 z wiedzy ogólnej (kosmos, ciało, mózg, rekordy; szablon B, **nie policja**, temat inny niż rolki tego dnia); 18:00 w pon., śr., pt. – „Co może policja”, w pozostałe dni (wt., czw., sob., nd.) – **NEWS: rolka z bieżących informacji** (skill `szkola-klamala-sledczy`, decyzja Michała 10.11: agent jak dziennikarz śledczy). Link od Michała ma pierwszeństwo przed kalendarzem.

> **Od 12.11:** każda rolka 9:00 i 18:00 najpierw z gorących tematów (sledczy.py + test kontrowersji); wpis w tabeli jest rezerwą, gdy żaden news nie przejdzie weryfikacji.

| Data | Pora | Rolka | Źródło (spec) | Opis | Status |
|---|---|---|---|---|---|
| czw. 5.11 | 9:00 | IKE – 28 260 zł przepada 31.12 | `specs/tydzien_4-8.11_r2-9.json#finanse_ike_limit` | `docs/agent/opisy/tydzien_4-8.11.md` (czw. 5.11, IKE) | wysłane (5.11 rano) |
| czw. 5.11 | 18:00 | Co może policja #4 – kontrola osobista | `specs/tydzien_4-8.11_r2-9.json#prawo_policja4_kontrola` | j.w. (Co może policja #4) | wysłane (5.11 wieczór) |
| pt. 6.11 | 9:00 | Punkty karne znikają rok po zapłacie | `specs/tydzien_4-8.11_r2-9.json#moto_punkty_rok` | j.w. (Motoryzacja: punkty karne) | do wysłania |
| pt. 6.11 | 13:00 | NOWA – karuzela 9:16 (TikTok) | NOWA | NOWA | do zrobienia |
| pt. 6.11 | 18:00 | Broń palną możesz mieć bez pozwolenia (czarnoprochowa) – decyzja Michała 6.11 | `publikacje/2026-11-06/spec_prawo_bron_czarnoprochowa.json#prawo_bron_czarnoprochowa` | `publikacje/2026-11-06/1800_opis.md` | wysłane (6.11, sesja główna) |
| sob. 7.11 | 9:00 | Ruletka – 2,7% | `specs/tydzien_4-8.11_r2-9.json#mat_ruletka` | j.w. (Matematyka: ruletka) | do wysłania |
| sob. 7.11 | 13:00 | NOWA – karuzela 9:16 (TikTok) | NOWA | NOWA | do zrobienia |
| sob. 7.11 | 18:00 | Saturn pływałby w wodzie (TikTok Shop: ROBOTIME globus 3D) – zamiast policji #6 po zamachu w Krakowie | `specs/tydzien_4-8.11_r2-9.json#kosmos_saturn_woda` | `publikacje/2026-11-07/1800_opis.md` | wysłane (7.11, sesja główna) |
| nd 8.11 | 9:00 | NOWA – temat neutralny (ciało, mózg, rekord), bez broni, policji i przemocy (dzień po zamachu w Krakowie) | NOWA | NOWA | do zrobienia |
| nd 8.11 | 13:00 | NOWA – karuzela 9:16 (TikTok) | NOWA | NOWA | do zrobienia |
| nd 8.11 | 18:00 | Co może policja #7 – milczenie | `specs/tydzien_4-8.11_r2-9.json#prawo_policja7_milczenie` | j.w. (Co może policja #7) | wysłane (8.11, sesja główna) |
| pon. 9.11 | 9:00 | ZUS daruje 315 mln zł. Jest haczyk. (nowy styl: plansza `dokument` z art. 6 druku 3010) | `publikacje/2026-11-09/spec_zus_umorzenie.json#zus_umorzenie` | `publikacje/2026-11-09/0900_opis.md` | wysłane (8.11 wieczorem, sesja główna) |
| pon. 9.11 | 13:00 | Największa pustynia świata jest z lodu (Antarktyda 14,2 mln km² vs Sahara 9,2 mln km²) | `publikacje/2026-11-09/spec_pustynia_antarktyda.json#pustynia_antarktyda` | `publikacje/2026-11-09/1300_opis.md` | wysłane (9.11 12:15, sesja główna – wersja z sesji zadania nie dotarła) |
| pon. 9.11 | 18:00 | Co może policja #5 – „Mandat? Możesz powiedzieć »nie«” (art. 97 § 2–3, art. 99 KPSW) | `publikacje/2026-11-09/spec_policja5_mandat.json#policja5_mandat` | `publikacje/2026-11-09/1800_opis.md` | wysłane (9.11 ok. 18:40, sesja główna – sesja zadania nie pobrała repozytorium) |
| wt. 10.11 | 9:00 | Pieniądze bez ściemy: „500 zł miesięcznie przez 30 lat to nie 180 tys. zł” (F3, przesunięte z 12.11) | `publikacje/2026-11-10/spec_finanse_500zl.json#finanse_500zl` | `publikacje/2026-11-10/0900_opis.md` | wysłane (sesja główna, 10.11 rano) – NIE ROBIĆ |
| wt. 10.11 | 13:00 | NOWA – karuzela 9:16 (TikTok) | NOWA | NOWA | do zrobienia |
| wt. 10.11 | 18:00 | „Pilny komunikat skarbówki” to nie kara – PIT telefonem od 5.11 (temat od Michała, RMF FM) | `publikacje/2026-11-10/spec_pit_telefon.json#pit_telefon` | `publikacje/2026-11-10/1800_opis.md` | wysłane (sesja główna, 10.11 rano) – NIE ROBIĆ |
| śr. 11.11 | 9:00 | Mit tygodnia: „Wielkiego Muru nie widać z Księżyca” (tło: klip AI „tablica” z Higgsfield, etykieta „Ilustracja AI”) | `publikacje/2026-11-11/spec_mur_ksiezyc.json#mur_ksiezyc` | `publikacje/2026-11-11/0900_opis.md` | wysłane (11.11 7:41, sesja główna – zaplanowana wysyłka) |
| śr. 11.11 | 13:00 | NOWA – karuzela 9:16 (TikTok) | NOWA | NOWA | do zrobienia |
| śr. 11.11 | 18:00 | Co może policja #6 – „+51 km/h na krajówce i 3 miesiące pieszo” – zwrot: autostrada (dwie jezdnie) poza przepisem; stary scenariusz „poza miastem prawko zostaje” NIEAKTUALNY od 3.03.2026 (Dz.U. 2025 poz. 1676, art. 4 pkt 25) | `publikacje/2026-11-11/spec_policja6_autostrada.json#policja6_autostrada` | `publikacje/2026-11-11/1800_opis.md` | wysłane (11.11 18:30, spóźnione – restart sesji) |

| czw. 12.11 | 9:00 | Śledztwo: „Pożyczasz 6000 zł. Oddajesz 13 000.” – pożyczka z obowiązkowym kursem (NEWS: „Pożyczka za kurs. Zarzuty dla spółek…”, UOKiK, 10.11.2026; TVN24, 300Gospodarka); tło: klip AI „waga” | `publikacje/2026-11-12/spec_pozyczka_kurs.json#pozyczka_kurs` | `publikacje/2026-11-12/0900_opis.md` | wysłane (12.11 7:08, sesja główna) |
| czw. 12.11 | 13:00 | NOWA – karuzela 9:16 (kosmos/ciało/rekord) | NOWA | NOWA | do zrobienia |
| czw. 12.11 | 18:00 | Śledztwo: „Mandat za letnie opony: 0 zł. Jest haczyk.” – OC płaci zawsze, AC może odmówić (art. 827 § 1 KC; NEWS: Elektromobilni.pl, Forsal.pl, 11.11); tło: klip AI „lupa” | `publikacje/2026-11-12/spec_zimowki_ac.json#zimowki_ac` | `publikacje/2026-11-12/1800_opis.md` | wysłane (automat 16:11 w swojej sesji – Michał nie widział; ponownie z sesji głównej 19:40) |
| pt. 13.11 | 9:00 | NOWA – motoryzacja albo prawo w codzienności | NOWA | NOWA | ROBI SESJA GŁÓWNA (wysyłka w rozmowie głównej ok. 8:00 / 17:00) – zadanie cykliczne NIE ROBI tej rolki |
| pt. 13.11 | 13:00 | NOWA – karuzela 9:16 | NOWA | NOWA | do zrobienia |
| pt. 13.11 | 18:00 | Co może policja #8 – „Masz prawo znać nazwisko policjanta” (§ 2 ust. 1 rozp. RM, Dz.U. 2023 poz. 2535) | NOWA (P1) | NOWA | ROBI SESJA GŁÓWNA (wysyłka w rozmowie głównej ok. 8:00 / 17:00) – zadanie cykliczne NIE ROBI tej rolki |
| sob. 14.11 | 9:00 | Mit tygodnia: „Największa pustynia świata jest z lodu” – rolka IG (tło: klip AI „antarktyda”) | `publikacje/2026-11-14/spec_antarktyda_pustynia.json#antarktyda_pustynia` | `publikacje/2026-11-14/0900_opis.md` | gotowe (sesja główna, wysyłka zaplanowana 14.11 ok. 7:45) – NIE ROBIĆ |
| sob. 14.11 | 13:00 | NOWA – karuzela 9:16 | NOWA | NOWA | do zrobienia |
| sob. 14.11 | 18:00 | NEWS – rolka z bieżących informacji (skill `szkola-klamala-sledczy`: `sledczy.py` → wybór → dokument pierwotny + 2. źródło); bez broni, przemocy i tragedii | NEWS | NOWA | do zrobienia |
| nd 15.11 | 9:00 | NOWA – kosmos/rekord (szablon B) | NOWA | NOWA | do zrobienia |
| nd 15.11 | 13:00 | NOWA – karuzela 9:16 | NOWA | NOWA | do zrobienia |
| nd 15.11 | 18:00 | NEWS – rolka z bieżących informacji (skill `szkola-klamala-sledczy`: `sledczy.py` → wybór → dokument pierwotny + 2. źródło); bez broni, przemocy i tragedii | NEWS | NOWA | do zrobienia |
| pon. 16.11 | 9:00 | NOWA – prawo w codzienności | NOWA | NOWA | do zrobienia |
| pon. 16.11 | 13:00 | NOWA – karuzela 9:16 | NOWA | NOWA | do zrobienia |
| pon. 16.11 | 18:00 | Co może policja #9 – „Policjant w cywilu? Poproś o legitymację – i ją przepisz” (§ 2 ust. 2 rozp. RM) | NOWA (P2) | NOWA | do zrobienia |
| wt. 17.11 | 9:00 | NOWA – motoryzacja (przepisy, mity kierowców) | NOWA | NOWA | do zrobienia |
| wt. 17.11 | 13:00 | NOWA – karuzela 9:16 | NOWA | NOWA | do zrobienia |
| wt. 17.11 | 18:00 | NEWS – rolka z bieżących informacji (skill `szkola-klamala-sledczy`: `sledczy.py` → wybór → dokument pierwotny + 2. źródło); bez broni, przemocy i tragedii | NEWS | NOWA | do zrobienia |
| śr. 18.11 | 9:00 | NOWA – nauka/mózg | NOWA | NOWA | do zrobienia |
| śr. 18.11 | 13:00 | NOWA – karuzela 9:16 | NOWA | NOWA | do zrobienia |
| śr. 18.11 | 18:00 | Co może policja #10 – „Zatrzymanie nielegalne? Sąd może Cię wypuścić od ręki” (art. 246 § 1–3 KPK) | NOWA (P6) | NOWA | do zrobienia |
| czw. 19.11 | 9:00 | Black Friday – „»Było 999 zł« to nie jest cena sprzed promocji” (najniższa cena z 30 dni, art. 4 ust. 2 ustawy o informowaniu o cenach – sprawdzić w ISAP; start oficjalnej sprzedaży TikTok Shop 19.11) | NOWA (S2) | NOWA | do zrobienia |

Wcześniej (4.11, ręcznie): Co może policja #3 – 48 h – wysłane.
