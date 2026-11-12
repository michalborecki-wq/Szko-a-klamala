# Lekcje – czytać PRZED każdą rolką (decyzja Michała 11.11: „wyciągaj wnioski, ucz się, dąż do perfekcji”)

Po każdej dostawie dopisz 1–3 linijki: co poszło źle/dobrze i jaka reguła z tego wynika. Reguły stosuj od następnej rolki.

## STANDARD KAŻDEJ ROLKI (decyzja Michała 11.11 – „dynamiczna animacja, kolory, kontrowersyjna treść”)
Każda rolka (9:00, 18:00, także karuzele w miarę możliwości) MUSI mieć wszystkie punkty:
1. **Kontrowersja w haczyku** – stwierdzenie, które budzi sprzeciw albo „to niesprawiedliwe” (porównanie niesprawiedliwości, ukryta stawka, nagłówek straszy – treść nie); zawsze prawdziwe, 2 źródła, w granicach zakazów.
2. **Dynamiczna animacja na pełnej mocy** – `"moc": "mocna"` (kadr nigdy nie stoi, puls na bicie), `"ton"` z presetem przejść, `fx`, liczby z `"count": true`, plansza `dokument` z markerem, `myth` TWIST ze stop-klatką na zwrocie, choreografia wejść (co prowadzi, co dołącza na uderzeniu – skill `choreograph`).
3. **Kolory na pełnej palecie marki** – żółty #FFC727 na liczbie/kluczowym słowie, czerwony #E53935 na stawce/karze/TWIST, niebieskie smugi #2F6BFF w ruchu; kontrast tła i tekstu ≥ 4,5:1; nigdy szare, płaskie plansze.
4. **Ruch w 1. sekundzie** – tło wideo (klip AI z etykietą, `tlo3d`) albo obraz-bohater na okładce + pieczątka.
5. **Muzyka i efekty** zsynchronizowane z cięciami (`--muzyka`, −14 LUFS), uderzenie na zwrocie i na logo.
6. **Min. 1 nowość** względem poprzedniej rolki (inny preset, mapa, foto, wycinek, nowy efekt) – zapisz w dzienniku, jaka.
7. **Kontrola przed wysyłką** – `kontrola.py` + obejrzenie arkusza klatek; plansza czytelna (0,3 s/słowo), maks. ok. 12–15 słów.

## KONTROWERSJA PRZEDE WSZYSTKIM (decyzja Michała 11.11 wieczorem: „Nastaw się na kontrowersje w treści. To jest najbardziej chwytliwe”)
Temat wybieramy po sile sporu, nie po „ciekawości”. Rolka bez sporu nie wchodzi do slotów 9:00 i 18:00 (może być karuzelą 13:00).
**Test kontrowersji – temat musi spełnić min. 2 z 4:**
1. *Niesprawiedliwość:* dwie podobne sytuacje, różne traktowanie (krajówka vs autostrada, wiatrówka vs broń czarnoprochowa).
2. *Pieniądze widza:* państwo/urząd/firma zabiera, dolicza albo „daruje” z haczykiem – konkretna kwota.
3. *Władza nad zwykłym człowiekiem:* co wolno policji, urzędowi, ochronie, pracodawcy – i gdzie jest granica.
4. *Dwie strony:* połowa widzów powie „słusznie”, połowa „skandal” – pytanie końcowe dzieli salę („Słusznie czy za surowo?”).
**Jak pisać:** haczyk nazywa spór wprost („Za to samo: tu kara, tam nic.”); zwrot akcji pokazuje lukę albo podwójny standard; ostatnia plansza pyta o OCENĘ zasady (nie o fakt) – widz ma mieć zdanie od razu.
**Granice bez zmian (CLAUDE.md):** tylko prawda z dokumentu + 2 źródła; fakt zamiast oceny („przepis mówi…”, nie „to skandal”); bez ataku na osoby, bez partii, bez wojen, religii, szczepionek, płci, migracji, spisków, tragedii i drastycznych opisów; stanowisko drugiej strony w opisie. Kontrowersja = prawdziwy podwójny standard, nie przesada w nagłówku.
**Źródła tematów:** raporty NIK i RPO, wyroki, taryfikatory i ich luki, nowe ustawy (ukryta stawka), różnice „dla jednych tak, dla drugich nie” (ulgi, przywileje grup zawodowych, kary).

## GORĄCE TEMATY + ŚLEDZTWO (decyzja Michała 11.11)
Każda rolka 9:00 i 18:00: najpierw `python3 VIRAL_REELS_FACTORY/narzedzia/sledczy.py --godziny 48 --top 15` → 3 kandydaci z pierwszych stron → test kontrowersji → dokument pierwotny + 2. źródło (maks. 20 min na kandydata) → rolka dodaje to, czego nie ma w nagłówku. Brak kandydata = temat z kalendarza. Procedura: skill `szkola-klamala-sledczy`, sekcja 1.
Uwaga na nagłówki-straszaki („najniebezpieczniejsza w UE”, „bezwzględna zasada”) – sprawdź w dokumencie, często teza jest słabsza; wtedy rolka „nagłówek straszy, dokument mówi…”.

