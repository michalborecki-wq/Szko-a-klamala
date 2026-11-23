# Otwarte sprawy

1. Zebrać wyniki 3 Reelsów „jeden mit” (Wenus, mózg, szkło) i porównać z Reelem o Merkurym (316 wyświetleń).
2. Za 2–3 tygodnie: wybrać zwycięzcę do promocji (wideo, cel „obserwujący”).
3. Rozważyć zaktualizowanie skilla `instagram-mich-bor` (usunąć Metricool, dodać nowe przedmioty i plan publikacji). Na razie te zmiany są tylko w prompcie zadania cyklicznego.
4. Media kit: przy ok. 5 tys. obserwujących albo stabilnie powyżej 10 tys. wyświetleń.
5. Zrobione 29.10: silnik grafik dodany do `.claude/skills/szkola-klamala-grafiki` i przetestowany na `examples/przyklad.json` (0 ostrzeżeń QA, MP4 z cichą ścieżką AAC).
- TikTok Shop (5.11): Michał weryfikuje zaproszenie w aplikacji, akceptuje, dodaje 3–5 produktów do Showcase i przysyła zrzut regulaminu – szczegóły `docs/tiktok-shop.md`.

## OmniRoute (23.11, prośba Michała „zainstaluj omniroute”)
- Zainstalowany w kontenerze sesji: `npm install -g omniroute --engine-strict=false` (v3.8.x, MIT, github.com/diegosouzapw/OmniRoute) + `omniroute runtime repair`. Start: `omniroute` → panel http://localhost:20128, API zgodne z OpenAI: http://localhost:20128/v1 (test 23.11: działa).
- Kontener jest ulotny – w nowej sesji instalacja od nowa (ok. 2 min, ok. 580 MB).
- Do zdecydowania z Michałem: do czego używamy (router modeli AI – wymaga kont/kluczy dostawców; klucze tylko w ustawieniach środowiska, budżet na płatne API 0 zł).
