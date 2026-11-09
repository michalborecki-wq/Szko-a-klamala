#!/usr/bin/env python3
"""
Zdjęcia na wolnych licencjach do planszy „foto” (decyzja Michała 9.11 – wariant bez kosztów).

  python3 zdjecia.py --szukaj "Morskie Oko"                # Openverse: tylko wolne licencje, źródło Commons
  python3 zdjecia.py --commons "File:Nazwa.jpg"            # albo URL strony pliku na commons.wikimedia.org
  python3 zdjecia.py --nasa <nasa_id>                      # images.nasa.gov – domena publiczna
  python3 zdjecia.py --plik foto.jpg --autor "…" --licencja "CC BY-SA 4.0" --zrodlo "https://…"   # pobrane ręcznie

Wynik: zrodla/zdjecia/<slug>.jpg + <slug>.json (autor, licencja, url licencji, źródło, serwis, data pobrania).
Plansza: {"type": "foto", "zdjecie": "zrodla/zdjecia/<slug>.jpg", ...} – render.py czyta metadane sam.

Dozwolone: CC0, domena publiczna, CC BY, CC BY-SA. Odrzucane: NC, ND, „all rights reserved”, brak licencji.
PAP, Reuters i inne agencje NIE są źródłem zdjęć (prawa zastrzeżone) – tylko faktów i nagłówków (plansza „wycinek”).
Google Grafika z filtrem „Licencje Creative Commons” służy do szukania; licencję zawsze potwierdza strona źródłowa.
"""
import argparse
import datetime as dt
import html
import json
import re
import shutil
import sys
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "zrodla" / "zdjecia"
UA = "SzkolaKlamalaZdjecia/1.0 (https://github.com/michalborecki-wq/Szko-a-klamala) python-urllib"


def licencja_ok(lic):
    u = (lic or "").upper().replace("‑", "-")
    if not u or re.search(r"\bNC\b|\bND\b|NON-?COMMERCIAL|NO-?DERIV|ALL RIGHTS RESERVED|FAIR USE", u):
        return False
    return any(k in u for k in ("CC0", "PUBLIC DOMAIN", "DOMENA PUBLICZNA", "PD-", "CC BY", "CC-BY", "NASA"))


def bez_html(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t or ""))).strip()


def slug(t):
    t = re.sub(r"^(File|Plik):", "", t)
    t = re.sub(r"\.[a-z0-9]{3,4}$", "", t, flags=re.I)
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60] or "zdjecie"


def get(url, binary=False, proby=4):
    """Pobranie z ponowieniem przy 429/503 (Wikimedia ogranicza wspólne adresy chmury) – czeka wg Retry-After, maks. 4 próby."""
    import time
    for k in range(proby):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                b = r.read()
            return b if binary else json.loads(b.decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or k == proby - 1:
                raise
            ra = e.headers.get("Retry-After")
            time.sleep(min(30, int(ra) if ra and ra.isdigit() else 2 ** (k + 1)))


def zapisz(sl, jpg_bytes_or_path, meta):
    if not licencja_ok(meta.get("licencja")):
        sys.exit(f"ODRZUCONE: licencja „{meta.get('licencja')}” – tylko CC0, domena publiczna, CC BY, CC BY-SA (bez NC/ND).")
    brak = [k for k in ("autor", "licencja", "zrodlo") if not meta.get(k)]
    if brak:
        sys.exit(f"ODRZUCONE: brak {', '.join(brak)}.")
    OUT.mkdir(parents=True, exist_ok=True)
    jp = OUT / f"{sl}.jpg"
    import io
    from PIL import Image
    src = io.BytesIO(jpg_bytes_or_path) if isinstance(jpg_bytes_or_path, (bytes, bytearray)) else jpg_bytes_or_path
    im = Image.open(src).convert("RGB")
    if max(im.size) > 2400:                        # 2400 px wystarcza na pełny kadr 4K po kadrowaniu; repo zostaje lekkie
        k = 2400 / max(im.size); im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    im.save(jp, "JPEG", quality=90)
    meta["pobrano"] = dt.date.today().isoformat()
    json.dump(meta, open(jp.with_suffix(".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(jp)
    print(json.dumps(meta, ensure_ascii=False))
    return jp


def commons_meta(info, tytul):
    em = info.get("extmetadata", {})
    v = lambda k: bez_html(em.get(k, {}).get("value", ""))
    lic = v("LicenseShortName") or v("License")
    return {"autor": v("Artist") or v("Credit"), "licencja": lic, "licencja_url": v("LicenseUrl"),
            "zrodlo": info.get("descriptionurl") or f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(tytul)}",
            "serwis": "Wikimedia Commons", "atrybucja_wymagana": v("AttributionRequired")}


def commons(tytul, plik_json=None):
    curid = re.search(r"curid=(\d+)", tytul)
    if curid:                                      # adres z Openverse: commons…/index.php?curid=N → tytuł pliku z API
        d0 = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
            {"action": "query", "pageids": curid.group(1), "format": "json"}))
        tytul = next(iter(d0["query"]["pages"].values()))["title"]
    elif tytul.startswith("http"):
        tytul = urllib.parse.unquote(tytul.rsplit("/wiki/", 1)[-1])
    if not re.match(r"^(File|Plik):", tytul):
        tytul = "File:" + tytul
    if plik_json:                                  # test offline na zapisanej odpowiedzi API
        d = json.load(open(plik_json, encoding="utf-8"))
    else:
        d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
            "action": "query", "titles": tytul, "prop": "imageinfo", "iiprop": "url|extmetadata",
            "iiurlwidth": 1920, "format": "json"}))
    page = next(iter(d["query"]["pages"].values()))
    if "imageinfo" not in page:
        sys.exit(f"Brak pliku na Commons: {tytul}")
    info = page["imageinfo"][0]
    meta = commons_meta(info, tytul)
    if not licencja_ok(meta["licencja"]):
        sys.exit(f"ODRZUCONE: {tytul} – licencja „{meta['licencja']}”.")
    if plik_json:
        print(json.dumps(meta, ensure_ascii=False)); return None
    # Wikimedia serwuje automatom miniatury do 1920 px (większe i oryginały → HTTP 429 dla adresów chmury);
    # kolejność: miniatura z API → Special:FilePath 1920 → 1280
    nazwa = urllib.parse.quote(re.sub(r"^(File|Plik):", "", tytul).replace(" ", "_"))
    kandydaci = [u for u in (info.get("thumburl"),
                             f"https://commons.wikimedia.org/wiki/Special:FilePath/{nazwa}?width=1920",
                             f"https://commons.wikimedia.org/wiki/Special:FilePath/{nazwa}?width=1280") if u]
    dane, ost = None, None
    for u in kandydaci:
        try:
            dane = get(u, binary=True); break
        except urllib.error.HTTPError as e:
            ost = e
    if dane is None:
        sys.exit(f"Nie udało się pobrać pliku z Commons ({ost}). Pobierz ręcznie i użyj --plik z danymi licencji ze strony: {meta['zrodlo']}")
    return zapisz(slug(tytul), dane, meta)


