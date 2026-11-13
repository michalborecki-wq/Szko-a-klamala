# Identyfikacja wizualna

Źródło prawdy dla silnika: skill `szkola-klamala-grafiki` (`scripts/render.py`, słownik `TOK`). Ten plik opisuje zasady użycia.

## Logo
- Plik: `.claude/skills/szkola-klamala-grafiki/assets/logo.png` (odznaka z biretem). Na końcu każdego filmu ok. 2,8 s animowanego outro z @szkola_klamala.
- Znak słowny „SZKOŁA KŁAMAŁA” u góry plansz (biały + żółty), mały, zawsze w tym samym miejscu.
- Logo i nazwy nie zmieniamy bez zgody Michała. Nie deformować, nie zmieniać kolorów, nie kłaść na jasnym zdjęciu bez ciemnej podkładki.

## Kolory
| Rola | Kolor | Użycie |
|---|---|---|
| Granat tła | #0A0E18 → #16203A | tło domyślne, tekst na żółtym |
| Niebieski | #2F6BFF | smugi, cień nagłówków, etykieta FAKT, nagłówek dokumentu |
| Żółty | #FFC727 | liczba, kluczowe słowo, marker, przycisk „Wyślij”, okładka żółta |
| Czerwony | #E53935 | stawka/kara, pieczątka, przekreślenie mitu, plansza TWIST |
| Biały | #FFFFFF / #F4F6FB | nagłówki, karta dokumentu |
**Zasada znaczeń:** żółty = „to zapamiętaj”, czerwony = „tu boli / tu jest fałsz”, niebieski = „to fakt / źródło”. Jeden kolor akcentu dominuje na planszy.
Proporcje w rolce: okładka żółta albo granatowa na zmianę; środek granatowy z poświatą wg typu planszy; nigdy płaska szarość.

## Typografia
- Nagłówki: Inter Display Black Italic, wersaliki, cień 7 px w niebieskim. Treść: Inter 400/800. Dokument: Georgia (cytat dosłowny).
- Tekst wypełnia ok. 84% pola (silnik powiększa sam). Minimum treści 44 px przy 1080 px szerokości.
- Hierarchia: 1 rzecz największa (liczba albo hasło), 1 średnia, źródło najmniejsze.

## Okładki i miniatury
- Nigdy sam tekst: obraz-bohater (`obrazy.py`: polska, torba, suwak, dowod, monety, opona, zegar, licznik, ruletka, saturn, odznaka, gwiazdki) + pieczątka + haczyk.
- Dwie sąsiednie okładki w siatce profilu nie mogą mieć tego samego układu i koloru tła.
- Haczyk ≤ 7 słów, czytelny w miniaturze (sprawdzać w skali 25%).

## Zdjęcia, ilustracje, AI
- Zdjęcia: tylko CC0, domena publiczna, CC BY, CC BY-SA; podpis „Fot. autor · licencja”.
- Ilustracja AI zawsze z etykietą; bez ludzi, logo, czytelnego tekstu. Procedura: `docs/higgsfield-procedura.md`.
- Wycinek prasowy = nasza plansza z dosłownym nagłówkiem, nigdy podróbka zrzutu ekranu.
