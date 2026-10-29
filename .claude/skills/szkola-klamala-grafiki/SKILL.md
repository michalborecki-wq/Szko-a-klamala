---
name: szkola-klamala-grafiki
description: Profesjonalne grafiki i plansze wideo dla konta „Szkoła kłamała” (Instagram, TikTok) – karuzele 4:5, zdjęcia 9:16, okładki „hero”, plansze Reelsów i MP4, w jednolitym stylu marki (granat, niebieskie smugi, żółte akcenty, czerwony pędzel), z automatyczną kontrolą stref bezpiecznych i czytelności. Używaj ZAWSZE, gdy trzeba zrobić, poprawić lub przerobić jakąkolwiek grafikę, slajd, okładkę, planszę, karuzelę, Reel, rolkę albo miniaturę dla „Szkoła kłamała” / @szkola_klamala – także gdy pada tylko „zrób grafiki”, „slajdy do posta”, „wersja na TikToka”, „hero”, „okładka”, „żeby wyglądało profesjonalnie”. Treść i rzetelność faktów opisuje skill instagram-mich-bor; ten skill odpowiada za wygląd i pliki.
---

# Grafiki „Szkoła kłamała”

Ten skill zamienia gotową, sprawdzoną treść w pliki gotowe do publikacji. Wygląd ma być taki, żeby konto wyglądało jak redakcja, a nie jak ktoś z Canvy: jeden spójny system, mało tekstu, duże liczby, równe marginesy, nic nie ucięte i nic pod przyciskami aplikacji.

Treść (temat, fakty, źródła, podpisy, hashtagi) pochodzi ze skilla **instagram-mich-bor** albo od Michała. Tu nie wymyślamy faktów – każda liczba na slajdzie musi mieć źródło lub być policzona w kodzie.

## Jak pracować

1. **Rozpisz treść na slajdy** w pliku JSON (format: `references/spec-format.md`). Nie pisz HTML ręcznie – szablony w `scripts/render.py` pilnują typografii, siatki i stref bezpiecznych. Dobierz typ slajdu do treści (tabela niżej).
2. **Wyrenderuj:**
   ```bash
   python <ścieżka-skilla>/scripts/render.py spec.json --out <katalog> --sheet --video
   ```
   `--sheet` tworzy podgląd zbiorczy każdego posta, `--video` składa MP4 dla postów `"format": "reel"`.
3. **Przeczytaj `qa_report.txt`.** Każde ostrzeżenie (⚠) oznacza błąd do poprawienia – najczęściej za dużo tekstu. Poprawiaj **treść** (skróć zdanie, rozbij na dwa slajdy), a nie rozmiar czcionki: skrypt już zmniejszył tekst do granicy czytelności.
4. **Obejrzyj podglądy** (`_podglad_*.jpg`, narzędzie Read) i co najmniej jeden slajd w pełnej rozdzielczości. Szukaj: wdów i sierot w nagłówkach, nagłówka dłuższego niż 3–4 linie, slajdu „pustego” albo „przeładowanego”, powtórzeń wyrazów. Popraw i wyrenderuj ponownie.
5. **Dostarcz pliki post po poście** (SendUserFile), w kolejności publikacji, z podpisem „dzień · godzina · sieć · temat”. Na Instagram wysyłaj tylko wersje 4:5 lub MP4, na TikTok tylko 9:16 (`_916`, `_reel`). Nie wysyłaj ZIP-ów ani dwóch wersji tego samego slajdu do jednej sieci – Michał publikuje ręcznie z telefonu i duplikaty mylą.

## Typy slajdów – kiedy który

| Typ | Do czego | Zasada |
|---|---|---|
| `cover` | slajd 1 karuzeli, plansza 1 Reela | Haczyk w 6–9 słowach: `title` + żółty `accent`. Pod spodem 1 zdanie `sub`. |
| `hero` | okładka z jedną mocną liczbą/słowem | Liczba czytelna na miniaturze w siatce profilu. Najlepsza okładka do TikToka i siatki IG. |
| `myth` | MIT (przekreślony) → FAKT | Mit ≤ 12 słów, fakt ≤ 25 słów, kluczowa liczba w `**…**`. |
| `number` | jedna duża liczba + wyjaśnienie | `big` maks. ~9 znaków (np. `×14`, `243 > 225`, `1 mln`). |
| `bars` | porównanie 2–6 wartości | Wartości policzone w kodzie; jednostka w `note` albo w etykiecie. |
| `text` | wyjaśnienie jednego kroku | 1 myśl na slajd, ≤ 30 słów. |
| `versus` | „Spór tygodnia”: ZA / PRZECIW | Równa objętość obu stron, każde ze źródłem w `source`. |
| `quiz` | quiz z odliczaniem (Reel) | Te same opcje we wszystkich klatkach; `countdown` 3→2→1, potem `reveal`. |
| `outro` | ostatni slajd | Otwarte pytanie merytoryczne (bez „wpisz A albo B”), źródła, miejsce na logo partnera. |

