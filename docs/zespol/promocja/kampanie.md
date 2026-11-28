# Kampanie i akcje – kalendarz okazji i plan kampanii

Autor: zm-kampanie-i-akcje (dział Promocja i wizerunek). Przekazanie: zm-planista, zm-scenarzysta.
Kampania **nie zmienia slotów ani zasad z CLAUDE.md** – podsuwa tematy do 9:00 / 13:00 / 18:00 i do relacji. Gorący temat z `sledczy.py`/`pilne.py` i link od Michała mają pierwszeństwo – wpisy poniżej są rezerwą i ramą kampanii.

---

## Kalendarz 29.11–13.12

Stan na sob. 28.11.2026, 14:30. Kontekst: `docs/zespol/promocja/2026-11_strategia.md`, sekcja 7.

### 1. Metoda (jak sprawdzono)

- Lista Dziennika Ustaw 2026 z API Sejmu (`https://api.sejm.gov.pl/eli/acts/DU/2026`, 1565 pozycji, ostatnia ogłoszona 26.11.2026). Dla każdej ustawy i rozporządzenia z 2026 r. pobrano szczegóły (`/eli/acts/DU/2026/<poz>`): pola `entryIntoForce` i `comments` (przepisy z innym terminem wejścia w życie). Dodatkowo ustawy z DU 2025 (terminy odroczone).
- Filtr: wejście w życie (całość lub część) 29.11–13.12.2026. Treść przepisów przeczytana w PDF z API (`/text.pdf`).
- Liczby (procenty, daty, rocznice) policzone w kodzie (Python), nie z głowy.
- Ograniczenia: nie sprawdzano DU 2024 i starszych (możliwe odroczone przepisy – BRAK) ani Monitora Polskiego. Wejście w życie 1.01.2027 – osobny przegląd na początku grudnia.

### 2. Przepisy wchodzące w życie 29.11–13.12 (Dziennik Ustaw)

