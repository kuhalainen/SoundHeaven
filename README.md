# SoundHeaven

tikawe-kurssia varten tuotettu SoundCloud kopio.

Sovelluksen tämänhetkiset toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen kappaleita. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään kappaleita.
* Jokaiseen kappaleeseen pystyy lisäämään nimen ja tekstikuvauksen ja maksimissaan 5 tagia.
* Käyttäjä näkee sovellukseen lisätyt kappaleet. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät kappaleet.
* Käyttäjä pystyy etsimään kappaleita hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä kappaleita.
* Jokaisella käyttäjällä on omat käyttäjäsivut, josta näkee käyttäjän lisäämät kappaleet.


     
Sovelluksesta puuttuvat toiminnot

* Kuvan ja äänitiedoston lisääminen kappaleisiin.
* Käyttäjäsivuille jonkinlaista tilastoa käyttäjästä.
* Kappaleiden lisääminen soittolistoihin

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
