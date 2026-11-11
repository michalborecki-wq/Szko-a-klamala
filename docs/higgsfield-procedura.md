# Higgsfield – ścisła procedura pozyskiwania i tworzenia materiałów (decyzja Michała 11.11)

Konektor Higgsfield jest podłączony na koncie (plan Plus; w liście narzędzi sesji bywa widoczny pod inną etykietą – narzędzia `generate_image`, `generate_video`, `balance`, `jobs_wait`). **Saldo 11.11: 0 kredytów.** Bez kredytów pracujemy wyłącznie na zasobach z `zrodla/ai_higgsfield/`.

## 0. Zasada nadrzędna
Każdy kredyt ma przypisaną rolkę. Nic nie generujemy „na zapas”, „do testu” ani pod temat już opublikowany.

## 1. Zanim cokolwiek wygenerujesz (wszystkie punkty obowiązkowe)
1. **Najpierw magazyn:** sprawdź `zrodla/ai_higgsfield/REJESTR.md` – jeśli pasuje zasób ze statusem „wolny”, użyj go i nie generuj.
2. **Temat nieopublikowany:** `docs/opublikowane.md` + kalendarz. Temat musi mieć wiersz w kalendarzu z datą w ciągu 7 dni.
3. **Fakty gotowe:** scenariusz po weryfikacji (2 źródła). Najpierw scenariusz, potem obraz – nigdy odwrotnie.
4. **Saldo i koszt:** `balance` → policz koszt z cennika (pkt 3). Zgoda Michała na wydatek jest wymagana **za każdym razem** (w wiadomości: temat, co powstanie, ile kredytów, ile zostanie). Zadanie cykliczne NIGDY nie wydaje kredytów.
5. **Limit na rolkę:** maks. 1 klip wideo (7,5 kr.) + 2 obrazy (0,5 kr.) = 8 kr. Seedance (35 kr.) i upscale – tylko na wyraźne polecenie Michała.

## 2. Co wolno generować
- **Tak:** tło-przebitka pod plansze (ruch w 1. sekundzie), obraz-bohater okładki, uniwersalne motywy marki (tablica, lupa, waga, klepsydra).
- **Nie:** ludzie i twarze, policjanci, politycy, prawdziwe miejsca zdarzeń, logo i marki, tablice rejestracyjne, mundury z oznaczeniami, dokumenty wyglądające na prawdziwe, czytelny tekst w kadrze (tekst kładzie silnik), broń, przemoc, wypadki, tragedie, cokolwiek, co widz mógłby wziąć za nagranie wydarzenia.
- Tematy zakazane w CLAUDE.md pozostają zakazane także jako ilustracja.

## 3. Parametry (stałe – nie zmieniać bez powodu)
| Rodzaj | Model | Format | Koszt | Uwagi |
|---|---|---|---|---|
| Obraz | gpt_image_2_6 | 9:16 | 0,25 kr. | okładka, kadr startowy do wideo |
| Wideo | kling3_0, 5 s, bez dźwięku | 9:16 | 7,5 kr. | obraz→wideo z własnego kadru startowego (przewidywalny wynik); dźwięk robi nasz silnik |
| Wideo premium | seedance_2_5, 5 s | 9:16 | 35 kr. | tylko na polecenie Michała |

Prompt (po angielsku, jeden akapit): przedmiot + powolny ruch kamery (slow push-in / orbit) + „dark navy background #0A0E18, electric blue #2F6BFF rim light, yellow #FFC727 accent, cinematic, shallow depth of field, no people, no text, no logos, vertical 9:16”. Ciemne tło jest konieczne – na nim leży biały i żółty tekst plansz.

## 4. Po wygenerowaniu
1. Obejrzyj wynik (klatki: początek, środek, koniec). Odrzuć, jeśli: pojawił się tekst/logo/człowiek, obraz jest jasny pod tekstem, ruch szarpie. Odrzut też wpisz do rejestru (żeby nie powtarzać promptu).
2. Zapisz: `zrodla/ai_higgsfield/<RRRR-MM-DD>/wideo|obrazy/<nazwa>.mp4|.jpg` (nazwy małymi literami, bez polskich znaków).
3. Dopisz wiersz do `zrodla/ai_higgsfield/REJESTR.md`: plik, data, model, koszt, prompt (skrót), rolka docelowa, status.
4. W rolce: `python3 VIRAL_REELS_FACTORY/narzedzia/wideo_tlo.py <plik> --sek 40 --jasnosc -0.15` → w poście `"tlo3d": {"klatki": "VIRAL_REELS_FACTORY/VIDEOS/tla/<nazwa>", "fps": 30, "krycie": 0.5}` i **zawsze** `"etykieta_ai": true`. W opisie zdanie: „Tło: ilustracja AI (Higgsfield) – nie jest nagraniem.”
5. Po wysyłce rolki zmień status w rejestrze na „użyty <data> – <rolka>”. Jeden klip = jedna rolka jako motyw główny (potem tylko jako drugoplanowe tło w innym temacie).
6. Commit zasobu i rejestru razem z rolką.

## 5. Rozliczenie
Po każdej sesji generowania w wiadomości do Michała: wydane / pozostałe kredyty, lista plików, do których rolek. Raz w tygodniu (ig-audit): porównanie śr. czasu oglądania rolek z tłem AI i bez – jeśli tło nie daje poprawy przez 2 tygodnie, wstrzymujemy generowanie.