| Od | Akt (Dz.U.) | Co zmienia (z tekstu aktu) | Dla zwykłego człowieka? |
|---|---|---|---|
| 30.11 | 2026 poz. 1431 – rozp. MZ, procedury dyspozytora medycznego | dyspozytor odczytuje wzywającemu adres i lokalizację wpisane przez operatora i prosi o potwierdzenie (§ 3 ust. 1 pkt 4); może odwołać wyjazd zespołu w 3 przypadkach: zdarzenie o wyższym priorytecie, inny zespół dojedzie szybciej, odwołanie przez wzywającego lub kierownika innego zespołu na miejscu (§ 8 ust. 3) | TAK – każdy, kto dzwoni po karetkę |
| 30.11 | 2026 poz. 1550 – rozp. MSWiA, zakaz przebywania w strefie nadgranicznej z Białorusią (90 dni, pas ok. 200 m) | czasowy zakaz przebywania | **POZA KONTEM** – temat graniczny styka się z migracją (zakaz z CLAUDE.md) |
| 1.12 | 2026 poz. 1270 – ustawa o VAT, art. 1 pkt 13 lit. b | stawka VAT do różnicy w wartości kaucji (system kaucyjny) | słabo – rozliczenie firm |
| 1.12 | 2026 poz. 1347 – nowelizacja ustawy o OZE (część przepisów) | m.in. zwrot prosumentowi niewykorzystanej nadpłaty przy zmianie sprzedawcy (art. 4 ust. 13b) | średnio – **do sprawdzenia**, czy ten punkt wchodzi 1.12 czy w terminie wyjątku (art. końcowy ma kilka dat) |
| 2.12 | 2026 poz. 1508 – rozp. MS, wydatki Skarbu Państwa w postępowaniu karnym | ryczałt za doręczenia 20 zł → 50 zł i teraz **od każdego** podejrzanego/oskarżonego; przewóz osoby na żądanie sądu 20 → 50 zł; przechowanie zajętych rzeczy 40 → 100 zł (20 → 50 zł przy kilku oskarżonych); doręczenia w mediacji 30 → 50 zł; **osoba przybrana do okazania (statysta) 12 → 20 zł**. Wzrosty: +150% (20→50, 40→100), +67% (30→50, 12→20). Stare stawki: tekst jednolity Dz.U. 2013 poz. 663 | TAK – podejrzani, oskarżeni, statyści w okazaniu, policja |
| 2.12 | 2025 poz. 1669, art. 3 – Prawo o notariacie (lista notariuszy) | rejestr notariuszy w KRN | nie |
| 3.12 | 2026 poz. 1517 – ustawa o działaniach antyterrorystycznych (nowy rozdz. 5b „Wydarzenie specjalne”) | MSWiA rozporządzeniem nadaje status wydarzenia specjalnego wydarzeniom organizowanych przez Prezydenta, Marszałków, Radę Ministrów lub ministra; **Policja może przetwarzać dane uczestników „także bez wiedzy i zgody tych osób”** (art. 26l ust. 1), do 90 dni po wydarzeniu (ust. 7); sprawdzenie uczestników przez Policję, a w zakresie terroryzmu przez ABW (art. 26m); organizator ma uprzedzić o sprawdzeniu (art. 26n) | TAK – władza nad zwykłym człowiekiem, policja |
| 3.12 | 2026 poz. 1518 – Prawo farmaceutyczne (reklama aptek) | nowa definicja reklamy apteki; zakazy: korzyści za zakup, reklama porównawcza, kierowanie do dzieci, wizerunek/głos osób znanych i osób z wykształceniem medycznym – **także wygenerowany cyfrowo** (art. 94a ust. 1d); kara do 1 000 000 zł, osobno za każdą aptekę; **wszczęte i niezakończone postępowania w sprawie reklamy aptek umarza się, a decyzja o umorzeniu nie wymaga uzasadnienia** (art. 2 ust. 1) | TAK – konsumenci (bez porad medycznych) |
| 3.12 | 2026 poz. 1440 – Kodeks spółek handlowych | sprawy spółek | nie |
| 6.12 | 2026 poz. 734, art. 2 pkt 1 – ustawa o systemie ubezpieczeń społecznych | ubezpieczony może zgłosić ZUS zmianę adresu i danych kontaktowych przez profil informacyjny (art. 36 ust. 13a) | słabo |
| 10.12 | 2026 poz. 1556 – ustawa o asystencji osobistej osób z niepełnosprawnościami | 18–65 lat i co najmniej 80 pkt poziomu potrzeby wsparcia (art. 3 ust. 3 pkt 1); 20–240 h/mies. (13–18 lat: 20–80 h, art. 21); stawki 49/51/53/55 zł brutto/h (art. 22 ust. 5); **ale wnioski wg harmonogramu (art. 120):** ≥ 90 pkt – wniosek od 1.12.2027, asystencja od 1.04.2028; ≥ 85 pkt – od 1.05.2028 / 1.09.2028; ≥ 80 pkt – od 1.09.2028 / 1.01.2029; 13–18 lat – od 1.05.2029 / 1.01.2030 (daty z „pierwszy dzień miesiąca po upływie 12/16/17/21 mies. od ogłoszenia 25.11.2026” – policzone w kodzie); limit godzin 200 w 2028 i 220 w 2029 (art. 121); po 65. r.ż. tylko do końca decyzji wydanej wcześniej (art. 3 ust. 4); ustawa każe ministrowi do 31.12.2030 zbadać „zasadność” kontynuacji po 65. r.ż. (art. 125) | TAK – rodziny, opiekunowie; od wejścia w życie do pierwszej asystencji (1.04.2028) mija 478 dni (kod) |
| 10.12 | 2026 poz. 1553–1555 – rozp. MS, egzaminy notarialne, radcowskie, adwokackie | procedury egzaminów | nie |
| 11.12 | 2026 poz. 755, art. 21 (część) – ustawa o Krajowym Rejestrze Oznakowanych Psów i Kotów | zmiany w innej ustawie (zakres art. 21 – BRAK analizy) | do sprawdzenia; cały rejestr od 11.06.2028 |
| 12.12 | 2026 poz. 1200 – rozp. MRPiPS, wypłaty z Funduszu Gwarantowanych Świadczeń Pracowniczych | wykazy i wnioski FGŚP | słabo – pracownicy niewypłacalnych firm (do sprawdzenia, co dokładnie) |

