# Biznes przyszłości – badanie rynku i rekomendacja (4.11.2026)

> Liczby w tabelach finansowych liczy `model.py` w tym folderze (`python3 docs/biznes-przyszlosci/model.py`). Oceny 1–5 w rankingu to moja ocena ekspercka oparta na źródłach z sekcji 11, nie dane z rynku. Rok 2035 to scenariusz, nie fakty. To nie jest porada inwestycyjna.

## 0. Wniosek w 5 zdaniach

1. **Zwycięzca: „Komplet”** – AI dla biur rachunkowych, które co miesiąc samo zbiera od klientów biura brakujące dokumenty (paragony, faktury spoza KSeF, wyjaśnienia płatności z wyciągu), czyta je i oddaje księgowej kompletną paczkę do programu księgowego.
2. Powód: KSeF uporządkował faktury, ale biura pracują teraz w dwóch obiegach naraz (KSeF i e-mail). W ankiecie SKwP i Symfonii z lipca 2026 to największe wyzwanie, a ok. 66% biur zgłasza wyraźny wzrost pracochłonności przy wzroście przychodów tylko w ok. 40%.
3. Rynek: ok. 70 tys. biur rachunkowych (szacunek KIBR). 100 tys. zł MRR to ok. 240 biur przy średnio 420 zł/mies., czyli ok. 0,3% rynku.
4. **Szczerze: 100 tys. zł MRR w 6 miesięcy z 20 tys. zł jest mało prawdopodobne.** W scenariuszu realistycznym model daje 100 tys. MRR w ok. 15. miesiącu sprzedaży, czyli ok. 17 miesięcy od dziś. W pesymistycznym nie dochodzi do tego w 24 miesiące i potrzebuje finansowania.
5. Pierwszy krok to nie kod, tylko **7 dni walidacji**: 25 rozmów z biurami i przedsprzedaż. Kryterium „idziemy dalej”: min. 3 biura płacą zaliczkę.

---

## 1. Scenariusz 2035 → co z tego wynika dziś

Teza (scenariusz) → co dziś to potwierdza:

| Teza na 2035 | Dzisiejsze dane | Wniosek na dziś |
|---|---|---|
| Faktury, VAT i księgi działają w czasie rzeczywistym w całej UE | Polska: KSeF obowiązkowy od 1.02.2026 (duzi) i 1.04.2026 (pozostali), mikrofirmy od 2027; UE: ViDA przyjęta 11.03.2025, transgraniczne e-faktury B2B od 1.07.2030, krajowe systemy do ujednolicenia do 2035; Belgia od 1.01.2026, Francja od 1.09.2026 | Dane fakturowe są już cyfrowe. Wąskim gardłem zostaje **wszystko, czego KSeF nie obejmuje**, i człowiek po stronie klienta |
| Księgowa staje się „kontrolerem i doradcą”, a mechaniczną pracę robi AI | Eurostat 2025: AI używa tylko 8,4% polskich firm (10+ osób) wobec 20% w UE | Duża luka adopcji AI w Polsce = okazja dla prostych, gotowych narzędzi |
| Komunikacja urząd–firma jest w 100% elektroniczna | e-Doręczenia obowiązkowe dla firm z CEIDG od 1.10.2026 | Mikrofirmy toną w powiadomieniach i terminach – ich biuro jest naturalnym „centrum dowodzenia” |
| Brak ludzi do pracy biurowej | Barometr fillup k24 2026: ok. 66% biur ma wyraźnie więcej pracy, tylko ok. 40% wyższe przychody; od lat brak specjalistów | Biuro zapłaci za narzędzie, które pozwala obsłużyć więcej klientów tym samym zespołem |
| Wygrywają aplikacje „pionowe” z workflow i integracjami, a nie ogólne czaty | Funduszowe rundy w Polsce: autoMEE/flowMEE (10 mln zł + 2,6 mln USD seed, księgowanie AI), Minerva (3 mln USD) i Mimira (4 mln zł) – przetargi | Inwestorzy płacą za pionowe AI z danymi i procesem; ogólny „czat z PDF-em” to nie biznes |

## 2. Dwadzieścia pomysłów i ocena

Kryteria (1–5, 5 = korzystnie dla nas; dla konkurencji, kosztu startu i pozyskania klientów 5 = łatwo) i wagi: rynek 1,0 · realny problem 1,5 · gotowość do płacenia 1,5 · konkurencja 1,0 · koszt startu 0,8 · automatyzacja AI 1,0 · subskrypcja 1,2 · eksport 0,6 · marża 1,0 · pozyskanie klientów 1,4. Wynik to % maksymalnej sumy.