## Zasady, które robią „profesjonalnie”

- **Jedna myśl na slajd.** Limit to ok. 30 słów (QA ostrzega). Gdy treść się nie mieści, dodaj slajd, nie zmniejszaj liter.
- **Liczba jest bohaterem.** Gdy fakt ma liczbę, daj ją w `big`, w `num` albo w `**pogrubieniu**` (robi się żółta). Żółty to wyłącznie akcent: maks. 1–2 wyróżnienia na slajd, inaczej przestaje działać.
- **Hierarchia jest stała:** etykieta → nagłówek → treść → źródło. Nie dodawaj własnych kolorów, czcionek, emoji na slajdach, ramek ani cieni – system już je ma. Spójność siatki profilu jest ważniejsza niż efekt pojedynczego slajdu.
- **Slajd 1 i plansza 1 to haczyk widoczny od pierwszej klatki**, bez intro i bez logo na początku. Slajd 2 karuzeli musi działać samodzielnie, bo Instagram pokazuje karuzelę drugi raz od slajdu 2.
- **Strefy bezpieczne 9:16 są wbudowane** (góra ok. 250 px na nazwę konta, dół ok. 430 px na podpis i dźwięk, prawa krawędź ok. 150 px na przyciski TikToka). Nie przesuwaj treści poza nie.
- **Polska typografia:** półpauza (–), cudzysłów „…”, twarde spacje po jednoliterowych wyrazach dodawane automatycznie. Nie pisz wersalikami w treści – szablon sam robi wersaliki w nagłówkach.
- **Źródło na slajdzie** w polu `source` (krótko: „NASA”, „Encyclopaedia Britannica”), pełne linki w podpisie i raporcie.
- **Zdjęcia i ilustracje:** domyślnie ich nie ma – typografia i liczby wystarczą i nie łamią praw autorskich. Ilustracje AI tylko niefotorealistyczne, nigdy wizerunki prawdziwych osób; wtedy oznacz treść jako AI przy publikacji.
- **Reklama:** gdy post jest płatną współpracą, `cover.sub` zaczyna się od „Reklama · współpraca z [marka]” (UOKiK), a logo partnera trafia w miejsce `partner_slot` na ostatnim slajdzie.

## Reelsy (MP4) – animowane napisy

- Plansze w formacie `reel`, 3–6 plansz, łącznie 8–20 s. Z flagą `--video` każdy Reel dostaje **animowane napisy** (kinetyczna typografia) – szczegóły ruchu i zasady opisuje skill **szkola-klamala-animacje**. `"animate": false` w poście wraca do prostego pokazu plansz.
- `durations` w sekundach na planszę: haczyk 2,4–3 s, treść 4–4,5 s (napisy najpierw wjeżdżają, potem trzeba zdążyć przeczytać), puenta 3,5–4 s, odliczanie quizu po 1 s. QA ostrzega, gdy wejście napisów zjada czas na czytanie.
- 30 kl./s, H.264, **cicha ścieżka AAC**. Muzykę Michał dodaje w aplikacji (biblioteka IG / dźwięki z trendów TikToka) – nigdy nie wgrywaj własnych MP3.
- Render z rozmyciem ruchu trwa ok. 1,5–2 min na 10 s filmu; `--draft` daje szybki podgląd bez rozmycia (do sprawdzania układu, nie do publikacji).
- Po złożeniu sprawdź `ffprobe` (długość, ścieżka audio) i obejrzyj klatki z kilku momentów: początek (haczyk musi być czytelny w klatce 0), środek wejścia napisów, przejście, koniec każdej planszy.

## Wymagania techniczne

Python z Playwright (Chromium), Pillow i ffmpeg. Czcionka **Inter / Inter Display** (z grubością Black Italic) musi być zainstalowana. Sprawdź: `fc-list | grep -i "Inter Display"`. Jeśli jej brak, zainstaluj Inter z oficjalnego wydania (github.com/rsms/inter) do `~/.fonts` i uruchom `fc-cache -f`. Bez Inter grafiki wyglądają amatorsko, więc nie renderuj na czcionce zastępczej.

## Pliki skilla

- `scripts/render.py` – silnik: szablony, autodopasowanie tekstu, QA, podglądy, MP4.
- `references/spec-format.md` – pełny format JSON z polami każdego typu slajdu. Przeczytaj przed pierwszym użyciem.
- `references/design-system.md` – tokeny marki, siatka, skala typografii, strefy bezpieczne i uzasadnienia. Czytaj, gdy trzeba zmienić wygląd albo dodać nowy typ slajdu.
- `examples/przyklad.json` – działający przykład wszystkich typów (karuzela + wersja 9:16, hero, quiz-Reel).