Wcześniej, ale świeże („od tygodnia obowiązuje”): Dz.U. 2026 poz. 1466 – przejazdy kolejowe, od 21.11 – **już wykorzystane** (rolki 23.11 i 24.11), nie powtarzać.

### 3. Daty, które budzą emocje (29.11–13.12)

| Data | Okazja | Kąt dla konta | Status |
|---|---|---|---|
| pon. 30.11 | Cyber Monday (po Black Friday 27.11) | prawa kupującego: najniższa cena z 30 dni przed obniżką (bank tematów S2) | „14 dni na zwrot tylko online” już było – nie powtarzać; S2 – sprawdzić art. 4 ust. 2 ustawy o informowaniu o cenach w ISAP |
| czw. 3.12 | Międzynarodowy Dzień Osób z Niepełnosprawnościami (ONZ) | zapowiedź asystencji osobistej (ustawa od 10.12) | data ONZ do potwierdzenia na un.org |
| pt. 4.12 | Barbórka | czy górnik ma ustawowo wolne? (prawdopodobnie układ zbiorowy, nie ustawa) – mit do sprawdzenia; bez polityki górniczej | do sprawdzenia (Kodeks pracy, Karta górnika – BRAK) |
| niedz. 6.12 | Mikołajki | bez wątku religijnego; prezenty i zwroty – temat zwrotu już wykorzystany | raczej pominąć |
| śr. 9.12 | Międzynarodowy Dzień Przeciwdziałania Korupcji (ONZ) | afery i pieniądze publiczne – raport NIK/CBA z `sledczy.py` | data do potwierdzenia na un.org |
| czw. 10.12 | Dzień Praw Człowieka (Powszechna Deklaracja Praw Człowieka, 10.12.1948 – 78. rocznica, kod) + wejście w życie ustawy o asystencji | środek „Tygodnia praw obywatela” | potwierdzić na un.org |
| niedz. 13.12 | 45. rocznica wprowadzenia stanu wojennego (13.12.1981, kod) | prawa obywatela wtedy i dziś: godzina milicyjna, legitymowanie, internowanie bez wyroku vs dzisiejsze art. 41 Konstytucji – fakty z IPN/ISAP | **decyzja Michała** – historia polityczna; tylko TikTok (niedziela), bez ocen partii |
| 7–13.12 | „Tydzień praw obywatela” (strategia, sekcja 7) | 7 praw wobec policji i urzędu | patrz kampania 2 |
| grudzień | sezon kontroli drogowych przed świętami | alkomaty, „trzeźwy poranek” | BRAK komunikatu KGP z datami akcji – sprawdzić policja.pl przed rolką |

### 4. Plan slotów 29.11–13.12 (rezerwa, gdy news nie przejdzie weryfikacji)

Zasady: policja pon./śr./pt. 18:00, „Twoje prawa” poza policją sob. 18:00, karuzela TikTok 13:00 = kontrowersja z przeglądu TV/radio (inny temat niż rolki dnia), IG pon.–sob., w niedzielę tylko TikTok. Filar „szkoła kłamała” min. 3× w tygodniu i nie więcej niż 2 rolki z rzędu o urzędach i przepisach – zm-planista dobiera 9:00 tak, by to spełnić.