| # | Pomysł | Ry | Pr | Pł | Ko | Ks | AI | Su | Ek | Ma | Po | Wynik |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Komplet – AI kompletuje dokumenty klientów biur rachunkowych** | 4 | 5 | 4 | 3 | 4 | 5 | 5 | 3 | 5 | 4 | **85,6** |
| 2 | AI asystent przetargowy (SWZ → oferta) dla MŚP | 4 | 5 | 5 | 2 | 3 | 4 | 4 | 3 | 4 | 3 | 76,7 |
| 3 | Pisma obywatelskie z AI (sprzeciw od nakazu, reklamacja, skarga) B2C | 3 | 4 | 3 | 3 | 5 | 5 | 1 | 2 | 5 | 5 | 72,5 |
| 4 | Skryba medyczny AI dla prywatnych gabinetów | 4 | 5 | 4 | 2 | 2 | 4 | 5 | 3 | 4 | 2 | 72,2 |
| 5 | Miękka windykacja z danych KSeF dla MŚP | 4 | 4 | 3 | 3 | 4 | 4 | 4 | 3 | 4 | 3 | 71,8 |
| 6 | Wyceny i oferty AI dla instalatorów i ekip remontowych | 3 | 4 | 3 | 3 | 4 | 4 | 4 | 3 | 4 | 3 | 70,0 |
| 7 | Głosowa recepcjonistka AI dla gabinetów i warsztatów | 4 | 4 | 3 | 2 | 4 | 4 | 5 | 3 | 3 | 2 | 67,8 |
| 8 | Tutor AI według kryteriów CKE (egzamin ósmoklasisty, matura) | 4 | 4 | 3 | 1 | 4 | 5 | 3 | 2 | 4 | 3 | 66,7 |
| 9 | Compliance NIS2 / KSC dla średnich firm | 3 | 4 | 4 | 2 | 3 | 3 | 4 | 4 | 4 | 2 | 66,2 |
| 10 | Fabryka krótkich wideo dla lokalnych firm | 3 | 3 | 3 | 1 | 5 | 4 | 4 | 3 | 3 | 4 | 65,8 |
| 11 | Compliance najmu krótkoterminowego (rozp. UE 2024/1028) | 2 | 3 | 3 | 3 | 4 | 3 | 4 | 4 | 4 | 3 | 64,7 |
| 12 | Agent AI obniżający rachunki domowe (prąd, telefon, polisy) | 3 | 3 | 3 | 3 | 4 | 3 | 3 | 4 | 4 | 3 | 64,4 |
| 13 | AI do wniosków o dotacje (FENG, programy regionalne) | 3 | 4 | 4 | 2 | 4 | 4 | 1 | 2 | 4 | 3 | 63,3 |
| 14 | Oprogramowanie AI dla wspólnot mieszkaniowych | 3 | 3 | 3 | 3 | 3 | 3 | 5 | 1 | 4 | 2 | 61,5 |
| 15 | AI skrzynka urzędowa dla JDG (e-Doręczenia, ZUS, US) | 3 | 3 | 2 | 3 | 4 | 4 | 4 | 2 | 4 | 2 | 60,9 |
| 16 | Audyt dostępności e-sklepów (Polski Akt o Dostępności) | 2 | 3 | 2 | 3 | 4 | 3 | 3 | 4 | 4 | 3 | 59,8 |
| 17 | Kadry i HR dla mikrofirm z AI | 3 | 3 | 3 | 2 | 3 | 3 | 4 | 1 | 4 | 2 | 57,5 |
| 18 | Compliance AI Act / RODO dla MŚP | 2 | 2 | 2 | 3 | 4 | 3 | 4 | 4 | 4 | 2 | 56,7 |
| 19 | Fakturowanie KSeF dla mikrofirm (2027) | 4 | 3 | 2 | 1 | 4 | 2 | 5 | 1 | 3 | 1 | 52,2 |
| 20 | Marketplace podwykonawców budowlanych z wyceną AI | 4 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | 1 | 47,5 |

## 3. Dlaczego odrzuciłem pozostałe (skrót)

