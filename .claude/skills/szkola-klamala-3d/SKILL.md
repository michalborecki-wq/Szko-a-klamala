---
name: szkola-klamala-3d
description: Sceny 3D w Blenderze jako tło rolek „Szkoła kłamała” (@szkola_klamala) – planety, orbity, Ziemia z osią, obiekty i schematy w ruchu kamery, w palecie marki (granat, niebieski #2F6BFF, żółty #FFC727), renderowane Cycles na CPU i podkładane pod animowane plansze silnika. Używaj, gdy rolka zyska na pokazaniu zjawiska w 3D (kosmos, ciało, mechanizm auta, fizyka), przy prośbach „w 3D”, „jak Zack D. Films”, „animacja 3D”, „Blender”. Treść i fakty – CLAUDE.md i szkola-klamala-viral; plansze, muzyka i logo – szkola-klamala-animacje.
---

# Sceny 3D (Blender)

Blender 4.2 LTS (darmowy) renderuje scenę 3D jako sekwencję klatek, a silnik rolek (`render.py`) podkłada je pod plansze. Napisy, muzyka, logo i 4K działają jak zawsze. 3D jest **tłem, które pokazuje zjawisko**. Nie zastępuje tekstu, bo widz często ogląda bez dźwięku i musi przeczytać fakt.

Instalacja (kontener jest ulotny): `bash scripts/instaluj.sh` (sekcja Blender) albo ręcznie z download.blender.org do `/opt/blender`.

## Jak pracować

1. Scenariusz wg `szkola-klamala-viral`, plansze w JSON jak zwykle.
2. **Najpierw długości plansz.** Zrób szybki podgląd bez 3D: `render.py spec.json --out draft --video --draft`. Z `draft/<id>_zdarzenia.json` (`plansze`) odczytaj, kiedy zaczyna się każda plansza, i ułóż ruch sceny pod te momenty (odpowiedź, twist, zbliżenie).
3. **Scena:** `scripts/sceny/<temat>.py` korzysta ze wspólnego `scripts/marka3d.py`. W nim są paleta marki, tło z gwiazdami, materiały emisyjne, kamera 9:16, poświata i render z wznawianiem. Wzór: `sceny/pory_roku.py`.
4. **Próbne klatki** (kilka momentów, mała rozdzielczość) → arkusz → Read:
   ```bash
   blender -b -P .claude/skills/szkola-klamala-3d/scripts/sceny/pory_roku.py -- --out test --sek 23 --szer 540 --probki 16 --od 300 --do 300
   ```
5. **Render pełny** (długość = suma plansz bez logo, `--sek`):
   ```bash
   blender -b -P .../sceny/<temat>.py -- --out klatki3d --sek 23 --szer 720 --probki 16
   ```
   Na tej maszynie (4 rdzenie, bez karty graficznej) to ok. 3,5 s na klatkę, czyli ok. 40 min na 23 s. Render pomija gotowe klatki, więc po restarcie kontenera wystarczy go uruchomić ponownie. Odszumianie jest wyłączone, bo kosztuje ok. 2 s na klatkę (`--odszum 1`, gdy scena ma dużo miękkich cieni). Ziarno marki i przyciemnienie ukrywają resztkowy szum.
6. **Podłączenie do rolki:** w poście dopisz
   ```json
   "tlo3d": {"klatki": "klatki3d", "fps": 30, "krycie": 0.9}
   ```
   Następnie uruchom zwykłe `render.py spec.json --out out --video --muzyka`. Tło 3D zastępuje warstwę gwiazd, siatki i kul (`fx.tlo = "3d"`) i przechodzi płynnie przez cięcia, bo klatka jest wybierana z czasu globalnego. Pod tekstem leży przyciemnienie (`.t3dv` w `ruch.py`), żeby napisy zostały czytelne.

## Zasady

- **Prawda w obrazie:** proporcje i ruch nie mogą sugerować nieprawdy. Przykład: orbita Ziemi jest prawie okrągła, więc nie rysuj mocnej elipsy. Gdy coś jest powiększone dla czytelności (rozmiar planet), napis nie może opierać się na tej skali.
- Paleta marki: granatowe tło, niebieskie linie #2F6BFF, żółte akcenty #FFC727 (osie, strzałki, wyróżnienia), czerwony #E53935 tylko do „mitu”. Żadnych tekstur ani modeli z internetu bez licencji – materiały proceduralne.
- Najważniejsze elementy kadruj w środkowym pasie, bo tekst plansz leży pośrodku, a strefy bezpieczne 9:16 są takie jak w `szkola-klamala-grafiki`. Jasne obiekty (Słońce) i tak zostaną przyciemnione pod napisami.
- Rozdzielczość: scena renderuje się w 720×1280 i jest skalowana do 4K. Napisy i grafika plansz zostają w 4K. Wyższa rozdzielczość (`--szer 1080`) to ok. 2,3× dłuższy render, więc tylko gdy obraz 3D jest głównym bohaterem.
- Ruch kamery jest powolny i płynny (`wygladz`), a jedna akcja przypada na planszę. Zbliżenie zgrywaj z planszą, która o nim mówi.
- Klip 3D w rolce oznaczasz tylko wtedy, gdy powstał w generatorze AI. Blender to animacja, nie AI.
- Zasada nr 8 montażu: przed wysłaniem obejrzyj arkusz klatek gotowego filmu (czytelność tekstu na tle 3D).
