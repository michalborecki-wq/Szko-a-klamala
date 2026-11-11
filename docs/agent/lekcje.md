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
