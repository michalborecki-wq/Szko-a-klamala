"""Ranking 20 pomysłów i model finansowy zwycięzcy („Komplet”).

Uruchom: python3 docs/biznes-przyszlosci/model.py
Wszystkie liczby w raporcie RAPORT.md pochodzą z tego skryptu.
Oceny 1–5 to ocena eksperta (5 = korzystnie dla nas), nie dane rynkowe.
"""

KRYTERIA = [  # (nazwa, waga)
    ("rynek", 1.0), ("problem", 1.5), ("placi", 1.5), ("konkurencja", 1.0),
    ("koszt_startu", 0.8), ("AI", 1.0), ("subskrypcja", 1.2), ("eksport", 0.6),
    ("marza", 1.0), ("pozyskanie", 1.4),
]

POMYSLY = {
    "Komplet – AI kompletuje dokumenty klientów biur rachunkowych": [4, 5, 4, 3, 4, 5, 5, 3, 5, 4],
    "AI asystent przetargowy (SWZ → oferta) dla MŚP":              [4, 5, 5, 2, 3, 4, 4, 3, 4, 3],
    "Głosowa recepcjonistka AI dla gabinetów i warsztatów":         [4, 4, 3, 2, 4, 4, 5, 3, 3, 2],
    "Pisma obywatelskie z AI (sprzeciw, reklamacja, skarga) B2C":   [3, 4, 3, 3, 5, 5, 1, 2, 5, 5],
    "Tutor AI wg kryteriów CKE (E8, matura)":                       [4, 4, 3, 1, 4, 5, 3, 2, 4, 3],
    "Audyt dostępności e-sklepów (Polski Akt o Dostępności)":       [2, 3, 2, 3, 4, 3, 3, 4, 4, 3],
    "AI do wniosków o dotacje (FENG, programy regionalne)":         [3, 4, 4, 2, 4, 4, 1, 2, 4, 3],
    "Oprogramowanie AI dla wspólnot mieszkaniowych":                [3, 3, 3, 3, 3, 3, 5, 1, 4, 2],
    "Fakturowanie KSeF dla mikrofirm (2027)":                       [4, 3, 2, 1, 4, 2, 5, 1, 3, 1],
    "AI skrzynka urzędowa JDG (e-Doręczenia, ZUS, US)":             [3, 3, 2, 3, 4, 4, 4, 2, 4, 2],
    "Compliance AI Act / RODO dla MŚP":                             [2, 2, 2, 3, 4, 3, 4, 4, 4, 2],
    "Compliance NIS2 / KSC dla średnich firm":                      [3, 4, 4, 2, 3, 3, 4, 4, 4, 2],
    "Miękka windykacja z danych KSeF dla MŚP":                      [4, 4, 3, 3, 4, 4, 4, 3, 4, 3],
    "Marketplace podwykonawców budowlanych z wyceną AI":            [4, 3, 2, 2, 2, 3, 2, 2, 3, 1],
    "Wyceny i oferty AI dla instalatorów i ekip remontowych":       [3, 4, 3, 3, 4, 4, 4, 3, 4, 3],
    "Compliance najmu krótkoterminowego (rozp. UE 2024/1028)":      [2, 3, 3, 3, 4, 3, 4, 4, 4, 3],
    "Skryba medyczny AI dla prywatnych gabinetów":                  [4, 5, 4, 2, 2, 4, 5, 3, 4, 2],
    "Kadry i HR dla mikrofirm z AI":                                [3, 3, 3, 2, 3, 3, 4, 1, 4, 2],
    "Fabryka krótkich wideo dla lokalnych firm":                    [3, 3, 3, 1, 5, 4, 4, 3, 3, 4],
    "Agent AI obniżający rachunki domowe (prąd, telefon, polisy)":  [3, 3, 3, 3, 4, 3, 3, 4, 4, 3],
}


def ranking():
    maks = 5 * sum(w for _, w in KRYTERIA)
    wyniki = []
    for nazwa, oceny in POMYSLY.items():
        s = sum(o * w for o, (_, w) in zip(oceny, KRYTERIA))
        wyniki.append((round(100 * s / maks, 1), nazwa, oceny))
    return sorted(wyniki, reverse=True)


# ---------------- model finansowy ----------------
VAT = 0.23  # ceny netto – B2B odlicza VAT, więc nie wchodzi w przychód

PLANY = {"Biuro (do 40 klientów)": 249, "Pro (do 120 klientów)": 549, "Sieć (do 300 klientów)": 1190}

SCENARIUSZE = {
    #               nowe biura/mies. (m1..), wzrost/mies., ARPA zł, churn/mies., CAC zł
    "pesymistyczny": dict(start=4, wzrost=1.10, arpa=330, churn=0.035, cac=1600),
    "realistyczny":  dict(start=8, wzrost=1.12, arpa=420, churn=0.022, cac=1000),
    "optymistyczny": dict(start=12, wzrost=1.14, arpa=520, churn=0.015, cac=700),
}

