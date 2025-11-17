# ohtu-miniprojekti

Kanban board: https://trello.com/b/iLiKi0vL 

[![CI](https://github.com/macabre-cs/ohtu-miniprojekti/actions/workflows/ci.yaml/badge.svg)](https://github.com/macabre-cs/ohtu-miniprojekti/actions/workflows/ci.yaml)

## Sovelluksen asennus

#### 1. Kopioi Git-projekti omalle koneellesi
```
$ git clone git@github.com:macabre-cs/ohtu-miniprojekti.git 
```
#### 2. Tietokanta
Sovellus tarvitsee PostgreSQL-tietokannan. Käytä esim. pilvipalveluna tarjottavaa tietokantaa https://aiven.io.

Luo projektikansion juureen tiedosto `.env` ja kopioi sinne alla olevat tiedot.
```
DATABASE_URL=postgresql://xxxx
TEST_ENV=true
SECRET_KEY=kirjoita_secret_key_tähän
```
Lisää kohtaan `DATABASE_URL`linkki tietokantaan ja luo salainen avain kohtaan `SECRET_KEY`

#### 3. Asenna poetry
```
$ poetry install
```
#### 4. Siirry virtuaaliympäristöön
```
$ eval $(poetry env activate) 
```
#### 5. Käynnistä sovellus
```
$ python3 src/index.py
```
