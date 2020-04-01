# Scraper
Sťahovanie a vypisovanie dát z portálu sector.sk

## Návod
Clone repository - skúšal som primárne v pyCharm

### Sťahovanie a ukladanie dát 
```
... cd Scraper
```
Vo virtual enviroment (venv) v záložke Scraper spustite príkaz
```
scrapy crawl sectorsk -a pages=0
```
V základe sa sťahuje a ukladá prvá stránka na sector.sk. Každá stránka máva 30 článkov.
Atribút **pages** určuje koľko stránok navyše chcete stiahnuť (pages=0 - iba prvá úvodná).
Čiže ak chcete napríklad stiahnuť dve stránky navyše(30+60) do atribútu **pages** zadáte 2.
```
scrapy crawl sectorsk -a pages=2
```


### Výpis a zoradzovanie dát v tabuľke 
```
cd.. -> cd Flask_api
```
Vo virtual enviroment (venv) v záložke Flask_api spustite príkaz
```
flask run
```
Na local hoste (127.0.0.1:5000) sa spustí jednoduchá stránka s tabuľkou dát uložených na mongoDB.
Ak by ste chceli skontrolovať, alebo mazať dáta na mongoDB zašlem aj prihlasovacie údaje.


### Použil som
*[Scrapy](https://scrapy.org/)
*[Flask](https://flask.palletsprojects.com/en/1.1.x/)
*[Flask-Pymongo](https://flask-pymongo.readthedocs.io/en/latest/)
*[MongoDB](https://www.mongodb.com/)
