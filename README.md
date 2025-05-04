# SoundHeaven

tikawe-kurssia varten tuotettu SoundCloud kopio.

Sovelluksen tämänhetkiset toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen kappaleita. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään kappaleita.
* Jokaiseen kappaleeseen pystyy lisäämään nimen, tekstikuvauksen, kuvan, äänitiedoston sekä maksimissaan 5 tagia.
* Käyttäjä näkee sovellukseen lisätyt kappaleet. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät kappaleet.
* Käyttäjä pystyy etsimään kappaleita hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä kappaleita.
* Jokaisella käyttäjällä on omat käyttäjäsivut, josta näkee käyttäjän lisäämät kappaleet.
* Jokaiselle käyttäjälle pystyy asettamaan profiilikuvan.
* Kappaleisiin pystyy lisäämään kommentteja, ja omia kommentteja pystyy poistamaan.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut:

```
$ sqlite3 database.db < schema.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```

## Sovelluksen suorituskyky suurella tietomäärällä

Ajamalla tiedosto ```seed.py``` tietokanta täytetään 1000 käyttäjällä ja 100 000 kappaleella. Jokaiseen kappaleeseen lisätään äänitiedosto sekä kuva.

Tämän lisäksi kappaleeseen track1 lisätään 1 000 000 kommenttia. 

Suurin apu suorituskykyyn saatiin sivutuksen avulla. Indeksoinnin lisääminen taas ei tuottanut mitattavaa suorituskyvyn paranemista. 

## Hyödynnetyt materiaalit

* normalize.css v8.0.1 | https://github.com/necolas/normalize.css

* Search.svg | https://fonts.google.com/icons?selected=Material+Symbols+Outlined:search:FILL@0;wght@400;GRAD@0;opsz@24&icon.size=24&icon.color=%231f1f1f

* Default pfp.jpg | https://commons.wikimedia.org/wiki/File:Default_pfp.jpg

* Montserrat | https://fonts.google.com/specimen/Montserrat

* test_files/image.png | https://commons.wikimedia.org/wiki/File:Grand_piano_and_upright_piano.jpg