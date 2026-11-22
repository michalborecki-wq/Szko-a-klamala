#!/usr/bin/env python3
"""Czujnik „PILNE / NEWS” (decyzja Michała 22.11): gorące, skandaliczne tematy z agencji, TV i radia – na bieżąco.

  python3 pilne.py                 # jeden przegląd, wypisuje NOWE gorące tematy (stan w RESEARCH/pilne_stan.json)
  python3 pilne.py --co 15         # pętla: przegląd co 15 min (do Monitor – każda linia = alarm)
  python3 pilne.py --prog 9 --godziny 6

Źródła: PAP, TVN24, Reuters, RMF24, Polsat News, Radio ZET, Polskie Radio 24, TOK FM, Rzeczpospolita, Onet, WP,
Interia + pierwsze strony Google News PL. Każdy alarm = klaster nagłówków o tej samej sprawie z ≥ 2 redakcji
(albo 1 agencja: PAP/Reuters + 1 inna). Odrzuca tematy zakazane (CLAUDE.md). Punktuje skandal: policja, prokuratura,
zarzuty, afery, władza, pieniądze publiczne, NIK/RPO, wyroki, oznaczenia „pilne”.

Alarm to TYLKO kandydat. Przed rolką: dokument pierwotny/komunikat + 2. niezależne źródło, „sprawa w toku –
domniemanie niewinności” gdy brak wyroku, bez nazwisk policjantów (CLAUDE.md, „NOWA RUTYNA – ROLKA 7 S”).
"""
import argparse, datetime as dt, json, os, re, sys, time, urllib.parse
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from research import pobierz, data_wpisu, parsuj, norm  # noqa: E402

STAN = os.path.join(ROOT, "RESEARCH", "pilne_stan.json")
LOG = os.path.join(ROOT, "RESEARCH", "pilne_log.md")

ZRODLA = {
    "PAP": "site:pap.pl", "TVN24": "site:tvn24.pl", "RMF24": "site:rmf24.pl", "Polsat News": "site:polsatnews.pl",
    "Radio ZET": "site:radiozet.pl", "Polskie Radio 24": "site:polskieradio24.pl OR site:polskieradio.pl",
    "TOK FM": "site:tokfm.pl", "Rzeczpospolita": "site:rp.pl", "Onet": "site:wiadomosci.onet.pl",
    "WP": "site:wiadomosci.wp.pl", "Interia": "site:wydarzenia.interia.pl",
}
AGENCJE = r"pap|reuters"

SKANDAL = (r"afer|skandal|zatrzyma|zarzut|prokurat|śledztw|\bcba\b|\babw\b|korupc|łapówk|nadużyc|nielegaln|bezprawn|"
           r"dymisj|odwołan|wyrok|skazan|uniewinn|areszt|immunitet|przeszuk|policj|policjant|funkcjonariusz|komend|"
           r"\bnik\b|najwyższa izba|\brpo\b|rzecznik praw|uokik|kontrola wykazał|ujawni|kulis|ukrywa|tusz|nagrani|"
           r"premier|minist|posł|posłank|senator|prezydent|sejm|rząd|trybunał|sąd najwyższ|ustaw|weto|"
           r"mln zł|mld zł|milion|miliard|dotacj|przetarg|nagrod[ay] dla|premi[ae] dla|pensj[ae] (prezes|minist|posł)|"
           r"oburz|burza|kontrowers|szok|wstyd|kompromit|protest|pozew|odszkodowan|kara dla|grzywn")
PILNE = r"\bpilne\b|\bpilny\b|breaking|przed chwilą|właśnie|nieoficjalnie|ustalenia|tylko u nas|jest decyzja|najnowsze|zdecydował"
DUZE = r"premier|prezydent|minist|komendant główn|prokurator krajow|szef (cba|abw|policji)|marszał|prezes (nbp|trybunał|orlen|pkn|pzu|tvp)"


def kanaly(godziny):
    q = lambda s: "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": f"({s}) when:{godziny}h", "hl": "pl", "gl": "PL", "ceid": "PL:pl"})
    k = [(n, q(s)) for n, s in ZRODLA.items()]
    k.append(("TVN24 najnowsze", "https://tvn24.pl/najnowsze.xml"))
    k.append(("Pierwsze strony", "https://news.google.com/rss?hl=pl&gl=PL&ceid=PL:pl"))
    k.append(("Reuters", "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": f"site:reuters.com Poland when:{godziny}h", "hl": "en-US", "gl": "US", "ceid": "US:en"})))
    return k


def tokeny(t):
    return {w for w in norm(t).split() if len(w) > 3}


# Wojna/bezpieczeństwo – dozwolone, gdy dotyczy Polski (decyzja Michała 22.11); inne konflikty – poza kontem.
WOJNA = (r"wojn|wojsk|ukrain|rosj|rosyj|rosjan|putin|izrael|gaz[ay]\b|hamas|iran|nato|dron|rakiet|pocisk|ostrzał|front\b|"
         r"wtargn|obiekt(y|ów)? (nad|w) pols|królewi|okręt|myśliw|armi|zbrojn|alarm lotnicz|schron|obron[ay] cywil")
POLSKA = (r"pols|kraj\b|rcb|\bmon\b|dowództw|wojsko polskie|sił zbrojnych rp|lubelsk|podkarpac|podlas|warmi|mazow|"
          r"prokuratur|samorząd|wojewod|straż|policj|gmin|mieszkańc|kosiniak|tusk|nawrock|sikorsk|gawkowsk|kierwińsk")
