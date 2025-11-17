## Projekt: Elections Scraper ##
Třetí projekt na kurzu od Engeto - Datový analytik s Pythonem.

### Popis projektu ###
Tento projekt slouží k extrahování výsledků parlamentních voleb v roce 2017. Odkaz k prohlédnutí naleznete [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

### Instalace knihoven ###
Knihovny, které jsou použity v kódu jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:

> $ pip 3 --version	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # overim verzi manazeru  
> $ pip 3 install -r requirements.txt &nbsp;&nbsp;&nbsp;&nbsp; # nainstaluji knihovnu

### Spuštění projektu ###
Spuštění souboru main.py v rámci příkazového řádku požaduje dva povinné argumenty.

> `python main.py <odkaz-uzemniho-celku> <vysledny-soubor>`

Následně se stáhnou výsledky jako soubor s příponou .csv.

### Ukázka projektu ###
Výsledky hlasování pro okres Benešov:

1. argument: `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101`
2. argument: `vysledky_benesov.csv`

Spuštění programu:

> python main.py `"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101"` `"vysledky_benesov.csv"`

Průběh stahování:

> Zpracovávám: 529303  
> Zpracovávám: 532568  
> Zpracovávám: 530743  
> …  
> Hotovo! Výsledky uloženy do vysledky_benesov.csv

Částečný výstup:

> code,location,registered,envelopes,valid,...  
> 529303,Benešov,13104,8476,8437,1052,10,2,624,3,802,597,109,35,112,6,11,948,3,6,414,2577,3,21,314,5,58,17,16,682,10  
> 532568,Bernartice,191,148,148,4,0,0,17,0,6,7,1,4,0,0,0,7,0,0,3,39,0,0,37,0,3,0,0,20,0  
> 530743,Bílkovice,170,121,118,7,0,0,15,0,8,18,0,2,0,0,0,3,0,0,2,47,1,0,6,0,0,0,0,9,0  
> … 