def nasa(nid):
    md = get("https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"nasa_id": nid}))
    it = md["collection"]["items"]
    if not it:
        sys.exit(f"Brak {nid} w images.nasa.gov")
    d = it[0]["data"][0]
    opis = (d.get("description") or "") + " " + (d.get("secondary_creator") or "")
    if re.search(r"copyright|©|courtesy of (?!NASA)", opis, re.I):
        sys.exit(f"UWAGA: {nid} ma dopisek o prawach osób trzecich – sprawdź ręcznie, nie pobieram automatycznie.")
    assets = [x["href"] for x in get(f"https://images-api.nasa.gov/asset/{urllib.parse.quote(nid)}")["collection"]["items"]]
    url = next((a for a in assets if re.search(r"~(large|orig)\.jpe?g$", a, re.I)), next((a for a in assets if a.lower().endswith((".jpg", ".jpeg"))), None))
    if not url:
        sys.exit(f"{nid}: brak pliku JPG")
    meta = {"autor": d.get("photographer") or d.get("center") and f"NASA/{d['center']}" or "NASA", "licencja": "Domena publiczna (NASA)",
            "zrodlo": f"https://images.nasa.gov/details/{nid}", "serwis": "NASA Image and Video Library", "tytul": d.get("title")}
    return zapisz(slug(nid), get(url.replace("http://", "https://"), binary=True), meta)


def szukaj(fraza, n=8):
    """Openverse (api.openverse.org): tylko CC0, domena publiczna, CC BY, CC BY-SA, źródło Wikimedia Commons."""
    d = get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": fraza, "license": "cc0,pdm,by,by-sa", "source": "wikimedia", "page_size": n}))
    print(f"wyników: {d.get('result_count')} (pokazuję {len(d['results'])}; licencję i tak sprawdza --commons na stronie pliku)")
    for r in d["results"]:
        print(f"- {r.get('width')}×{r.get('height')} | {r['license'].upper()} {r.get('license_version') or ''} | {r.get('creator')} | {r.get('title')}\n"
              f"  python3 VIRAL_REELS_FACTORY/narzedzia/zdjecia.py --commons \"{r['foreign_landing_url']}\"")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--commons"); g.add_argument("--nasa"); g.add_argument("--plik"); g.add_argument("--szukaj")
    ap.add_argument("--autor"); ap.add_argument("--licencja"); ap.add_argument("--zrodlo"); ap.add_argument("--serwis")
    ap.add_argument("--slug")
    ap.add_argument("--offline-json", help="test: odpowiedź API Commons zapisana w pliku (bez sieci, bez pobierania)")
    a = ap.parse_args()
    if a.szukaj:
        szukaj(a.szukaj)
    elif a.commons:
        commons(a.commons, a.offline_json)
    elif a.nasa:
        nasa(a.nasa)
    else:
        meta = {"autor": a.autor, "licencja": a.licencja, "zrodlo": a.zrodlo, "serwis": a.serwis or ""}
        zapisz(a.slug or slug(Path(a.plik).name), a.plik, meta)


if __name__ == "__main__":
    main()
