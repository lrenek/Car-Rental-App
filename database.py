import sqlite3

#connect to database or create a new one
conn = sqlite3.connect('car-rental-python-database.db')

#create a cursor
c= conn.cursor()

#create the tables

#client table
c.execute(""" CREATE TABLE client
(   afm INTEGER NOT NULL,
    fname TEXT,
    lname TEXT,
    driv_licence INTEGER NOT NULL,
    email VARCHAR(319) NOT NULL,
    phone_number INTEGER,
    location_name TEXT,
    location_number INTEGER,
    PRIMARY KEY(afm)
)
""")

#reservation table
c.execute(""" CREATE TABLE reservation
(   reservation_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    reservation_date DATE NOT NULL,
    free_can_period DATE,
    cancellation_date DATE,
    pickup_date DATE NOT NULL,
    return_date DATE NOT NULL,
    returned_date DATE,
    damages DECIMAL DEFAULT 0,
    total_cost DECIMAL, 
    ins_id INTEGER NOT NULL,
    cat_id INTEGER NOT NULL,
    c_id VARCHAR NOT NULL,
    pul_id INTEGER NOT NULL,
    dol_id INTEGER NOT NULL,
    PRIMARY KEY(reservation_id),
    FOREIGN KEY(client_id) REFERENCES client(afm),
    FOREIGN KEY(ins_id) REFERENCES insurance(insurance_id),
    FOREIGN KEY(cat_id) REFERENCES category(category_id),
    FOREIGN KEY(c_id) REFERENCES car(car_id),
    FOREIGN KEY(pul_id)REFERENCES location(location_id),
    FOREIGN KEY(dol_id)REFERENCES location(location_id)
)
""")

#payment table
c.execute(""" CREATE TABLE payment
(   payment_id INTEGER NOT NULL,
    r_id INTEGER NOT NULL,
    card_number INTEGER NOT NULL,
    card_exp_date TEXT NOT NULL,
    card_cvv INTEGER NOT NULL,
    PRIMARY KEY(payment_id),
    FOREIGN KEY(r_id) REFERENCES reservation(reservation_id)
)
""")

#category table
c.execute(""" CREATE TABLE category
(   category_id INTEGER NOT NULL,
    size TEXT NOT NULL,
    seat_number INTEGER NOT NULL,
    door_number INTEGER NOT NULL,
    transmission TEXT,
    cost_per_day DECIMAL NOT NULL,
    PRIMARY KEY(category_id)
)
""")

#car table
c.execute(""" CREATE TABLE car
(   car_id VARCHAR(8) NOT NULL,
    cat_id INTEGER NOT NULL,
    l_id INTEGER NOT NULL, 
    model VARCHAR,
    PRIMARY KEY(car_id),
    FOREIGN KEY(cat_id) REFERENCES category(category_id),
    FOREIGN KEY(l_id) REFERENCES location(location_id)
)
""")

#location table
c.execute(""" CREATE TABLE location
(   location_id INTEGER NOT NULL,
    lname TEXT,
    PRIMARY KEY(location_id)
)
""")

#evaluation table
c.execute(""" CREATE TABLE evaluation
(   rating_id INTEGER NOT NULL,
    r_id INTEGER NOT NULL,
    rating INTEGER,
    comments TEXT,
    PRIMARY KEY(rating_id),
    FOREIGN KEY(r_id) REFERENCES reservation(reservation_id)
)
""")

#contains table
c.execute(""" CREATE TABLE contains
(   r_id INTEGER NOT NULL,
    s_id INTEGER NOT NULL,
    PRIMARY KEY(r_id,s_id),
    FOREIGN KEY(r_id) REFERENCES reservation(reservation_id),
    FOREIGN KEY(s_id) REFERENCES services(services_id)    
)
""")

#services table
c.execute(""" CREATE TABLE services
(   services_id INTEGER NOT NULL,
    sname TEXT,
    cost DECIMAL NOT NULL,
    PRIMARY KEY(services_id)
)
""")

#insurance table
c.execute(""" CREATE TABLE insurance
(   insurance_id INTEGER NOT NULL,
    iname TEXT,
    cost DECIMAL NOT NULL,
    PRIMARY KEY(insurance_id)
)
""")

#insert data into database

