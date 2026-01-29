# Parking Reservation System

Sistem za rezervaciju parking mjesta razvijen kao akademski projekat u okviru predmeta **Projektovanje Informacionih Sistema**. Aplikacija služi kao simulator koji korisnicima omogućava upravljanje vozilima i rezervacijama, dok administratorima pruža potpunu kontrolu nad infrastrukturom parkinga.

## Pregled Projekta

Aplikacija je bazirana na Flask framework-u i koristi SQLite bazu podataka. Dizajnirana je da simulira realni scenario u kojem korisnici mogu da biraju lokacije, registruju vozila i vrše digitalne rezervacije, dok admin panel omogućava uvid u kompletnu metriku sistema.

### Funkcionalnosti Sistema

* **Autentifikacija i Sigurnost:**
    * Registracija i verifikacija korisnika.
    * Hashing lozinki korišćenjem `pbkdf2:sha256` metode (Werkzeug).
    * Mogućnost promjene lozinke i ažuriranja profila.
* **Korisnički Modul:**
    * Upravljanje vozilima (dodavanje različitih tipova: Automobil, Kamion, Autobus, Motor, Kombi).
    * Dodavanje metoda plaćanja.
    * Rezervacija parking mjesta na specifičnim lokacijama i otkazivanje istih.
* **Administratorski Modul:**
    * Grafički interfejs za CRUD operacije nad svim entitetima.
    * Upravljanje lokacijama (dodavanje GPS koordinata, kapaciteta i fotografija lokacija).
    * Pregled i upravljanje svim korisnicima i njihovim vozilima.
    * Mogućnost imenovanja novih administratora.

## Tehnologije

* **Backend:** Python 3.15, Flask
* **Baza podataka:** SQLite3
* **Sigurnost:** Werkzeug (Security helpers)
* **Kontejnerizacija:** Docker

## Instalacija i Pokretanje

### 1. Native Instalacija (Lokalno)
Za pokretanje je potrebno imati instaliran **Python 3.15** i **pip**.

```bash
# Instalacija neophodnih biblioteka
pip install -r requirements.txt

# Aktivacija virtuelnog okruženja
source venv/bin/activate

# Inicijalizacija baze podataka (samo pri prvom pokretanju)
python3 db_init.py

# Popunjavanje baze inicijalnim podacima (Seed-ovanje)
python3 db_populate.py

# Pokretanje aplikacije
python3 app.py

### 2. Docker Instalacija

Ukoliko preferirate rad sa kontejnerima, aplikacija je dostupna na Docker Hub-u.
Bash

# Preuzimanje slike
docker pull rdj917/public-projects:parking-app_v1.0

# Pokretanje kontejnera
docker run -p 5000:5000 <id-image-a>

Podaci za Pristup (Admin)

Baza je unaprijed popunjena admin nalogom za testiranje sistema:

    Username: admin

    Password: root

    Email: admin@mail.com

Struktura Baze Podataka

Sistem se automatski popunjava podacima koji obuhvataju:

    Korisnici: 30+ generisanih korisnika sa različitim ulogama.

    Vozila: Različite kategorije (Golf 7, BMW X5, MAN kamioni, Vespa motori itd.) sa pripadajućim registarskim oznakama.

    Lokacije: Ključne tačke u Podgorici (Rimski Trg, Delta City, Bazar, TC Palada, City Kej, UDG, itd.) sa definisanim kapacitetima i koordinatama.