| Dzień | 9:00 | 13:00 (TikTok) | 18:00 |
|---|---|---|---|
| niedz. 29.11 | (TikTok) mit z lekcji | przegląd TV/radio | (TikTok) – |
| pon. 30.11 | **Od dziś obowiązuje #1:** „Dzwonisz po karetkę. Mogą ją odwołać.” – 1431 | przegląd TV/radio | Policja – z `sledczy.py`; rezerwa: zapowiedź Tygodnia (zatrzymanie – 48 h) |
| wt. 1.12 | mit z lekcji (filar „szkoła kłamała”) | przegląd TV/radio | mit / wiedza ogólna |
| śr. 2.12 | mit z lekcji | przegląd TV/radio | **Policja + Od dziś obowiązuje #2:** „Statysta w okazaniu? Od dziś 20 zł.” / „Listy z sądu: 50 zł od każdego oskarżonego” – 1508 |
| czw. 3.12 | **Od dziś obowiązuje #3:** „Apteka bez celebryty. Kara: 1 mln zł.” (+ umorzone sprawy bez uzasadnienia) – 1518 | przegląd TV/radio | mit z lekcji |
| pt. 4.12 | Barbórka – mit (jeśli się potwierdzi) albo wiedza ogólna | przegląd TV/radio | **Policja + Od dziś obowiązuje #4:** „Idziesz na wydarzenie rządu? Policja sprawdzi cię bez zgody.” – 1517 |
| sob. 5.12 | wiedza ogólna / rekord | przegląd TV/radio | Twoje prawa: prawa kupującego po Black Friday (S2, najniższa cena z 30 dni) |
| niedz. 6.12 | (TikTok) mit | przegląd TV/radio | – |
| pon. 7.12 | Tydzień praw #1 (urząd) | przegląd TV/radio | **Tydzień praw #2 – Policja** |
| wt. 8.12 | mit z lekcji | przegląd TV/radio | Tydzień praw #3 (urząd / informacja publiczna) |
| śr. 9.12 | Dzień walki z korupcją – raport NIK/CBA (sledczy) | przegląd TV/radio | **Tydzień praw #4 – Policja** |
| czw. 10.12 | **Od dziś obowiązuje #5 + Dzień Praw Człowieka:** „Ustawa od dziś. Asystent – w 2028.” – 1556 | przegląd TV/radio | mit z lekcji |
| pt. 11.12 | mit z lekcji | przegląd TV/radio | **Tydzień praw #5 – Policja** |
| sob. 12.12 | wiedza ogólna | przegląd TV/radio | **Tydzień praw #6 – Twoje prawa** (praca/sklep) |
| niedz. 13.12 | (TikTok) Tydzień praw #7 – stan wojenny 45 lat temu: prawa wtedy i dziś (jeśli Michał zgodzi się) | przegląd TV/radio | – |

### 5. Kampania 1 – seria „Od dziś obowiązuje” (30.11–10.12)

- **Hasło:** „Od dziś obowiązuje. Ty dowiadujesz się ostatni.”
- **Format:** rolka-pętla 7 s (`petla7.py`) z etykietą „NEWS” albo „OD DZIŚ”; plansza `dokument` z dosłownym przepisem i numerem Dz.U.; w opisie IG: artykuł, ustawa, data wejścia w życie, stanowisko drugiej strony (uzasadnienie projektu z druku sejmowego), „To nie jest porada prawna”, pytanie o ocenę zasady.
- **Materiały (5 rolek + 1 karuzela + relacje):**
  1. 30.11 9:00 – dyspozytor medyczny może odwołać karetkę (1431) – „co robisz”: podaj adres, potwierdź odczytany adres, nie odwołuj zgłoszenia bez potrzeby. Dopisek medyczny wg CLAUDE.md.
  2. 2.12 18:00 – koszty w procesie karnym: statysta 12 → 20 zł, doręczenia 20 → 50 zł od każdego oskarżonego (1508 + Dz.U. 2013 poz. 663 jako dowód starych stawek). Kto ponosi koszty – sprawdzić art. 627 i 632 k.p.k. w ISAP przed rolką.
  3. 3.12 9:00 – reklama aptek: zakaz celebrytów, lekarzy i głosów AI, kara do 1 mln zł; sprawy w toku umorzone bez uzasadnienia (1518). Bez porad medycznych, bez koszyka z suplementem pod tą rolką.
  4. 4.12 18:00 – wydarzenie specjalne: dane uczestników bez wiedzy i zgody, 90 dni, sprawdzenie przez ABW (1517). Ta sama miara wobec każdej władzy – mówimy o przepisie, nie o partii; druga strona: uzasadnienie projektu (bezpieczeństwo wydarzeń państwowych).
  5. 10.12 9:00 – asystencja osobista: ustawa od 10.12, pierwsza asystencja najwcześniej 1.04.2028 (478 dni), wniosek do 65. r.ż., stawka 49–55 zł/h (1556). Pytanie: „Słusznie, że po 65. urodzinach wniosku nie złożysz?”
  6. Karuzela TikTok (np. sob. 5.12 lub niedz. 6.12 13:00, jeśli przegląd TV/radio nic nie da): „5 przepisów, które weszły w tym tygodniu” – 4 slajdy.
  7. Relacje: ankieta „Wiedziałeś?” do każdej rolki serii.