#cars
c.execute("INSERT OR IGNORE INTO car VALUES('AEA2355','2','1','Hyundai Santa Fe')")
c.execute("INSERT OR IGNORE INTO car VALUES('BHI2139','2','2','2012 Nissan Frontier S')")
c.execute("INSERT OR IGNORE INTO car VALUES('NMB4728','2','1','BMW 4 Series 435Xi')")
c.execute("INSERT OR IGNORE INTO car VALUES('KTP8718','1','3','Toyota Corolla')")
c.execute("INSERT OR IGNORE INTO car VALUES('ATB6368','1','2','Toyota Camry Dlx')")
c.execute("INSERT OR IGNORE INTO car VALUES('KBB6261','1','5','Toyota Yaris')")
c.execute("INSERT OR IGNORE INTO car VALUES('YNH2184','2','5','Ford Focus')")
c.execute("INSERT OR IGNORE INTO car VALUES('KOM1243','3','3','Ford Escape')")
c.execute("INSERT OR IGNORE INTO car VALUES('AXT9122','1','2','Toyota Yaris')")
c.execute("INSERT OR IGNORE INTO car VALUES('AAN2955','1','4','Toyota Yaris')")
c.execute("INSERT OR IGNORE INTO car VALUES('ZAZ1232','1','1','Nissan Micra')")
c.execute("INSERT OR IGNORE INTO car VALUES('KKT9121','1','5','Nissan Micra')")
c.execute("INSERT OR IGNORE INTO car VALUES('ANP7759','2','2','VW Passat')")
c.execute("INSERT OR IGNORE INTO car VALUES('OIT2388','2','2','VW Touareg')")
c.execute("INSERT OR IGNORE INTO car VALUES('KKA7623','2','4','Lexus ES')")
c.execute("INSERT OR IGNORE INTO car VALUES('ABN3212','3','4','Subaru Forester')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΥΑΑ2161','2','6','Toyota Prius')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΥΒΤ6001','3','8','Ford Edge')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΥΥΜ1160','2','8','Mazda 3')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΤΡB3432','1','9','VW Golf')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΒΚΚ1290','1','10','Ford K+')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΚΑΑ3081','3','11','Dodge Caravan')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΡTB7742','3','11','Land Rover Range Rover')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΤΖΑ7878','2','6','Toyota Camry')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΒΕΕ1340','3','6','Chevrolet Tahoe')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΥΤΙ8700','2','7','Honda Accord')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΧΑΑ4177','3','12','Mitsubishi Outlander')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΑΜΑ2000','1','13','Toyota Camry')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΙΚΑ7622','2','14','Ford Fusion Se')")
c.execute("INSERT OR IGNORE INTO car VALUES('ΟΟΑ8444','1','15','Nissan Altima')")
c.execute("INSERT OR IGNORE INTO car VALUES('BAA3251','2','15','Toyota Camry')")
c.execute("INSERT OR IGNORE INTO car VALUES('AIA1568','1','2','Toyota Corolla ')")
c.execute("INSERT OR IGNORE INTO car VALUES('ABE9526','2','3','Nissan Sentra')")
c.execute("INSERT OR IGNORE INTO car VALUES('EEA1064','1','2','Mazda Cx-5')")
c.execute("INSERT OR IGNORE INTO car VALUES('AIB7456','3','4','Jeep Cherokee')")
c.execute("INSERT OR IGNORE INTO car VALUES('IBA1763','2','5','Chevrolet Cobalt')")
c.execute("INSERT OR IGNORE INTO car VALUES('IAK8780','3','6','Ford Edge')")
c.execute("INSERT OR IGNORE INTO car VALUES('OAT8562','3','7','Ford Escape')")
c.execute("INSERT OR IGNORE INTO car VALUES('KKB8742','2','7','Mazda 3')")

#locations
c.execute("INSERT OR IGNORE INTO location VALUES('0001','Piraeus')")
c.execute("INSERT OR IGNORE INTO location VALUES('0002','Athens')")
c.execute("INSERT OR IGNORE INTO location VALUES('0003','Patras')")
c.execute("INSERT OR IGNORE INTO location VALUES('0004','Volos')")
c.execute("INSERT OR IGNORE INTO location VALUES('0005','Thessaloniki')")
c.execute("INSERT OR IGNORE INTO location VALUES('0006','Korinthos')")
c.execute("INSERT OR IGNORE INTO location VALUES('0007','Chania')")
c.execute("INSERT OR IGNORE INTO location VALUES('0008','Heraklio')")
c.execute("INSERT OR IGNORE INTO location VALUES('0009','Larissa')")
c.execute("INSERT OR IGNORE INTO location VALUES('0010','Trikala')")
c.execute("INSERT OR IGNORE INTO location VALUES('0011','Ioannina')")
c.execute("INSERT OR IGNORE INTO location VALUES('0012','Xanthi')")
c.execute("INSERT OR IGNORE INTO location VALUES('0013','Chalkida')")
c.execute("INSERT OR IGNORE INTO location VALUES('0014','Agrinio')")
c.execute("INSERT OR IGNORE INTO location VALUES('0015','Komotini')")


#services
c.execute("INSERT INTO services VALUES('1','Extra Driver','10')")
c.execute("INSERT INTO services VALUES('2','GPS','7')")
c.execute("INSERT INTO services VALUES('3','Baby Seat','12')")
c.execute("INSERT INTO services VALUES('4','Telephone Customer Service','3')")


#category
c.execute("INSERT INTO category VALUES('1','City','5','4','Manual','30')")
c.execute("INSERT INTO category (size,seat_number,door_number,transmission,cost_per_day) VALUES('SUV','5','4','Manual','40')")
c.execute("INSERT INTO category (size,seat_number,door_number,transmission,cost_per_day) VALUES('Jeep','5','4','Manual','50')")


#insurance
c.execute("INSERT INTO insurance VALUES('1','Silver','20')")
c.execute("INSERT INTO insurance VALUES('2','Golden','30')")
c.execute("INSERT INTO insurance VALUES('3','Platinum','40')")

#commit command
conn.commit()
#close connection to database
conn.close()
 
