# MusicMarket

Suunnitelma:

Sovellus johon käyttäjä voi ladata tekemäänsä musiikkia ja muut käyttäjät voivat ostaa näitä kappaleita.

Toiminnot:
  - Käyttäjä voi luoda tilin ja kirjautua sisään/ulos
  - Käyttäjä voi ladata kappaleitaan sovellukseen
  - Käyttäjä voi ostaa musiikkia ja artisti voi seurata paljonko rahaa on tienannut ja paljonko latauksia on.
  - Musiikkia voi hakea genren/nimen mukaan
  - Kappaleille voi antaa tykkäyksiä/kommentteja

Tällä hetkellä sovelluksessa toimivat muut ominaisuudet paitsi tykkäys/kommentointi.
Sovellukseen voi luoda uuden käyttäjän ja kirjautua sillä siään.
Kappaletta haettaessa tulee valita jokin hakukriteeri, jotta haku onnistuu.
Tietokantaan on tallennettu yksi kappale nimellä TheArtist - TheTrack, genrenä rock.
Tällä hetkellä kappaleen ostamisen jälkeen ohjataan käyttäjä etusivulle, tämän tulen vielä muuttamaan.
Kappaleita ladattaessa näkyy alhaalla jo ladatut omat kappaleet, sekä kuinka monen euon edestä kappaleita on ostettu. 

Sovellus ei ole vielä saatavilla fly.io:ssa, sillä en kerennyt saada sitä toimimaan.

Käyynistysohjeet:

1. Kloonaa repositorio koneellesi
2. Luo kansioon .env tiedosto, jonka sisältö on:
      DATABASE_URL= <tietokannan-paikallinen-osoite>
      SECRET_KEY=<salainen avain>

3. Aktivoi virtuaaliympäristö: 
      $ python3 -m venv venv
      $ source venv/bin/activate
      $ pip install -r ./requirements.txt
      
4. Määritä tietokannan skeema:
      $ psql < schema.sql
                         
5. Käynnistä sovellus:
      $ flask run


