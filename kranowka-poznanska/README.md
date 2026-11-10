# Kranówka Poznańska – system marki „Odcisk”

Koncepcja odświeżenia identyfikacji kampanii „Kranówka Poznańska” (10.11.2026). Projekt osobny od „Szkoła kłamała” – nie korzysta z jej silnika ani zasad.

## Pomysł

Wzór marki robi sama woda: szklanka nalana z kranu i postawiona na papierze zostawia mokre kółko. Kółko jest literą Ó w słowie KRANÓWKA, kropla – jej kreską. Wzór pomocniczy to kaustyki, czyli siatka światła, którą woda rzuca na stół.

Punkt wyjścia: film referencyjny Super Studio dla piekarni Rose (wzór z odbitki kromki chleba). Przejęta została zasada – „wzór powstaje z produktu, a film zaczyna się od procesu” – nie elementy graficzne.

## System

| Element | Decyzja |
|---|---|
| Kolory | Atrament `#0B1B3F`, Papier `#F5F3EE`, Woda `#2EA8FF` (jedyny akcent), pomocniczo Mgła `#DDE7EF`. Bez gradientów. |
| Kroje | Fraunces Black (opsz 144, SOFT 100) – logo i hasła; Fraunces Italic – puenty; Instrument Sans – informacja. Oba na licencji OFL. |
| Logo | `assets/img/logo-*.svg` (podstawowe, nocne, mono), sygnet `znak-*.svg`. |
| Wzór | `assets/img/kaustyka-*.png` – kafle bez szwów: ekranowe (a, b) i drukowe, jednokolorowe (druk). |
| Ruch | Sześć ruchów w `assets/js/kp.js`: zalanie, krąg, dryf, wynurzenie, złożenie logo, kręgi. |
| Partnerzy | Herb Poznania i znak Aquanet zawsze w oryginalnych kolorach, na polu papieru. |

## Pliki

- `index.html` – prezentacja marki (GSAP + ScrollTrigger, responsywna, respektuje „ogranicz ruch”).
- `rolki/rolka.html?r=1|2|3` – trzy rolki 9:16 (podgląd na żywo); `rolki/render.js` – eksport do MP4.
- `makiety/makieta.html?m=…` – plakat, billboard, posty, podkładka, naklejka, butelka; `makiety/render.js` – eksport do PNG.
- `gotowe/` – wyrenderowane pliki: rolki MP4 (1080×1920, 30 kl./s, z muzyką), okładki, makiety PNG, zrzuty prezentacji.
- `narzedzia/build_assets.py` – generator logo i wzoru.

## Uruchamianie

```bash
python3 -m http.server 8000          # w folderze kranowka-poznanska, potem http://localhost:8000
pip install fonttools brotli numpy scipy pillow
python3 narzedzia/build_assets.py    # logo + wzór
node rolki/render.js                 # wszystkie rolki (albo: node rolki/render.js 2) – obraz z cichą ścieżką
python3 narzedzia/muzyka.py          # dokłada muzykę i efekty do gotowych rolek
node makiety/render.js               # makiety + zrzuty prezentacji
```

Render wymaga Playwright (Chromium) i ffmpeg.

## Hasła

1. Lej, tej.
2. Najkrótsza dostawa w mieście: z kranu do szklanki.
3. Poznaniak umie liczyć. Dlatego pije z kranu.
4. Woda z dostawą do domu. Od zawsze.
5. Nie dźwigaj. Odkręć.
6. Lokalna. Bardziej się nie da.
7. Bez kaucji. Bez zakrętki. Bez noszenia.
8. Źródło masz w kuchni.
9. Dobra woda nie potrzebuje etykiety.
10. Poznań leje wodę. I dobrze.

## Źródła i prawa

- Herb Poznania: plik wektorowy z nagłówka poznan.pl (10.11.2026). Znak Aquanet: z nagłówka aquanet.pl. Oba należą do właścicieli i są użyte poglądowo – **publikacja materiałów z tymi znakami wymaga zgody Miasta Poznania i Aquanet SA**.
- Kampania „Kranówka Poznańska” jest prowadzona przez Aquanet (kranowkapoznanska.pl); ten projekt to propozycja, nie oficjalny materiał.
- Kroje: Fraunces i Instrument Sans (SIL Open Font License), GSAP (licencja standardowa, bezpłatna).
- Muzyka i efekty dźwiękowe rolek są w całości generowane w kodzie (`narzedzia/muzyka.py`), bez cudzych nagrań; głośność −14 LUFS.
- Liczby (ceny, wyniki badań wody) trafiają do materiałów dopiero po potwierdzeniu u dostawcy. Jedyna liczba w rolkach to arytmetyka: 6 × 1,5 l = 9 l, czyli ok. 9 kg wody.

## Do zrobienia

- Znak miasta „POZnan*” – brak oficjalnego pliku; dodać po otrzymaniu od Urzędu Miasta.
- Ujęcie otwierające rolki 1 nagrane kamerą (ręka, szklanka, widok z góry) zamiast animacji.

