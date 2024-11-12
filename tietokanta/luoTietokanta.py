import sqlite3, json
from kysymyssetti import Kysymyssetti

#suluissa :memory:, niin tekee vain muistiin
conn = sqlite3.connect('tietokanta.db')
#conn = sqlite3.connect(':memory:')

c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS Aiheet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aihe TEXT NOT NULL UNIQUE
    )
''')

#Olk oikea_vastaus = ov, tällöin jos ov = 0 --> False,
#ov = 1 --> True (vastauksia = 2), ov = 2 --> (vastauksia > 2) Custom --> 
#Luodaan rivit tauluun Vastausvaihtoehdot
c.execute('''
    CREATE TABLE IF NOT EXISTS Kysymykset (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aihe_id INTEGER,
        vastauksia INTEGER,
        oikea_vastaus INTEGER,
        kysymys TEXT,
        FOREIGN KEY (aihe_id) REFERENCES Aiheet (id) ON DELETE CASCADE
    )
''')

c.execute('''
          CREATE TABLE Vastausvaihtoehdot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kysymys_id INTEGER,
            vve_teksti TEXT,
            onko_oikein BOOLEAN,
            FOREIGN KEY (kysymys_id) REFERENCES Kysymykset (id) ON DELETE CASCADE
        )
''')




#loytyko = get_aiheet()
#for row in loytyko:
#    print(row)

#loytyko = get_kysymykset()
#for row in loytyko:
#    print(row)

#loytyko = get_vve()
#for row in loytyko:
#    print(row)
conn.close()