- **Fakturowanie KSeF (19):** rynek jest ogromny, ale zajęty: inFakt, wFirma, iFirma i Fakturownia mają KSeF, marki i kanały. Do tego MF daje darmowe narzędzia. Nie ma tu przewagi.
- **Marketplace budowlany (20):** problem kury i jajka po obu stronach, wysoki CAC, niska powtarzalność.
- **Tutor CKE (8):** rodzice płacą (rynek korepetycji szacowany na 4–7,5 mld zł rocznie), ale uczniowie mają darmowe czaty, a sezonowość podbija churn. Konkurencja: wszystkie modele ogólne.
- **Recepcjonistka głosowa (7):** w Polsce jest już co najmniej 10 dostawców, ceny od 159 zł do ponad 1 900 zł netto/mies. To wojna cenowa z platformami (ElevenLabs, Zoom).
- **Skryba medyczny (4):** dobry problem i wysokie płatności, ale dane o zdrowiu (art. 9 RODO), długa sprzedaż do gabinetów i duże ryzyko odpowiedzialności. Za drogi start jak na 20 tys. zł.
- **Compliance (9, 11, 16, 18):** płaci się za to raz, a nie co miesiąc. Mikrofirmy są w dużej części zwolnione z Aktu o Dostępności; polska ustawa o najmie krótkoterminowym jest jeszcze w toku prac.
- **Dotacje (13), skrzynka JDG (15), kadry (17), rachunki domowe (12):** jednorazowe albo niska gotowość do płacenia; skrzynkę JDG lepiej sprzedać jako funkcję zwycięzcy (biuro widzi pisma klienta).
- **Fabryka wideo (10):** Michał zna ten proces, ale to raczej usługa agencyjna niż produkt, a konkurencją są Canva i CapCut. Bez przewagi.
- **Windykacja (5), wyceny dla instalatorów (6):** sensowne, ale wąsko (5) albo z rozproszonym kanałem dotarcia (6). Windykację z KSeF warto dodać do Kompletu później.

## 4. Trzech finalistów

| | **1. Komplet (biura rachunkowe)** | 2. Asystent przetargowy | 3. Pisma obywatelskie B2C |
|---|---|---|---|
| Problem | Co miesiąc ściganie klientów o dokumenty i wyjaśnienia; dwa obiegi (KSeF + e-mail) | Analiza SWZ i komplet dokumentów to dni pracy; błąd formalny = odrzucona oferta | Pismo w 14 dni (sprzeciw od nakazu zapłaty), reklamacje, skargi; prawnik kosztuje setki zł |
| Klient płaci, bo… | odzyskuje godziny pracy księgowych przy braku ludzi; może wziąć więcej klientów | jedna wygrana to kontrakt warty dziesiątki tysięcy zł i więcej | sprawa jest pilna i stresująca |
| Rynek (PL) | ok. 70 tys. biur, które obsługują większość z ok. 2,9 mln aktywnych firm | ok. 153 tys. zamówień rocznie, wartość ok. 587 mld zł (UZP 2024); MŚP składają 87–88% ofert | miliony nakazów w e-sądzie (EPU – ponad 2 mln spraw rocznie wg jednego źródła, brak aktualnej oficjalnej liczby) |
| Konkurencja | Saldeo SMART (obieg dokumentów), Symfonia AI Dekret, flowMEE/autoMEE – głównie **księgowanie**, nie zbieranie od klienta | Minerva (3 mln USD, 115 klientów), Mimira (4 mln zł), Przetarg Pro, Przetargi.io – rynek już finansowany | rozproszona; ogólne czaty AI za darmo |
| Model | subskrypcja per biuro, rośnie z liczbą klientów biura | subskrypcja + success fee | płatność za pismo (39–99 zł) |
| Atut po naszej stronie | wąski, łatwy do znalezienia klient (grupy FB księgowych, SKwP, OSCBR); pętla poleceń przez klientów biur | duża gotowość do płacenia | **zasięg @szkola_klamala** (seria o policji i prawie) = tani ruch |
| Główne ryzyko | duzi gracze (Comarch, Symfonia, Saldeo) dodadzą to samo | konkurencja z kapitałem; trudne dokumenty (budowlanka); ryzyko błędu | niska powtarzalność (brak MRR), odpowiedzialność za treść pisma, „darmowy ChatGPT” |
| Werdykt | **zwycięzca** | dobry, ale wchodzimy jako 5. gracz bez kapitału | dobry jako dodatkowy biznes „z zasięgu”, zły jako silnik MRR |

## 5. Zwycięzca: „Komplet”

> Nazwa robocza. Przed użyciem sprawdzić znaki towarowe (UPRP, EUIPO) i domeny.

**Grupa docelowa:** biura rachunkowe z 2–15 pracownikami i 40–300 klientami (JDG i małe spółki). Kupuje właściciel biura.