## HACZYK – wzór z danych (analiza 11.11, `docs/analiza-wynikow-2026-11-11.md`)
- ≤ 7 słów; zaczyna się od podmiotu znanego każdemu (ZUS, policja, mandat, szkoła, bank); jedna liczba albo jedno zaprzeczenie; kończy się otwartą pętlą („Jest haczyk.”, „Połowa – bezprawnie.”, „Szkoła kłamała.”).
- NIE: znak „+”, skróty, żargon („krajówka”), pytanie w 1. linii, zdanie do policzenia. Przykład zły: „+51 km/h na krajówce i 3 miesiące pieszo” (97% pominięć). Lepiej: „Policja zabierze prawo jazdy za miastem. Jest wyjątek.”
- Cytat w `dokument` ≤ 18 słów, plansza ≤ 12 słów, rolka 20–26 s, zwrot (`myth`) najpóźniej na 3. planszy.
- Silnik od 11.11 sam: okładka żółta/ciemna na zmianę (gdy brak `tlo3d` i `uklad`), tekst rośnie do wypełnienia kadru, TWIST czerwony, outro z żółtym przyciskiem „Wyślij komuś” (pole `sub` zaczynaj od „Wyślij komuś, kto…”).

## Zasada dostawy (11.11)
- **Rolka u Michała ok. 1 h przed publikacją:** 9:00 → wysłane ok. 8:00, 18:00 → ok. 17:00, 13:00 → ok. 12:00. Start pracy min. 1,5 h przed wysyłką (render 4K 15–25 min, poprawki).
- **Wszystkie narzędzia, które realnie podnoszą jakość:** pełny Dynamic Visual Engine (ton, moc mocna, `dokument`, `myth` TWIST, liczby `count`), tło wideo z niewykorzystanego zasobu AI (`zrodla/ai_higgsfield/*/INFO.md`) z etykietą, okładka z obrazem i pieczątką, zasady ruchu (choreograph – Emil Kowalski), kontrola `kontrola.py` + obejrzenie arkusza klatek. Płatne kredyty (Higgsfield, Adobe Firefly) tylko za zgodą Michała.
- **Pliki wysyłać pojedynczo** (5 osobnych wysyłek) – paczka 5 plików naraz nie dała się zapisać (11.11).
- Gdy o T–20 min render nie jest gotowy: wyślij, co jest, i powiedz uczciwie.

## Lekcje
- 11.11 – stary spec z kalendarza (Policja #6, 7.11) miał nieaktualny zwrot: nowela Dz.U. 2025 poz. 1676 od 3.03.2026 objęła drogi jednojezdniowe poza miastem. **Reguła:** przed użyciem specu starszego niż 2 dni sprawdź `zrodla/prawo/policja/zmiany/` i wyszukaj „<temat> 2026 nowe przepisy”.
- 11.11 – w planszy `myth` pola to `myth`/`fact` (nie `title`/`accent`) – render padł z `KeyError: 'myth'`. **Reguła:** wzoruj się na działającym specu z ostatnich dni.
- 11.11 – restart procesu zjadł ~1 h i rolka przyszła 18:30. **Reguła:** zaczynaj wcześniej (zasada dostawy wyżej); render uruchamiaj `setsid` w tle i loguj do pliku.
- 11.11 – rolka 39 s, bo silnik wydłużył planszę z długim przepisem. **Reguła:** cytat w `dokument` ≤ 18 słów; reszta przepisu w opisie.
- 11.11 – Michał pytał, czy wygląd go zaskoczy; uczciwa odpowiedź: standard. **Reguła:** każda rolka ma min. 1 element nowy względem poprzedniej (tło wideo, mapa, foto, wycinek, nowy preset przejść) – zapisz w dzienniku, który.
- 11.11 – start zadania cyklicznego 16:23 padł: USAGE_LIMIT_REACHED (limit użycia konta), stąd brak rolki 18:00. Starty przesunięte na 6:23/10:23/15:23. **Reguła:** sesja główna pilnuje slotów, gdy limit jest blisko.
- 12.11 – na planszy `myth` w wideo podświetlone słowa były żółte na żółtym (animacja `kHi` kończy na żółtym kolorze tekstu; w podglądzie statycznym tego nie widać). Poprawione w silniku (`!important`). **Reguła:** arkusz klatek z gotowego WIDEO oglądać zawsze – sam podgląd plansz nie wystarcza; każdą zmianę CSS sprawdzać w obu wariantach animacji.
- 12.11 – render 4K z tłem wideo: ok. 13 min obraz + 3 min muzyka i paczka; drugi render po poprawce zmieścił się, bo start był 6:30. Start 1,5 h przed wysyłką zostaje.
- 12.11 – skaner: cennik skupu (prosięta, drób) dostaje wysokie punkty za słowo „ceny” – do odfiltrowania (rolnicze portale branżowe).
