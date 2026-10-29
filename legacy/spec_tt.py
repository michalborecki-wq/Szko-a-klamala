import json
S="<div class='tx' style='font-size:34px;color:#9AA3B5;margin-top:36px'>%s</div>"
def L(t): return f"<div class='lbl'>SZKOŁA KŁAMAŁA · {t}</div>"
def rows(items, mx):
    return "<div class='chart'>"+"".join(f"<div class='row' style='font-size:42px'><span class='k' style='width:330px'>{k}</span><span class='v' style='width:{int(380*v/mx)}px'></span><span class='n'>{n}</span></div>" for k,v,n in items)+"</div>"
P=[
("t01_technologia_sms","TECHNOLOGIA",[
L("TECHNOLOGIA")+"<h1>Pierwszego SMS-a<span class='y'>nie wysłał telefon</span></h1><div class='ul'></div><div class='sub'>I miał tylko dwa słowa.</div>",
"<div class='big'>1992</div><h2 style='margin-top:30px'>3 <span class='y'>grudnia</span></h2><div class='tx'>22-letni inżynier Neil Papworth wysłał wiadomość <b>z komputera</b> na telefon dyrektora Vodafone.</div>",
"<h2>Treść? <span class='y'>„Merry Christmas”</span></h2><div class='tx'>Odbiorca, Richard Jarvis, był akurat na firmowej imprezie świątecznej.</div>",
"<h2>Pamiętasz swój <span class='y'>pierwszy SMS?</span></h2><div class='ul'></div><div class='sub'>Do kogo był i co w nim napisałeś?</div>"+S%"Źródło: History.com"]),
("t02_matematyka_urodziny","MATEMATYKA",[
L("MATEMATYKA")+"<h1>Wystarczą 23 osoby,<span class='y'>by wygrać zakład</span></h1><div class='ul'></div><div class='sub'>Chodzi o wspólne urodziny. Intuicja podpowiada co innego.</div>",
"<div class='big'>50,7%</div><div class='tx' style='margin-top:30px'>Tyle wynosi szansa, że wśród <b>23 osób</b> dwie mają urodziny tego samego dnia.</div>",
"<h2>Im więcej <span class='y'>osób…</span></h2>"+rows([("23 osoby",50.7,"50,7%"),("30 osób",70.6,"70,6%"),("50 osób",97,"97%"),("70 osób",99.9,"99,9%")],100)+"<div class='tx' style='margin-top:30px'>Liczy się każda <b>para</b> – przy 23 osobach par jest aż 253.</div>",
"<h2>Sprawdź w klasie <span class='y'>albo w pracy</span></h2><div class='ul'></div><div class='sub'>Ile osób potrzebowałeś, żeby trafić parę?</div>"+S%"Obliczenia własne (rok 365 dni, każdy dzień równie prawdopodobny)"]),
("t03_biologia_osmiornica","BIOLOGIA",[
L("BIOLOGIA")+"<h1>Ośmiornica ma<span class='y'>trzy serca</span></h1><div class='ul'></div><div class='sub'>I niebieską krew.</div>",
"<h2>Dwa + <span class='y'>jedno</span></h2><div class='tx'>Dwa serca pompują krew przez <b>skrzela</b>. Trzecie rozsyła natlenioną krew do narządów i mięśni.</div>",
"<h2>Pływanie <span class='y'>męczy</span></h2><div class='tx'>Gdy ośmiornica płynie, trzecie serce <b>przestaje bić</b>. Dlatego woli pełzać po dnie.</div>",
"<h2>Skąd niebieska <span class='y'>krew?</span></h2><div class='tx'>Zamiast żelaza tlen przenosi białko z <b>miedzią</b> – hemocyjanina.</div><div class='sub' style='margin-top:40px'>Znasz dziwniejsze zwierzę?</div>"+S%"Źródło: Smithsonian Magazine"]),
("t04_fizyka_piorko","FIZYKA",[
L("FIZYKA")+"<h1>Młotek i piórko<span class='y'>spadają razem</span></h1><div class='ul'></div><div class='sub'>Na Księżycu ktoś to naprawdę sprawdził.</div>",
"<div class='big'>1971</div><h2 style='margin-top:30px'>Apollo <span class='y'>15</span></h2><div class='tx'>Dowódca David Scott upuścił jednocześnie <b>młotek 1,32 kg</b> i <b>sokole pióro 0,03 kg</b>.</div>",
"<h2>Wynik?</h2><div class='tx'>Uderzyły w grunt <b>w tej samej chwili</b>. Bez powietrza nic nie hamuje piórka – oba spadają z tym samym przyspieszeniem.</div>",
"<h2>Galileusz <span class='y'>miał rację</span></h2><div class='ul'></div><div class='sub'>Doszedł do tego kilkaset lat wcześniej – bez rakiety.</div>"+S%"Źródło: NASA"]),
("t05_psychologia_mozg","PSYCHOLOGIA",[
L("PSYCHOLOGIA")+"<h1>Używasz tylko 10% mózgu?<span class='y'>Nie.</span></h1><div class='ul'></div><div class='sub'>To jeden z najtrwalszych mitów o człowieku.</div>",
"<h2>Pracuje <span class='y'>prawie cały</span></h2><div class='tx'>Badania obrazowe pokazują, że w ciągu dnia działają <b>praktycznie wszystkie</b> obszary mózgu – nawet podczas snu.</div>",
"<div class='big'>20%</div><h2 style='margin-top:30px'>energii <span class='y'>ciała</span></h2><div class='tx'>Mózg to ok. <b>3%</b> masy ciała, a zużywa ok. <b>20%</b> energii.</div>",
"<h2>Skąd znasz <span class='y'>ten mit?</span></h2><div class='ul'></div><div class='sub'>Z filmu, z reklamy, czy z lekcji?</div>"+S%"Źródło: Scientific American"]),
("t06_jezykpolski_robot","JĘZYK POLSKI",[
L("JĘZYK POLSKI")+"<h1>Słowo „robot”<span class='y'>jest słowiańskie</span></h1><div class='ul'></div><div class='sub'>A wymyślił je brat pisarza.</div>",
"<div class='big'>1920</div><h2 style='margin-top:30px'>Sztuka <span class='y'>R.U.R.</span></h2><div class='tx'>Czeski pisarz Karel Čapek pokazał w niej sztucznych robotników. Najpierw chciał ich nazwać <b>„labori”</b>.</div>",
"<h2>Brat miał <span class='y'>lepszy pomysł</span></h2><div class='tx'>Josef Čapek podsunął <b>„roboti”</b> – od słowa <b>robota</b>, czyli przymusowa praca, pańszczyzna.</div>",
"<h2>Słowiańska „robota” <span class='y'>zrobiła karierę</span></h2><div class='ul'></div><div class='sub'>Znasz inne polskie słowo, które ruszyło w świat?</div>"+S%"Źródło: Science Friday"]),
("t07_finanse_regula72","FINANSE",[
L("FINANSE")+"<h1>Reguła 72,<span class='y'>której nie było na lekcji</span></h1><div class='ul'></div><div class='sub'>Jeden podział pokazuje, jak działa procent składany.</div>",
"<div class='big'>72 : %</div><div class='tx' style='margin-top:30px'>Podziel <b>72</b> przez roczną stopę procentową. Wynik to przybliżona liczba lat, po której kwota się <b>podwaja</b>.</div>",
"<h2>Sprawdzamy</h2>"+rows([("4% rocznie",18,"18 lat"),("6% rocznie",12,"12 lat"),("8% rocznie",9,"9 lat")],18)+"<div class='tx' style='margin-top:30px'>Dokładnie: 17,7 · 11,9 · 9,0 roku.</div>",
"<h2>Działa też <span class='y'>dla inflacji</span></h2><div class='tx'>Przy inflacji 6% rocznie ceny podwoiłyby się po ok. 12 latach.</div>"+S%"Obliczenia własne. To nie jest porada inwestycyjna."]),
("t08_historia_kleopatra","HISTORIA",[
L("HISTORIA")+"<h1>Kleopatra żyła bliżej nas<span class='y'>niż budowy piramid</span></h1><div class='ul'></div><div class='sub'>Brzmi absurdalnie? Policzmy.</div>",
"<h2>Daty</h2><div class='tx'>Wielką Piramidę w Gizie ukończono na początku <b>XXV w. p.n.e.</b> Kleopatra urodziła się ok. <b>70 r. p.n.e.</b></div>",
"<h2>Różnica</h2>"+rows([("Piramida → Kleopatra",2420,"2400+ lat"),("Kleopatra → dziś",2095,"ok. 2095 lat")],2420),
"<h2>Dla Kleopatry piramidy <span class='y'>były zabytkiem</span></h2><div class='ul'></div><div class='sub'>Jaki inny fakt tak samo „psuje” Ci oś czasu?</div>"+S%"Źródło: Encyclopaedia Britannica; obliczenia własne"]),
("t09_geografia_strefy","GEOGRAFIA",[
L("GEOGRAFIA")+"<h1>Najwięcej stref czasowych<span class='y'>nie ma Rosja</span></h1><div class='ul'></div><div class='sub'>Ani USA.</div>",
"<div class='big'>12</div><h2 style='margin-top:30px'>Francja</h2><div class='tx'>Kontynentalna Francja ma jedną strefę. Pozostałe <b>11</b> to terytoria zamorskie.</div>",
"<h2>Ranking</h2>"+rows([("Francja",12,"12"),("Rosja",11,"11"),("USA",11,"11")],12),
"<h2>Wszystko <span class='y'>przez wyspy</span></h2><div class='tx'>Polinezja, Gujana Francuska, wyspy na trzech oceanach i kawałek Antarktydy.</div>"+S%"Źródło: timeanddate.com"]),
("t10_kosmos_wenus","KOSMOS",[
L("KOSMOS")+"<h1>Na Wenus dzień trwa dłużej<span class='y'>niż rok</span></h1><div class='ul'></div><div class='sub'>To nie literówka.</div>",
"<h2>Liczby</h2>"+rows([("Obrót wokół osi",243,"243 dni"),("Okrążenie Słońca",225,"225 dni")],243)+"<div class='tx' style='margin-top:30px'>W dniach ziemskich.</div>",
"<h2>Słońce wschodzi <span class='y'>na zachodzie</span></h2><div class='tx'>Wenus obraca się <b>w przeciwną stronę</b> niż Ziemia i większość planet.</div>",
"<h2>Wschód Słońca <span class='y'>co ok. 117 dni</span></h2><div class='ul'></div><div class='sub'>Wytrzymałbyś taką noc?</div>"+S%"Źródło: NASA Space Place"]),
("t11_ekonomia_monety","EKONOMIA",[
L("EKONOMIA")+"<h1>Pierwsze monety<span class='y'>nie były ze złota</span></h1><div class='ul'></div><div class='sub'>Ani ze srebra. Z czegoś pomiędzy.</div>",
"<h2>Lidia, <span class='y'>ok. 650 r. p.n.e.</span></h2><div class='tx'>Pierwsze prawdziwe monety bito w <b>Lidii</b> w Azji Mniejszej – na terenie dzisiejszej Turcji.</div>",
"<h2>Elektrum</h2><div class='tx'>Naturalny <b>stop złota i srebra</b>. Grecy nazywali go „białym złotem”. Wartość zależała od proporcji metali.</div>",
"<h2>Co było pieniądzem <span class='y'>przed monetami?</span></h2><div class='ul'></div><div class='sub'>Strzelaj w komentarzu.</div>"+S%"Źródło: Encyclopaedia Britannica"]),
]
json.dump([{"id":i,"kind":"tt","label":l,"slides":s} for i,l,s in P],open("spec_tt.json","w"),ensure_ascii=False)