**Problem:** KSeF dostarcza tylko faktury ustrukturyzowane. Reszta – paragony, faktury zagraniczne (SaaS, Allegro, Amazon), umowy, wyciągi, wyjaśnienia „co to za przelew” – nadal przychodzi mailem, na WhatsAppie albo w reklamówce w ostatnim dniu. Księgowa dzwoni i pisze do każdego klienta, a terminy (np. 20. dnia miesiąca) są nieprzesuwalne.

**Propozycja wartości:** *„Twoi klienci sami oddają komplet. Ty zamykasz miesiąc 2 dni wcześniej.”*

**Jak działa (rdzeń):**
1. Biuro podłącza klienta: dostęp do KSeF (token lub certyfikat z uprawnieniem do odczytu), wyciąg bankowy (import MT940/CSV, później PSD2 przez licencjonowanego pośrednika).
2. Komplet porównuje płatności z wyciągu z fakturami z KSeF i dokumentami w teczce. Każda płatność bez dokumentu trafia na listę braków.
3. Agent pisze do klienta (e-mail/SMS, później WhatsApp) konkretnie: „12.10 zapłaciłeś 230,00 zł na stacji paliw – wrzuć zdjęcie paragonu albo napisz, że to wydatek prywatny”. Link otwiera stronę wgrywania bez logowania i hasła.
4. AI czyta dokument (data, NIP, kwoty, VAT, waluta), dopasowuje go do płatności i oznacza pewność. Niepewne pozycje sprawdza człowiek.
5. Księgowa widzi tablicę „kto ma komplet / komu czego brakuje” i eksportuje paczkę do swojego programu (Optima, Symfonia, Rewizor, enova, wFirma – zaczynamy od 2 najpopularniejszych wśród klientów z walidacji).

**Przewaga nad konkurencją:**
- Nie konkurujemy z programem księgowym biura – działamy **obok każdego** z nich. Saldeo, Symfonia czy flowMEE chcą być systemem biura. My jesteśmy warstwą „klient → biuro”.
- Zaczynamy od **braków**, a nie od OCR: punkt wyjścia to wyciąg i KSeF („czego brakuje?”), a nie skrzynka, do której klient musi coś sam wysłać.
- Pętla wzrostu: każde biuro zaprasza dziesiątki swoich klientów. Klient widzi markę Komplet, a mikrofirmy bez biura mogą zaprosić swoje biuro.
- Mało pracy przy wdrożeniu: biuro zaczyna od 5 klientów w 15 minut.

**Uczciwa krytyka:**
- Najsłabszy punkt: Saldeo SMART ma już aplikację dla klienta biura, a Comarch/Symfonia mogą dodać agenta przypomnień w kwartał. Nasza obrona to tempo, skupienie na jednym problemie i niezależność od programu księgowego, a nie technologia.
- Dostęp do KSeF dla wielu NIP-ów (tokeny działają do końca 2026, potem certyfikaty) trzeba sprawdzić w oficjalnej dokumentacji API KSeF 2.0. Źródła branżowe są tu sprzeczne.
- Biura są konserwatywne. Sprzedaż wymaga zaufania, demo i bezpieczeństwa danych (umowa powierzenia przetwarzania, serwery w UE).
- Zasięg @szkola_klamala prawie nie pomaga w B2B. Pomaga za to umiejętność robienia treści, które docierają do ludzi.

### Cennik (netto, bez VAT; B2B odlicza VAT)

| Plan | Cena/mies. | Dla kogo |
|---|---|---|
| Próba | 0 zł przez 30 dni, do 5 klientów | test bez karty |
| Biuro | 249 zł | do 40 klientów |
| Pro | 549 zł | do 120 klientów, eksport do 2 programów, SMS w cenie |
| Sieć | 1 190 zł | do 300 klientów, wielu księgowych, priorytetowe wsparcie |
| Dodatki | 3 zł / klient ponad limit; WhatsApp; „Skrzynka pism klienta” (e-Doręczenia); windykacja z KSeF | |

Pierwsze 20 biur: cena „założycielska” –40% dożywotnio w zamian za cotygodniowy feedback.

### Koszt obsługi i marża (model, realistycznie)

Na biuro miesięcznie: AI ok. 48 zł (ok. 2 400 dokumentów × ok. 0,02 zł tanim modelem przy cenach rzędu 1 USD / 5 USD za 1 mln tokenów), wiadomości 15 zł, płatność ok. 1,5% + 1 zł, wsparcie 20 zł → **ok. 90 zł przy ARPA 420 zł = marża brutto ok. 78%.** Sprzedaż przez WWW, bez sklepów z aplikacjami (brak prowizji 15–30%).

