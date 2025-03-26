django-lume
===========

Django-tuki muiden kenttien mukaan tietokannassa laskettaville lume- eli näennäiskentille

# Asennus

```bash
$ pip install django-lume
```

Yhteensopivuus:
* Python >= 3.6
* Django >= 3.1

# Käyttö

Moduuli `lume` sisältää vastineet kaikille `django.db.models`-moduulin määrittämille kenttätyypeille, esim. `lume.DecimalField`, `lume.ForeignKey`. Kunkin kenttätyypin vaatimat pakolliset sekä halutut valinnaiset parametrit (esim. `verbose_name`, `max_length`) annetaan normaalisti kentän luonnin yhteydessä. Lisäksi lumekenttä ottaa omat (nimetyt) parametrinsä:
- `kysely` (pakollinen): kysely, jonka mukaan kentän arvo haetaan
- `automaattinen` (oletus: `False`): otetaanko kenttä oletuksena mukaan kaikkiin tähän tauluun kohdistuviin tietokantahakuihin
- `laske` (oletus: erillinen haku kannasta): funktio, jonka mukaan kentän arvo lasketaan silloin, kun sitä ei haeta alkuperäisen kyselyn mukana
- `aseta` (oletus: nostaa poikkeuksen): funktio, jota kutsutaan, kun kenttään sijoitetaan arvo kutsuvasta koodista

Esimerkki (`mallit.py`):
```python
from django.db import models
import lume

class Malli(models.Model):
  ...
  # Pylint saattaa valittaa puuttuvasta `DecimalField`-luokasta,
  # koska `lume`-moduulin kenttäkohtaiset luokat luodaan ajonaikaisesti.
  # Kierretään tämä käyttämällä 'no-member'-lippua.

  numerokentta = lume.DecimalField( # pylint: disable=no-member
    max_digits=5, # kenttätyypin vaatimat parametrit
    decimal_places=2,
    ...
    kysely=models.Sum('toinen_malli__summa'), # arvon laskenta
    automaattinen=True, # kenttä lisätään kyselyihin automaattisesti
  )
  viittauskentta = lume.ForeignKey( # pylint: disable=no-member
    # Käytetään sulkeumaa kyselyn palauttamiseen silloin,
    # kun suora argumentti vaatisi kehämäisen python-tuonnin.
    kysely=lambda: models.Subquery(
      ToinenMalli.objects.filter(
        viittaus=models.OuterRef('pk')
      ).annotate(
        ...
      ).order_by(...).values('pk')[:1],
      output_field=models.IntegerField(),
    ),
    # Kenttä lisätään kyselyihin vain pyydettäessä (.lume('viittauskentta')).
    automaattinen=False,
    # Paikallinen laskentafunktio, käytetään tarvittaessa.
    laske=lambda self: self.viittaukset.order_by(...).first(),
  )
  ...
```

Automaattisiksi määritetyt näennäiskentät lisätään oletuksena kaikkiin kyselyihin. Lisäksi kutsumalla `QuerySet`-luokan metodia `lume('kenttä1', 'kenttä2', ...)` voidaan lisätä kyselykohtaisia lumekenttiä mukaan kyselyyn. Metodikutsut kasaantuvat, joten `qs.lume('k1', 'k2') == qs.lume('k1')....lume('k2')`.

Kutsu `lume(None)` poistaa kaikki aiemmin pyydetyt lumekentät kyselystä. Automaattisiksi määritellyt kentät lisätään tällöinkin kyselyyn.

Kyselyyn mukaan otettavat tai siitä pois jätettävät lumekentät voidaan määrittää myös tavanomaisten `only()`- ja `defer()`-kutsujen avulla. Tämä ohittaa lumekenttien `automaattinen`-määritykset.


## Kentän laskenta ja asettaminen

Kullekin kentälle voidaan määrittää `laske(rivi)`-funktio, jonka avulla sen arvo lasketaan sitä kysyttäessä silloin, kun kenttä ei ollut mukana tietokantakyselyssä. Oletuksena kentän arvo kysytään tällöin erikseen kannasta.

Lisäksi voidaan määrittää `aseta(rivi, arvo)`-funktio, jota kutsutaan silloin, kun kenttään sijoitetaan arvo tietokantahaun jälkeen. Mikäli funktiota ei ole määritetty, arvon sijoittaminen aiheuttaa poikkeuksen.


## Puutteet ja ongelmat

Lumekentän laskenta `OuterRef`-viittauksen takaa ei toistaiseksi toimi. Tällaisessa tilanteessa ei pystytä päättelemään sitä SQL-aliasta, jonka viittaamasta taulusta lumekentän kyselyssä viitatut sarakkeet haettaisiin. Esimerkki tällaisesta kyselystä: ks. yksikkötestit.
