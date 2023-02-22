# MusicMarket

Suunnitelma:

Sovellus johon käyttäjä voi ladata tekemäänsä musiikkia ja muut käyttäjät voivat ostaa näitä kappaleita.

Toiminnot:
  - Käyttäjä voi luoda tilin ja kirjautua sisään/ulos
  - Käyttäjä voi ladata kappaleitaan sovellukseen
  - Käyttäjä voi ostaa musiikkia ja artisti voi seurata paljonko rahaa on tienannut ja paljonko latauksia on.
  - Musiikkia voi hakea genren/nimen mukaan
  - Kappaleille voi antaa tykkäyksiä/kommentteja

Tällä hetkellä sovelluksessa toimivat kaikki ominaisuudet.
Sovellukseen voi luoda uuden käyttäjän ja kirjautua sillä siään.
Kappaletta haettaessa tulee valita jokin hakukriteeri, jotta haku onnistuu.
Tietokantaan on tallennettu yksi kappale nimellä TheArtist - TheTrack, genrenä rock.
Tällä hetkellä kappaleen ostamisen jälkeen ohjataan käyttäjä etusivulle, tämän tulen vielä muuttamaan.
Kappaleita ladattaessa näkyy alhaalla jo ladatut omat kappaleet, sekä kuinka monen euon edestä kappaleita on ostettu. 
Sovelluksen ulkoasua on muokattu, mutta osa sivuista ei vielä ole uudessa layoutissa.

Sovellus ei ole vielä saatavilla fly.io:ssa, sillä en kerennyt saada sitä toimimaan.

Käynnistysohjeet:

1. Kloonaa repositorio koneellesi
2. Luo kansioon .env tiedosto, jonka sisältö on:<br>
      DATABASE_URL= tietokannan-paikallinen-osoite<br>
      SECRET_KEY=salainen avain<br>

3. Aktivoi virtuaaliympäristö: <br>
      $ python3 -m venv venv<br>
      $ source venv/bin/activate<br>
      $ pip install -r ./requirements.txt<br>
      
4. Määritä tietokannan skeema:<br>
      $ psql < schema.sql
                         
5. Käynnistä sovellus:<br>
      $ flask run