## 6. Matematyka biznesu

### Ilu klientów na 100 000 zł MRR (zaokrąglenie w górę)

| Cena/mies. | Klienci | Przychód |
|---|---|---|
| 49 zł | 2 041 | 100 009 zł |
| 99 zł | 1 011 | 100 089 zł |
| 199 zł | 503 | 100 097 zł |
| 249 zł | 402 | 100 098 zł |
| 420 zł (średnia ARPA Komplet) | 239 | 100 380 zł |
| 549 zł | 183 | 100 467 zł |
| 1 190 zł | 85 | 101 150 zł |

### Trzy scenariusze (m1 = pierwszy miesiąc sprzedaży, ok. 2–3 miesiące od dziś)

Założenia: nowe biura rosną co miesiąc o 10/12/14%; koszty stałe 1,5 tys. zł do m6, potem + osoba do wsparcia (9 tys. zł), od m13 + programista (razem ok. 30 tys. zł). Start z 20 tys. zł gotówki. Właściciel nie bierze pensji do m6.

| | Pesymistyczny | Realistyczny | Optymistyczny |
|---|---|---|---|
| ARPA | 330 zł | 420 zł | 520 zł |
| Churn miesięczny | 3,5% | 2,2% | 1,5% |
| CAC | 1 600 zł | 1 000 zł | 700 zł |
| LTV (marża / churn) | 6 887 zł | 14 986 zł | 28 547 zł |
| LTV/CAC | 4,3 | 15,0 | 40,8 |
| Zwrot CAC | 6,6 mies. | 3,0 mies. | 1,6 mies. |
| Biura / MRR po m6 | 29 / 9 426 zł | 62 / 25 999 zł | 99 / 51 597 zł |
| Biura / MRR po m12 | 74 / 24 311 zł | 176 / 74 068 zł | 308 / 160 379 zł |
| Biura / MRR po m24 | 279 / 92 150 zł | 822 / 345 283 zł | 1 743 / 906 468 zł |
| 100 tys. zł MRR | nie w 24 mies. | **m15** | m10 |
| EBIT m12 / m24 (mies.) | –11 902 / –19 896 zł | 18 915 / 132 728 zł | 85 166 / 545 504 zł |
| Najniższy stan gotówki | **–400 487 zł** (potrzebny kapitał) | 4 892 zł (na styk) | 15 082 zł |
| Dochód właściciela m24* | 0 | ok. 97 800 zł/mies. | ok. 402 000 zł/mies. |

\* Przy wypłacie całego EBIT: sp. z o.o., CIT 9% (mały podatnik) + 19% podatku od dywidendy. Przychód ≠ zysk operacyjny ≠ dochód właściciela – w realistycznym m12 przy MRR 74 tys. zł zysk operacyjny to ok. 19 tys., a właścicielowi na rękę zostaje ok. 14 tys. zł.

**Jak czytać:** scenariusz realistyczny wymaga CAC ok. 1 000 zł, czyli głównie kanałów organicznych i poleceń, a nie reklam. Jeśli w walidacji koszt pozyskania wyjdzie bliżej 1 600 zł, a churn ok. 3,5%, firma bez inwestora się nie utrzyma – to sygnał, żeby zmienić kierunek.

## 7. Pozyskiwanie klientów (mały budżet)

- **Pierwsze 100 biur (m1–m6):** sprzedaż założyciela. Codziennie posty i pomoc w grupach FB dla księgowych, darmowy webinar „Zamknij miesiąc z KSeF i bez pogoni za paragonami”, 10 telefonów dziennie do biur z wyszukiwarek map, demo w 15 minut. Partnerstwa: regionalne oddziały SKwP, OSCBR, szkolenia KSeF.
- **Do 1 000 (m6–m18):** treści krótkie (Reels/TikTok/YouTube Shorts) dla księgowych w stylu fabryki rolek („3 sposoby, jak klient chowa paragon”); SEO pod frazy KSeF i biuro; program partnerski 20% przez 12 mies. dla doradców i trenerów KSeF; mikroinfluencerzy-księgowi; studia przypadków z liczbą odzyskanych godzin.
- **Do 10 000 (m18+):** pętla B2B2C (mikrofirma zaprasza swoje biuro – miesiąc gratis dla obu), integracje w marketplace'ach programów księgowych, Czechy i Słowacja oraz kraje z obowiązkowymi e-fakturami (Belgia, Francja, potem cała UE z ViDA 2030).
- **Program poleceń:** biuro poleca biuro → oba dostają miesiąc gratis.