- **Dokument pierwotny przed każdą rolką:** PDF aktu z API Sejmu (adres w tabeli) + druk sejmowy z uzasadnieniem (ustawy 1517, 1518, 1556) + 2. niezależne źródło (np. RPO, Rzeczpospolita, Prawo.pl, gov.pl).

### 6. Kampania 2 – „Tydzień praw obywatela” (7–13.12)

- **Hasło:** „Znasz swoje prawa? Policja zna swoje.” (ze strategii, sekcja 7)
- **Oś:** 10.12 Dzień Praw Człowieka. 7 praw wobec policji i urzędu, każde z artykułem i „co robisz”. Bez powtórek z `docs/opublikowane.md` (już były: norma legitymowań, kontrola osobista, milczenie, odmowa mandatu, policjant w cywilu, policjant się przedstawia).
- **Proponowane prawa (wszystkie do sprawdzenia w ISAP przed rolką – tu tylko wskazanie, gdzie szukać):**
  1. pon. 7.12 9:00 – urząd ma miesiąc na sprawę i co zrobić, gdy milczy (ponaglenie) – k.p.a. art. 35 i 37.
  2. pon. 7.12 18:00, policja – zatrzymany: ile najdłużej bez decyzji sądu – Konstytucja art. 41 ust. 3, k.p.k. art. 248.
  3. wt. 8.12 18:00 – informacja publiczna: urząd ma 14 dni na odpowiedź – ustawa o dostępie do informacji publicznej art. 13.
  4. śr. 9.12 18:00, policja – prawo do adwokata i zażalenie na zatrzymanie – k.p.k. art. 244–246.
  5. pt. 11.12 18:00, policja – czy wolno nagrywać interwencję – stanowisko RPO + orzecznictwo (dokument pierwotny: wystąpienie RPO / wyrok).
  6. sob. 12.12 18:00, Twoje prawa – praca w grudniu: niedziela handlowa/nadgodziny (bez powtarzania „3 niedziel handlowych” z 28.11 – inny kąt, np. dodatek za nadgodziny, k.p. art. 151¹).
  7. niedz. 13.12 TikTok – 45 lat od stanu wojennego: godzina milicyjna i internowanie vs dzisiejsze gwarancje (IPN + Konstytucja) – **tylko za zgodą Michała**.
- Każda rolka kończy się „co robisz” (skarga, zażalenie, RPO) i pytaniem o ocenę zasady. Relacja codziennie: „Prawo dnia” (wklejka `_relacja.jpg`).

### 7. Wykluczone (zasady CLAUDE.md)

- Dz.U. 2026 poz. 1550 (strefa przy granicy z Białorusią) – styk z migracją.
- Mikołajki w wątku religijnym; 1.12 Światowy Dzień AIDS – spór medyczny/zdrowie, pominięty.
- Przejazdy kolejowe (poz. 1466), zimówki, 14 dni na zwrot online – już opublikowane.
