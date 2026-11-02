import json, urllib.request, subprocess, os, sys, datetime
B="https://api.sejm.gov.pl/eli/acts/"
OUT=sys.argv[1]
def get(i): return json.load(urllib.request.urlopen(B+i,timeout=90))
def key(i): _,y,p=i.split('/'); return (int(y),int(p))
AKTY=[
 ("01_ustawa_o_policji","DU/1990/179"),
 ("02_kodeks_wykroczen","DU/1971/114"),
 ("03_kodeks_postepowania_w_sprawach_o_wykroczenia","DU/2001/1148"),
 ("04_srodki_przymusu_bezposredniego_i_bron_palna","DU/2013/628"),
 ("05_kodeks_postepowania_karnego","DU/1997/555"),
 ("06_kodeks_karny","DU/1997/553"),
 ("07_prawo_o_ruchu_drogowym","DU/1997/602"),
 ("08_kierujacy_pojazdami","DU/2011/151"),
 ("09_wychowanie_w_trzezwosci","DU/1982/230"),
 ("10_dowody_osobiste","DU/2019/653"),
 ("11_straze_gminne","DU/1997/779"),
 ("12_ochrona_osob_i_mienia","DU/1997/740"),
 ("13_konstytucja","DU/1997/483"),
 ("14_kodeks_postepowania_administracyjnego_skargi","DU/1960/168"),
 ("15_przeciwdzialanie_narkomanii","DU/2005/1485"),
 ("20_taryfikator_mandatow_wysokosc_grzywien","DU/2003/2023"),
 ("21_nakladanie_grzywien_w_drodze_mandatu","DU/2002/201"),
 ("22_uprawnienia_policjantow_legitymowanie_zatrzymanie_kontrola","DU/2023/2535"),
 ("23_kontrola_ruchu_drogowego","DU/2019/2141"),
 ("24_dokumentowanie_kontroli_osobistej","DU/2019/904"),
 ("25_badania_na_zawartosc_alkoholu","DU/2018/2472"),
 ("26_wykroczenia_mandaty_strazy_gminnej","DU/2003/2026"),
]
idx=[]
for nazwa,i in AKTY:
    d=get(i)
    tj=[x['id'] for x in d['references'].get('Inf. o tekście jednolitym',[])]
    src=max(tj,key=key) if tj else i
    s=get(src)
    data_src=s.get('announcementDate') or s.get('promulgation')
    zm=[x for x in d['references'].get('Akty zmieniające',[]) if x.get('date','') > (s.get('promulgation') or '')]
    zm_info=[]
    for x in sorted(zm,key=lambda x:x['id']):
        z=get(x['id']); zm_info.append(f"{z['displayAddress']} (wejście w życie {z.get('entryIntoForce','?')}) – {z['title'][:160]}")
    pdf=f"{OUT}/{nazwa}.pdf"
    urllib.request.urlretrieve(B+src+"/text.pdf",pdf)
    subprocess.run(["pdftotext","-layout",pdf,f"{OUT}/{nazwa}.txt"],check=True)
    idx.append((nazwa,d['title'],d['displayAddress'],s['displayAddress'],d['status'],zm_info))
    print(nazwa,s['displayAddress'],len(zm_info),"zmian po t.j.",flush=True)
with open(f"{OUT}/INDEKS.md","w") as f:
    f.write(f"# Akty prawne – co może policja (pobrane z API Sejmu ELI, {datetime.date.today():%d.%m.%Y})\n\n")
    f.write("Teksty jednolite (PDF z Dziennika Ustaw) + wersja .txt do przeszukiwania. **Zmiany po tekście jednolitym trzeba czytać osobno** – lista pod każdym aktem. Przed rolką sprawdzić przepis w ISAP (isap.sejm.gov.pl) na dzień publikacji.\n\n")
    for n,t,a,s,st,zm in idx:
        f.write(f"## {n}\n- {t}\n- pierwotnie: {a}; plik: tekst jednolity **{s}**; status: {st}\n")
        f.write("- zmiany po t.j.: " + ("brak\n" if not zm else "\n"+"".join(f"  - {z}\n" for z in zm)))
        f.write("\n")
