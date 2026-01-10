import sqlite3
from werkzeug.security import generate_password_hash

def seed_database():
    conn = sqlite3.connect('./parking.db')
    cursor = conn.cursor()

    def hash_pw(password):
        return generate_password_hash(password, method='pbkdf2:sha256')

    users_data = [
        # ADMIN 
        (68, 1, 'Glavni', 'Admin', 'admin', 'admin@mail.com', hash_pw('root'), '067000000'),
        (69, 0, 'Nikola', 'Vukovic', 'nikola_v', 'nikola@gmail.com', hash_pw('pass123'), '068123456'),
        (70, 0, 'Jelena', 'Perovic', 'jelena_p', 'jelena@yahoo.com', hash_pw('pass123'), '069222333'),
        (71, 0, 'Milica', 'Radovic', 'milica_r', 'milica@gmail.com', hash_pw('pass123'), '067444555'),
        (72, 0, 'Filip', 'Bojovic', 'filip_b', 'filip@outlook.com', hash_pw('pass123'), '068666777'),
        (73, 0, 'Ana', 'Kovacevic', 'ana_k', 'ana@gmail.com', hash_pw('pass123'), '069111000'),
        (74, 0, 'Petar', 'Draskovic', 'petar_d', 'petar@gmail.com', hash_pw('pass123'), '067888999'),
        (75, 0, 'Ivana', 'Popovic', 'ivana_p', 'ivana@gmail.com', hash_pw('pass123'), '068112233'),
        (76, 0, 'Stefan', 'Lekic', 'stefan_l', 'stefan@gmail.com', hash_pw('pass123'), '069554433'),
        (77, 0, 'Maja', 'Pavicevic', 'maja_p', 'maja@gmail.com', hash_pw('pass123'), '067332211'),
        (78, 0, 'Bojan', 'Ivanovic', 'bojan_i', 'bojan@gmail.com', hash_pw('pass123'), '068998877'),
        (79, 0, 'Sara', 'Vujovic', 'sara_v', 'sara@gmail.com', hash_pw('pass123'), '069776655'),
        (80, 0, 'Luka', 'Nikolic', 'luka_n', 'luka@gmail.com', hash_pw('pass123'), '067223344'),
        (81, 0, 'Anja', 'Markovic', 'anja_m', 'anja@gmail.com', hash_pw('pass123'), '068556677'),
        (82, 0, 'Dragan', 'Zaric', 'dragan_z', 'dragan@gmail.com', hash_pw('pass123'), '069889900'),
        (83, 0, 'Elena', 'Bulatovic', 'elena_b', 'elena@gmail.com', hash_pw('pass123'), '067114477'),
        (84, 0, 'Milos', 'Sekulic', 'milos_s', 'milos@gmail.com', hash_pw('pass123'), '068225588'),
        (85, 0, 'Nina', 'Durovic', 'nina_d', 'nina@gmail.com', hash_pw('pass123'), '069336699'),
        (86, 0, 'Pavle', 'Milovic', 'pavle_m', 'pavle@gmail.com', hash_pw('pass123'), '067447700'),
        (87, 0, 'Teodora', 'Kadic', 'teodora_k', 'teodora@gmail.com', hash_pw('pass123'), '068558811'),
        (88, 0, 'Vuk', 'Ostojic', 'vuk_o', 'vuk@gmail.com', hash_pw('pass123'), '069669922'),
        (89, 0, 'Sofija', 'Micic', 'sofija_m', 'sofija@gmail.com', hash_pw('pass123'), '067770033'),
        (90, 0, 'Andrija', 'Savic', 'andrija_s', 'andrija@gmail.com', hash_pw('pass123'), '068881144'),
        (91, 0, 'Kristina', 'Babic', 'kristina_b', 'kristina@gmail.com', hash_pw('pass123'), '069992255'),
        (92, 0, 'Danilo', 'Gusic', 'danilo_g', 'danilo@gmail.com', hash_pw('pass123'), '067003366'),
        (93, 0, 'Katarina', 'Jovovic', 'katarina_j', 'katarina@gmail.com', hash_pw('pass123'), '068114477'),
        (94, 0, 'Aleksa', 'Vlahovic', 'aleksa_v', 'aleksa@gmail.com', hash_pw('pass123'), '069225588'),
        (95, 0, 'Maša', 'Becic', 'masa_b', 'masa@gmail.com', hash_pw('pass123'), '067336699'),
        (96, 0, 'Ognjen', 'Kljajic', 'ognjen_k', 'ognjen@gmail.com', hash_pw('pass123'), '068447700'),
        (97, 0, 'Tamara', 'Pejovic', 'tamara_p', 'tamara@gmail.com', hash_pw('pass123'), '069558811'),
        (98, 0, 'Igor', 'Simic', 'igor_s', 'igor@gmail.com', hash_pw('pass123'), '067112233')
    ]
    cursor.executemany("INSERT INTO users (user_id, is_admin, first_name, last_name, username, email, password, phone) VALUES (?,?,?,?,?,?,?,?)", users_data)

  
    vehicles_data = [
        (69, 69, 'Automobil', 'VW Golf 7', 'PG-AB123', 'Siva', 2015, 'Hatchback', 1),
        (70, 70, 'Automobil', 'BMW X5', 'PG-X5001', 'Crna', 2019, 'SUV', 1),
        (71, 71, 'Motor', 'Yamaha R1', 'PG-MT001', 'Plava', 2020, 'Sport', 1),
        (72, 72, 'Kombi', 'Mercedes Sprinter', 'PG-KM111', 'Bijela', 2018, 'Transportni', 1),
        (73, 73, 'Kamion', 'MAN TGE', 'PG-TR999', 'Crvena', 2017, 'Sanduk', 1),
        (74, 74, 'Autobus', 'Isuzu Turkuaz', 'PG-BS222', 'Bijela', 2015, 'Mini-bus', 1),
        (75, 75, 'Motor', 'Vespa GTS', 'CT-SC121', 'Crvena', 2021, 'Scooter', 1),
        (76, 76, 'Automobil', 'Skoda Octavia', 'NK-SO001', 'Bijela', 2018, 'Limuzina', 1),
        (77, 77, 'Automobil', 'Audi A3', 'BD-AA555', 'Siva', 2022, 'Hatchback', 1),
        (78, 78, 'Kamion', 'Volvo FH', 'PG-TK888', 'Plava', 2019, 'Cisterna', 1),
        (79, 79, 'Kombi', 'Renault Master', 'TV-RM000', 'Bijela', 2016, 'Panel Van', 1),
        (80, 80, 'Automobil', 'Tesla Model 3', 'UL-EL660', 'Crna', 2021, 'Limuzina', 1),
        (81, 81, 'Motor', 'Harley Davidson', 'BR-HD111', 'Crna', 2013, 'Cruiser', 1),
        (82, 82, 'Autobus', 'Mercedes Citaro', 'PG-GZ606', 'Žuta', 2019, 'Gradski', 1),
        (83, 83, 'Kombi', 'VW Crafter', 'HN-VW123', 'Bijela', 2021, 'Putnički', 1),
        (84, 84, 'Automobil', 'Toyota Corolla', 'PG-TC900', 'Plava', 2020, 'Limuzina', 1),
        (85, 85, 'Motor', 'Ducati Panigale', 'PG-DP080', 'Crvena', 2022, 'Sport', 1),
        (86, 86, 'Automobil', 'Honda Accord', 'PG-HA777', 'Srebrna', 2012, 'Limuzina', 1),
        (87, 87, 'Automobil', 'Nissan Qashqai', 'NK-NQ101', 'Siva', 2018, 'SUV', 1),
        (88, 88, 'Motor', 'BMW GS 1250', 'PG-BM202', 'Bijela', 2021, 'Touring', 1),
        (89, 89, 'Automobil', 'Alfa Romeo Giulia', 'PG-AR159', 'Crvena', 2018, 'Sport', 1),
        (90, 90, 'Kamion', 'Scania R450', 'PG-SC100', 'Zelena', 2020, 'Kontejnerski', 1),
        (91, 91, 'Automobil', 'Seat Leon', 'PG-SL555', 'Crna', 2019, 'Hatchback', 1),
        (92, 92, 'Automobil', 'Mercedes E Class', 'PG-ME220', 'Bijela', 2020, 'Limuzina', 1),
        (93, 93, 'Automobil', 'Dacia Duster', 'CT-DD001', 'Narandžasta', 2021, 'SUV', 1),
        (94, 94, 'Automobil', 'BMW 320d', 'PG-B3200', 'Siva', 2014, 'Limuzina', 1),
        (95, 95, 'Automobil', 'Jeep Compass', 'PG-JC707', 'Crna', 2022, 'SUV', 1),
        (96, 96, 'Automobil', 'Citroen C3', 'PG-CC333', 'Bijela', 2019, 'Hatchback', 1),
        (97, 97, 'Automobil', 'Skoda Superb', 'PG-SS111', 'Teget', 2021, 'Limuzina', 1),
        (98, 98, 'Kombi', 'Ford Transit', 'PG-FT222', 'Siva', 2019, 'Pick-up', 1)
    ]
    cursor.executemany("INSERT INTO vehicles (car_id, user_id, vehicle_type, vehicle_production_mark, vehicle_licence_plate, vehicle_color, vehicle_year_of_production, vehicle_body_type, is_registered) VALUES (?,?,?,?,?,?,?,?,?)", vehicles_data)

   
    locations_data = [
        (69, 'Trg Nezavisnosti', '42.4411, 19.2625', 45, 5, 'https://upload.wikimedia.org/wikipedia/commons/2/2c/Podgorica_Main_Square.jpg'),
        (70, 'Rimski Trg', '42.4418, 19.2461', 20, 10, 'https://upload.wikimedia.org/wikipedia/commons/4/42/Rimski_Trg_Podgorica.jpg'),
        (71, 'Delta City', '42.4385, 19.2340', 80, 20, 'https://investitor.me/wp-content/uploads/2018/02/delta-city-podgorica.jpg'),
        (72, 'Bazar - Blok 5', '42.4485, 19.2410', 38, 2, 'https://podgorica.me/storage/1922/5c332c96c56f9_Bazar1.jpg'),
        (73, 'TC Panonka', '42.4221, 19.2510', 25, 0, 'https://shampitica.me/wp-content/uploads/2019/12/TC-Panonka.jpg'),
        (74, 'Voli - Stari Aerodrom', '42.4350, 19.2810', 55, 5, 'https://www.standard.co.me/wp-content/uploads/2019/11/Voli-Stari-Aerodrom.jpg'),
        (75, 'Gradski Stadion', '42.4460, 19.2660', 30, 15, 'https://upload.wikimedia.org/wikipedia/commons/e/e0/Podgorica_City_Stadium.jpg'),
        (76, 'Mall of Montenegro', '42.4310, 19.2610', 58, 12, 'https://upload.wikimedia.org/wikipedia/commons/0/04/Mall_of_Montenegro_Podgorica.jpg'),
        (77, 'TC Palada', '42.4480, 19.2550', 15, 5, 'https://m.pobjeda.me/storage/2020/05/18/10/37/102061_0.jpg'),
        (78, 'City Kej', '42.4600, 19.2650', 49, 6, 'https://celebic.com/wp-content/uploads/2017/10/City-Kej-naslovna.jpg'),
        (79, 'Univerzitet DG', '42.4180, 19.2100', 90, 10, 'https://upload.wikimedia.org/wikipedia/commons/9/91/UDG_Podgorica.jpg'),
        (80, 'Blok 9', '42.4520, 19.2350', 27, 8, 'https://foursquare.com/img/categories_v2/parks_outdoors/neighborhood_64.png'),
        (81, 'Dom Zdravlja Konik', '42.4380, 19.2950', 29, 1, 'https://www.dzpg.me/wp-content/uploads/2015/05/konik.jpg'),
        (82, 'Trim staza Tološi', '42.4560, 19.2250', 23, 2, 'https://podgorica.me/storage/2458/60ae14b9868f0_trimstaza.jpg'),
        (83, 'Stadion FK Kom', '42.4680, 19.2950', 45, 0, 'https://cg-fudbal.com/wp-content/uploads/2017/08/kom-stadion.jpg')
    ]
    cursor.executemany("INSERT INTO locations (location_id, location_name, location_coordinates, free_locations, used_location, soon_available_place) VALUES (?,?,?,?,?,?)", locations_data)

  
    payments_data = []
    for i in range(30):
        uid = 69 + i
        pid = 69 + i
        method = '1' if i % 2 == 0 else '2'
        payments_data.append((pid, uid, method, users_data[i+1][2], users_data[i+1][3], 'Podgorica Adresa ' + str(i), users_data[i+1][2] + ' ' + users_data[i+1][3], '4532XXXXXXXX' + str(1000+i), '12/26'))
    
    cursor.executemany("INSERT INTO payments (payment_id, user_id, payment_method, payment_first_name, payment_last_name, billing_address_1, card_holder_name, card_number, exp_date) VALUES (?,?,?,?,?,?,?,?,?)", payments_data)

    
    reservations_data = []
    for i in range(25):
        rid = 69 + i
        uid = 69 + i
        vid = 69 + i
        lid = 69 + (i % 15)
        reservations_data.append((rid, uid, lid, vid, rid, 'P' + str(i), '60', '2025-01-10 10:00', '2025-01-10 11:00'))

    cursor.executemany("INSERT INTO reservations (reservation_id, user_id, location_id, vehicle_id, payment_id, reserved_location, reservation_time_period, reservation_begin_date, reservation_exp_date) VALUES (?,?,?,?,?,?,?,?,?)", reservations_data)

    conn.commit()
    conn.close()
    print("Database popunjen!")

if __name__ == "__main__":
    seed_database()