SLUZBY = r"rcb|alert|syren|schron|ewakuac|służb|wojewod|samorząd|straż|policj|wojsko|dowództw|reakcj|zawiod|opóźni|nie zadział|brak"
# zawsze poza kontem (CLAUDE.md): religia, szczepionki, płeć, migracja, spiski + drastyczne treści
ZAKAZ_STALY = (r"religi|kości[oó]ł|papie|bisk|ksi[eę]dz|szczepi|aborc|gender|transpł|lgbt|migra|imigra|uchodźc|spisk|"
               r"ciał[ao]\b|zwłok|nie żyj|zmarł|śmier|zabój|zabit|zginęł|zgin[aą]ł|ofiar|morderst|gwałt|samobój|"
               r"tragedi|pobi[łt]|nożem|strzelanin|katastrof|lotto|losowani|kasyn|bukmach")


def redakcja(n):
    n = re.sub(r"^(www\.)|^wiadomości\s+", "", n.strip(), flags=re.I)
    n = re.sub(r"\s*(najnowsze|wiadomości|wydarzenia|\|.*)$", "", n, flags=re.I)
    return {"polsatnews.pl": "Polsat News", "wyborcza.pl": "Wyborcza", "polskieradio.pl": "Polskie Radio 24", "polskie radio": "Polskie Radio 24"}.get(n.lower(), n)


def ocena(t):
    tl = t.lower()
    if re.search(ZAKAZ_STALY, tl):
        return None
    pkt = 3 * len(set(re.findall(SKANDAL, tl)))
    if re.search(WOJNA, tl):
        if not re.search(POLSKA, tl):
            return None                      # konflikt bez związku z Polską
        pkt += 6                             # bezpieczeństwo kraju = temat dnia
        if re.search(SLUZBY, tl):
            pkt += 3                         # kąt: jak zachowały się służby / co zawiodło
    if re.search(PILNE, tl):
        pkt += 3
    if re.search(DUZE, tl):
        pkt += 2
    return pkt


def przeglad(godziny, prog):
    teraz = dt.datetime.now(dt.timezone.utc)
    wpisy = []
    for nazwa, url in kanaly(godziny):
        try:
            for w in parsuj(pobierz(url), nazwa):
                d = data_wpisu(w.get("data"))
                if d and (teraz - d).total_seconds() > godziny * 3600:
                    continue
                w["kanal"] = nazwa
                w["zrodlo"] = w.get("zrodlo") or nazwa
                wpisy.append(w)
        except Exception as e:  # jedna redakcja nie może zatrzymać czujnika
            print(f"[pilne] {nazwa}: {type(e).__name__}", file=sys.stderr)
    # klastry: ta sama sprawa = wspólne ≥ 50% słów (krótszego tytułu)
    klastry = []
    for w in wpisy:
        tw = tokeny(w["tytul"])
        if len(tw) < 3:
            continue
        for k in klastry:
            if len(tw & k["tok"]) / min(len(tw), len(k["tok"])) >= 0.5:
                k["wpisy"].append(w); k["tok"] |= tw; break
        else:
            klastry.append({"tok": set(tw), "wpisy": [w]})
    wyniki = []
    for k in klastry:
        red = {redakcja(w["zrodlo"]) for w in k["wpisy"]}
        glowny = max(k["wpisy"], key=lambda w: ocena(w["tytul"]) or -1)
        p = ocena(glowny["tytul"])
        if p is None or any(ocena(w["tytul"]) is None for w in k["wpisy"]):
            continue
        agencja = any(re.search(AGENCJE, r.lower()) for r in red)
        if len(red) < 2:
            continue
        p += min(6, 2 * (len(red) - 1)) + (2 if agencja else 0)
        if p >= prog:
            wyniki.append({"pkt": p, "tytul": re.sub(r"\s+-\s+[^-]{2,40}$", "", glowny["tytul"]),
                           "redakcje": sorted(red)[:8], "agencja": agencja,
                           "linki": [w["link"] for w in k["wpisy"]][:4], "klucz": " ".join(sorted(k["tok"]))[:200]})
    return sorted(wyniki, key=lambda x: -x["pkt"])


def nowe(wyniki):
    os.makedirs(os.path.dirname(STAN), exist_ok=True)
    stan = json.load(open(STAN)) if os.path.exists(STAN) else {"widziane": []}
    widz = [set(s.split()) for s in stan["widziane"]]
    out = []
    for w in wyniki:
        t = set(w["klucz"].split())
        if any(len(t & s) / max(1, min(len(t), len(s))) >= 0.5 for s in widz):
            continue
        out.append(w); widz.append(t); stan["widziane"].append(w["klucz"])
    stan["widziane"] = stan["widziane"][-400:]
    json.dump(stan, open(STAN, "w"), ensure_ascii=False)
    return out


def zglos(nw):
    teraz = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG, "a", encoding="utf-8") as f:
        for w in nw:
            f.write(f"- {teraz} | {w['pkt']} pkt | {w['tytul']} | {', '.join(w['redakcje'])} | {w['linki'][0]}\n")
            print(f"PILNE {w['pkt']}pkt | {w['tytul']} | {len(w['redakcje'])} redakcji: {', '.join(w['redakcje'][:5])}"
                  f"{' | AGENCJA' if w['agencja'] else ''} | {w['linki'][0]}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--godziny", type=int, default=6)
    ap.add_argument("--prog", type=int, default=8)
    ap.add_argument("--co", type=int, default=0, help="minuty między przeglądami (0 = jeden przegląd)")
    a = ap.parse_args()
    while True:
        zglos(nowe(przeglad(a.godziny, a.prog)))
        if not a.co:
            break
        time.sleep(a.co * 60)


if __name__ == "__main__":
    main()