# koszt zmienny na biuro / mies. (zł): AI ok. 2 400 dokumentów × ~0,02 zł + wiadomości
# + przetwarzanie płatności (~1,5% + 1 zł) + wsparcie
def koszt_zmienny(arpa):
    ai = 2400 * 0.02            # klasyfikacja/ekstrakcja dokumentu tanim modelem (~1 $/5 $ za 1 mln tokenów)
    wiadomosci = 15             # SMS/e-mail/WhatsApp – przypomnienia
    platnosc = arpa * 0.015 + 1
    wsparcie = 20               # ok. 10 min pracy wsparcia na biuro
    return ai + wiadomosci + platnosc + wsparcie


def koszty_stale(m):
    """Koszty stałe miesiąca m (1..24), zł netto."""
    infra = 600 if m <= 6 else 1500 if m <= 12 else 3000
    narzedzia_ksiegowosc = 900   # księgowość własna, domeny, poczta, prawnik (umowy, RODO)
    zespol = 0 if m <= 6 else 9000 if m <= 12 else 26000  # wsparcie od m7, + programista od m13
    return infra + narzedzia_ksiegowosc + zespol


def symulacja(p, miesiace=24):
    klienci, wiersze, nowi = 0.0, [], p["start"]
    gotowka = 20000
    for m in range(1, miesiace + 1):
        klienci = klienci * (1 - p["churn"]) + nowi
        przychod = klienci * p["arpa"]
        zmienne = klienci * koszt_zmienny(p["arpa"])
        marketing = nowi * p["cac"]
        stale = koszty_stale(m)
        ebit = przychod - zmienne - marketing - stale
        gotowka += ebit
        wiersze.append(dict(m=m, klienci=klienci, nowi=nowi, mrr=przychod, ebit=ebit, gotowka=gotowka,
                            marza_brutto=(przychod - zmienne) / przychod if przychod else 0))
        nowi *= p["wzrost"]
    return wiersze


def ltv(p):
    marza = p["arpa"] - koszt_zmienny(p["arpa"])
    return marza / p["churn"]


def dochod_wlasciciela(ebit_mies):
    """Sp. z o.o.: CIT 9% (mały podatnik) + 19% dywidenda → ok. 26,3% łącznie."""
    if ebit_mies <= 0:
        return 0
    return ebit_mies * (1 - 0.09) * (1 - 0.19)


def tabela_cenowa():
    out = []
    for cena in (49, 99, 199, 249, 420, 549, 1190):
        n = -(-100000 // cena)  # zaokrąglenie w górę
        out.append((cena, n, n * cena))
    return out


if __name__ == "__main__":
    print("== RANKING ==")
    for i, (wynik, nazwa, oc) in enumerate(ranking(), 1):
        print(f"{i:2}. {wynik:5}  {nazwa}  {oc}")
    print("\n== ILU KLIENTÓW NA 100 000 zł MRR ==")
    for cena, n, suma in tabela_cenowa():
        print(f"{cena:5} zł × {n:5} = {suma:,} zł".replace(",", " "))
    print("\n== KOSZT ZMIENNY NA BIURO ==")
    for nazwa, p in SCENARIUSZE.items():
        kz = koszt_zmienny(p["arpa"])
        print(f"{nazwa}: ARPA {p['arpa']} zł, koszt zmienny {kz:.0f} zł, marża brutto {(1-kz/p['arpa'])*100:.0f}%,"
              f" LTV {ltv(p):,.0f} zł, CAC {p['cac']} zł, LTV/CAC {ltv(p)/p['cac']:.1f}, "
              f"zwrot CAC {p['cac']/(p['arpa']-kz):.1f} mies.")
    for nazwa, p in SCENARIUSZE.items():
        w = symulacja(p)
        print(f"\n== {nazwa.upper()} ==")
        for r in w:
            if r["m"] in (3, 6, 9, 12, 18, 24):
                print(f"m{r['m']:2}: biura {r['klienci']:6.0f}  nowe {r['nowi']:5.0f}  MRR {r['mrr']:10,.0f}  "
                      f"EBIT {r['ebit']:10,.0f}  gotówka {r['gotowka']:11,.0f}  "
                      f"dochód właściciela {dochod_wlasciciela(r['ebit']):9,.0f}".replace(",", " "))
        dojscie = next((r["m"] for r in w if r["mrr"] >= 100000), None)
        dno = min(r["gotowka"] for r in w)
        print(f"100 tys. MRR w miesiącu: {dojscie}; najniższy stan gotówki: {dno:,.0f} zł".replace(",", " "))