## 8. Plan realizacji

| Etap | Czas | Co | Mierzalny wynik (bramka) |
|---|---|---|---|
| 1. Walidacja | 7 dni | 25 rozmów z właścicielami biur, strona z listą oczekujących, przedsprzedaż „założycielska” | min. 15/25 potwierdza problem jako top 3; **min. 3 zaliczki**; jeśli nie – zmiana kierunku (finalista 2 lub 3) |
| 2. Projekt i prototyp | 14 dni | sprawdzenie dokumentacji API KSeF 2.0, makiety, klikany prototyp, testy na 3 biurach | 3 biura przechodzą proces na danych 5 klientów |
| 3. MVP | 30 dni | zakres z sekcji 9 | 10 biur, 100 klientów biur, ≥60% braków zamkniętych przez agenta bez telefonu |
| 4. Start komercyjny | 60 dni | płatności, wdrożenie samoobsługowe, webinar, partnerzy | 40 płacących biur, MRR ≥ 12 tys. zł, churn < 3% |
| 5. Optymalizacja | 90 dni | 2. program księgowy, WhatsApp, wsparcie | 100 biur, MRR ≥ 40 tys. zł, CAC ≤ 1 000 zł |
| 6. Skala | 180 dni | zespół 3 osób, partnerzy, CZ/SK | 240+ biur = ok. 100 tys. zł MRR (realistycznie ok. m15) |

Kalendarz jest realny dla 1 osoby z Claude Code. Najdłużej trwają integracje (KSeF, eksporty) i budowanie zaufania biur, a nie samo programowanie.

## 9. Propozycja MVP (do zbudowania po bramce z etapu 1)

**W zakresie:**
1. Konto biura (logowanie + 2FA), lista klientów, terminy.
2. Teczka miesiąca dla klienta: płatności z wyciągu (import CSV/MT940), faktury zakupowe z KSeF (odczyt), dokumenty wgrane → lista braków.
3. Agent przypomnień (e-mail + SMS) z linkiem do wgrania bez logowania; harmonogram eskalacji (dzień 3, 7, 10).
4. Odczyt dokumentów AI + dopasowanie do płatności z progiem pewności; kolejka „do sprawdzenia”.
5. Eksport paczki do 1–2 programów (format wybrany po walidacji).
6. Subskrypcje (Stripe Billing, faktury VAT), panel administratora, analityka (aktywność biur, % zamkniętych braków).

**Poza MVP:** WhatsApp, PSD2, czat z klientem, windykacja, wiele języków.

**Technologia (tania i skalowalna):** Next.js + TypeScript; PostgreSQL z RLS i magazyn plików w regionie UE (np. Supabase Frankfurt); kolejka zadań; Claude Haiku do odczytu dokumentów, mocniejszy model tylko do trudnych przypadków; wysyłka e-mail i SMS przez dostawców z UE/PL; Stripe Billing. Bezpieczeństwo: szyfrowanie plików, dziennik zdarzeń, umowa powierzenia przetwarzania (RODO), dostawcy AI bez trenowania na danych. **Wymaga kont i kluczy od Ciebie:** Stripe, dostawca SMS, e-mail, hosting, API Anthropic, środowisko testowe KSeF. Do tego czasu integracje zostaną oznaczone jako nieukończone. Niczego płatnego nie uruchamiam bez Twojej zgody.

## 10. Rekomendacja: 20 000 zł, 1 komputer, AI, 6 miesięcy

**Zainwestowałbym w Komplet, ale z inną obietnicą niż „100 tys. w 6 miesięcy”.** Uczciwy cel na 6 miesięcy to **30–100 płacących biur i ok. 10–40 tys. zł MRR** (sprzedaż rusza ok. 2.–3. miesiąca) z dowodem, że CAC < 1 000 zł i churn < 3%. Taki wynik daje realną drogę do 100 tys. zł MRR w ok. 12–18 miesięcy bez inwestora, albo dobrą pozycję do rozmowy z funduszem (jak autoMEE czy Minerva). Szansa na 100 tys. MRR w 6 miesięcy to moim zdaniem około 1 do 10.

Podział 20 000 zł:

| Pozycja | Kwota |
|---|---|
| Programowanie | 0 zł (Ty + Claude Code) |
| Hosting, AI, SMS, domena, narzędzia – 6 mies. | 3 000 zł |
| Prawnik: regulamin, umowa powierzenia, polityka prywatności | 2 500 zł |
| Zgłoszenie znaku towarowego (UPRP) i identyfikacja | 1 500 zł |
| Testy reklam do właścicieli biur (FB/LinkedIn) – tylko po walidacji | 5 000 zł |
| Webinary, konferencje KSeF, dojazdy do biur | 3 000 zł |
| Rezerwa (opóźnienia integracji) | 5 000 zł |

