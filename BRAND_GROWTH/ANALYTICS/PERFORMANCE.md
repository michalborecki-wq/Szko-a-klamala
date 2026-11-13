# Wyniki (skrót; pełne dane: `docs/wyniki.md`, `docs/analiza-wynikow-2026-11-09.md`, `docs/analiza-wynikow-2026-11-11.md`)

Źródło: Instagram przez Composio (tylko odczyt). **Facebook (ponad 90% wyświetleń) nie jest widoczny w API** – potrzebny cotygodniowy zrzut „Statystyki rolki” od Michała. Próbki małe: sygnał, nie dowód.

## Stan 11.11 (ostatni pomiar)
| Rolka | Format | Wyśw. IG | Pominięcia 3 s | Śr. czas |
|---|---|---|---|---|
| ZUS daruje 315 mln zł. Jest haczyk. | NEWS | 109 | 66% | 3,8 s |
| Wielkiego Muru nie widać z Księżyca | MYTH + tło wideo | 5 | 67% | 7,7 s |
| „Pilny komunikat skarbówki” | NEWS | 9 | 78% | 2,9 s |
| 500 zł miesięcznie przez 30 lat | EXPLAINER | 36 | 91% | 3,4 s |
| +51 km/h na krajówce | NEWS | 38 | 97% | 1,2 s |
| Mandat? Możesz powiedzieć „nie” | MYTH | 6 | 100% | 1,2 s |
Udostępnienia i zapisy: 0 we wszystkich rolkach konta. Rekord łączny (IG+FB, zrzut): Policja #1 ok. 2 tys.; Francja i ISS po 1,1 tys.

## Co wiemy
1. Haczyk: podmiot znany każdemu + liczba/zaprzeczenie + otwarta pętla trzyma (≤ 75%); żargon, znak „+”, pytanie na początku – nie (≥ 90%).
2. Rekordy zasięgu zrobiły rolki z filaru „szkoła kłamała” (Francja, ISS) i pierwsza policyjna – nie rolki o urzędach.
3. Średni czas 1–4 s przy rolkach 26–39 s: większość widzów nie dochodzi do zwrotu akcji.

## Czego nie wiemy (luki pomiaru)
- Wyników z Facebooka per rolka, demografii, źródeł ruchu.
- Wyników TikToka (brak konektora) – do ręcznego zrzutu.
- Wpływu zmian z 11–13.11 (nowy wygląd, żółta okładka) – pierwszy pomiar 14.11.

## Następny pomiar
14.11 wieczorem: rolki 12.11 (×2) i 13.11 (×2) – ta sama tabela + kolumny Format, Okładka, Tło.

## Zrzut Facebooka (zgoda Michała 13.11)
Co niedzielę Michał przysyła zrzuty „Statystyki rolki” (IG → rolka → Statystyki) dla rolek z tygodnia. Tabela: rolka | wyśw. łącznie | z FB | śr. czas | pominięcia | udostępnienia.

## TikTok – pomiar (prośba Michała 13.11)
- **Composio → TikTok (logowanie konta): nie działa** – TikTok odrzuca aplikację pośrednika („Coś poszło nie tak… client_key”, 13.11 7:29). To błąd po stronie integracji, nie konta. Niedokończone połączenia usunięte. Ponowić próbę za kilka tygodni albo po założeniu własnej aplikacji w TikTok for Developers (wymaga weryfikacji – na razie nie).
- Publiczna strona profilu nie oddaje danych automatom; zabezpieczeń nie obchodzimy.
- **Droga obowiązująca (0 zł):** raz w tygodniu Michał pobiera w TikTok Studio na komputerze (tiktok.com/tiktokstudio → Analityka → „Pobierz dane”) plik z zakładki Treści i Przegląd (ostatnie 7 dni) i wysyła w rozmowie; agent wczytuje CSV/XLSX i dopisuje tabelę: film | wyświetlenia | polubienia | komentarze | udostępnienia | śr. czas | obejrzane do końca. Z telefonu: zrzuty „Analityka filmu” dla 3 najlepszych i 3 najgorszych.
- Opcja płatna (ok. 0,001 USD za zapytanie, publiczne liczniki bez czasu oglądania) – tylko za zgodą Michała.

### TikTok – pierwszy pomiar (zrzuty Michała, 13.11 7:32)
| Film | Publikacja | Wyśw. | Polub. | Kom. | Udost. | Zapisy | Śr. czas | Do końca | Śr. % filmu | Uwagi |
|---|---|---|---|---|---|---|---|---|---|---|
| „Pilny komunikat skarbówki” to nie kara. To telefon. (31,6 s) | 10.11 19:50 | 9 | 0 | 0 | 0 | 0 | 4,5 s | 0% | 14% | większość wychodzi po 0:02; krzywa: ok. 35% po 2 s, ok. 20% po 4 s, ok. 10% do 26 s; źródła ruchu niedostępne (< 100 wyśw.); wszystkie wyświetlenia 10.11, potem 0 |

Wnioski robocze (1 film – sygnał, nie dowód):
1. **9 wyświetleń w 3 dni to problem dystrybucji, nie haczyka.** TikTok zwykle pokazuje nowy film przynajmniej kilkudziesięciu–kilkuset osobom; tu po pierwszej godzinie ruch ustał. Przy 9 widzach nie da się oceniać treści.
2. Kształt krzywej jest taki sam jak na IG (ucieczka w 2 s) – pierwsza klatka nadal rozstrzyga.
3. Do sprawdzenia przez Michała: (a) lista filmów w Analityce → Treści – czy wszystkie mają jednocyfrowe wyświetlenia, czy tylko ten; (b) Ustawienia → Pomoc/Wsparcie → „Stan konta” (ograniczenia, naruszenia); (c) czy filmy są wstawiane z aplikacji TikTok (nie z przeglądarki) i z dodanym dźwiękiem z biblioteki; (d) czy przy publikacji nie włącza się „tylko znajomi”/ograniczeń wieku.