Dlaczego to, a nie aplikacja konsumencka: biuro rachunkowe ma bolesny, comiesięczny problem z twardym terminem, płaci z firmowego budżetu, łatwo je znaleźć i rzadko zmienia narzędzia, które działają. To daje przewidywalny MRR z małym zespołem. Aplikacje B2C w Polsce wymagają milionów użytkowników albo dużego budżetu reklamowego.

**Następny krok, który mogę zrobić od razu:** skrypt 25 rozmów walidacyjnych, tekst strony z listą oczekujących i lista grup/partnerów do kontaktu. Po bramce z etapu 1 – szkielet MVP w osobnym repozytorium (nie w repo Szkoły kłamała).

## 11. Źródła (dostęp 4.11.2026)

- KSeF – harmonogram: [jpk.info.pl](https://jpk.info.pl/faktury/e-faktura-ustrukturyzowana-ksef/harmonogram/), [infor.pl](https://ksiegowosc.infor.pl/wiadomosci/7577102,ksef-w-2026-roku-obowiazkowy-jakie-obowiazki-ksef-i-dla-kogo-w-2027.html), druk sejmowy 2321 (odroczenie dla mikrofirm – status do sprawdzenia): [api.sejm.gov.pl](https://api.sejm.gov.pl/sejm/term10/prints/2321/2321.pdf); liczba firm w KSeF 9.02.2026 (73 063, MF/PAP): [xyz.pl](https://xyz.pl/?p=169510)
- Problemy z KSeF po 100 dniach (podwójny obieg): [infor.pl](https://ksiegowosc.infor.pl/wiadomosci/7620358,najwieksze-problemy-z-ksef-jak-je-rozwiazac-oceny-i-wnioski-ksiegowych-i-biur-rachunkowych-po-ponad-100-dniach-pracy-z-systemem.html); [rp.pl](https://pro.rp.pl/krajowy-system-e-faktur-ksef/art44770621-ksef-po-pieciu-miesiacach-system-dziala-firmy-z-klopotami); ankieta SKwP: [skwp.pl](https://skwp.pl//content/uploads/2025/10/Ankieta-Obawy-biur-rachunkowych-przed-wejsciem-KSeF-1.pdf)
- Biura rachunkowe – ok. 70 tys. (KIBR), obciążenie (fillup k24): [infor.pl](https://ksiegowosc.infor.pl/ksef/7554393,ksef-zmienia-rynek-pracy-w-polsce-rewolucja-dla-ksiegowych-i-hr.html), [podatki.biz](https://www.podatki.biz/artykuly/ksef-ai-i-automatyzacja-ksiegowosci-jak-zmienia-sie-praca-biur-rachunkowych-w-2026-roku_40_62261.htm); raport Symfonii o gotowości biur: [symfonia.pl](https://symfonia.pl/blog/firmy/biura-rachunkowe/czy-biura-rachunkowe-sa-gotowe-na-wdrozenie-ksef-raport-z-badan/); Symfonia AI Dekret: [symfonia.pl](https://symfonia.pl/blog/finanse-i-ksiegowosc/ksef-zmienil-import-faktur-czas-zmienic-takze-dekretacje/)
- Konkurencja: autoMEE/flowMEE: [xyz.pl](https://xyz.pl/?p=255867), [dealroom.co](https://dealroom.co/news/157853-automee-raises-2-6m-seed-to-bring-real-time-accounting-to-polands-smes/); SaldeoSMART: [pomoc.saldeosmart.pl](https://pomoc.saldeosmart.pl/hc/pl/articles/21383464614941); ceny usług księgowych: [cenauslug.pl](https://cenauslug.pl/poradniki/ile-kosztuje-prowadzenie-ksiegowosci-porownanie-biur-rachunkowych-i-programow-online)
- API KSeF 2.0 (tokeny, uprawnienia – źródła sprzeczne): [kluczesoft.pl](https://kluczesoft.pl/wiedza/logowanie/ksef-2-0-logowanie), [itwiz.pl](https://itwiz.pl/program-do-faktur-a-nadawanie-uprawnien-w-ksef-jak-to-dziala-w-praktyce/)
- ViDA i e-faktury w UE: [econnect.eu](https://econnect.eu/en/docs/knowledge/regulations/europe), [KPMG](https://kpmg.com/lu/en/blogs/home/posts/2025/12/hitting-send-time-preparing-mandatory-e-invoicing-requirements.html)
- GUS – aktywne firmy (2,875 mln, III kw. 2025): [superbiz.se.pl](https://superbiz.se.pl/wiadomosci/polska-przedsiebiorczosc-w-rozkwicie-blisko-3-miliony-aktywnych-firm-w-iii-kwartale-2025-roku-aa-rgps-HrhK-XtAN.html), [xyz.pl](https://xyz.pl/?p=145899)
- Eurostat – AI w firmach 2025 (PL 8,4%, UE 20%): [trade.gov.pl](https://www.trade.gov.pl/en/news/artificial-intelligence-in-the-european-union-leaders-and-outsiders), [SGH](https://transformwork.sgh.waw.pl/node/214)
- e-Doręczenia (CEIDG od 1.10.2026): [ifirma.pl](https://www.ifirma.pl/blog/e-doreczenia-dla-przedsiebiorcow), [infor.pl](https://ksiegowosc.infor.pl/obrot-gospodarczy/dzialalnosc-gospodarcza/6443301,kiedy-przedsiebiorca-musi-miec-adres-do-edoreczen-terminy.html)
- Zamówienia publiczne 2024 (ok. 587 mld zł, ok. 153 tys. zamówień): [xyz.pl / PAP](https://xyz.pl/?p=109455); konkurencja: [Minerva](https://xyz.pl/dzieje-sie/startup-minerva-pozyskal-3-mln-dolarow-rozwija-technologie-ulatwiajaca-start-w-przetargach-3050), [Mimira](https://itwiz.pl/mimira-z-4-mln-zl-na-cyfryzacje-przetargow-publicznych/), [Przetarg Pro](https://www.producthunt.com/p/przetargpro)
- Recepcjonistki głosowe AI w PL (ceny 159–1 900+ zł; źródło dostawcy): [ainora.lt](https://ainora.lt/pl/blog/asystent-ai-warsztat-samochodowy-porownanie-2026)
- Korepetycje (4–7,5 mld zł, szacunki różnej daty): [gazetaprawna.pl](https://www.gazetaprawna.pl/urzad/oswiata/artykuly/10901722,jak-wyglada-rynek-korepetycji-w-polsce-raport.html), [money.pl](https://www.money.pl/gospodarka/korepetycje-coraz-drozsze-godzina-matematyki-wyzszej-nawet-za-95-zl-6809766001453664a.html)
- Polski Akt o Dostępności: [gov.pl](https://www.gov.pl/web/dostepnosc-cyfrowa/polski-akt-o-dostepnosci--uslugi-handlu-elektronicznego), [PARP](https://redakcja.parp.gov.pl/storage/publications/pdf/PARP_mala_broszura_PAD_PARP_18_11.pdf)
- Najem krótkoterminowy (rozp. 2024/1028): [infor.pl](https://www.infor.pl/prawo/nowosci-prawne/7567596,wynajem-mieszkan-zmiany-przepisow-od-20-maja-2026-r-kary-do-50-tys-zl-za-brak-rejestracji-i-numeru-identyfikacyjnego-adwokat-idzie-rewolucja-a-wiekszosc-wlascicieli-nic-o-tym-nie-wie.html), [gov.pl](https://www.gov.pl/web/sport/regulacja-najmu-krotkoterminowego--projekt-uporzadkowania-rynku-uslug-noclegowych)
- EPU / e-sąd: [bankier.pl](https://www.bankier.pl/wiadomosc/E-nie-sprawiedliwosc-2776733.html), [bezprawnik.pl](https://bezprawnik.pl/e-sad-nakazy-zaplaty/)
- Booksy (ceny, Boost 45%): [meetergo.com](https://meetergo.com/pl/blog/booksy-cennik)
- Ceny API Claude (orientacyjnie; sprawdzić na stronie Anthropic): [finout.io](https://finout.io/blog/anthropic-api-pricing); Stripe PL (ok. 1,5% + 1 zł – sprawdzić u Stripe): [quasa.io](https://quasa.io/pl/media/stripe-czy-payu-stala-zlotowka-boli-najbardziej-przy-malym-koszyku)

**Do weryfikacji przed decyzją:** status odroczenia KSeF dla mikrofirm (druk 2321), oficjalna dokumentacja API KSeF 2.0 (dostęp biura do wielu NIP-ów), aktualna liczba biur (GUS, PKD 69.20), cenniki Saldeo i flowMEE (z rozmów lub demo).
