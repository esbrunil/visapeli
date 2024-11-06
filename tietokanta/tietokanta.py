import sqlite3

#suluissa :memory:, niin tekee vain muistiin
#conn = sqlite3.connect('employee.db')
conn = sqlite3.connect(':memory:')

c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS Aiheet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aihe TEXT NOT NULL
    )
''')

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
            onko_oikein BOOLEAN,
            vve_teksti TEXT,
            FOREIGN KEY (kysymys_id) REFERENCES Kysymykset (id) ON DELETE CASCADE
        )
''')


def insert_kysymys(aihe_id, vastauksia, oikea_vastaus, kysymys):
    with conn:
        c.execute('''INSERT INTO Kysymykset (aihe_id, vastauksia, oikea_vastaus, kysymys) VALUES (?,?,?,?)''', 
                  (aihe_id, vastauksia, oikea_vastaus, kysymys))
        

def insert_aihe(aihe):
    with conn:
        c.execute('''INSERT INTO Aiheet (aihe) VALUES (?)''', (aihe,))

def get_aihe_id(aihe):
    c.execute('SELECT id FROM Aiheet WHERE aihe = ?', (aihe,))
    return c.fetchone()

def get_kysymys_id(kysymys):
    c.execute('SELECT id FROM Kysymykset WHERE kysymys = ?', (kysymys,))
    return c.fetchone()

def insert_vve(kysymys_id, onko_oikein, teksti):
    c.execute('''INSERT INTO Vastausvaihtoehdot (kysymys_id, onko_oikein, vve_teksti) VALUES (?,?,?)''',
              (kysymys_id, onko_oikein, teksti))

aihe = "Historia"
insert_aihe(aihe)
insert_kysymys(get_aihe_id(aihe)[0], 4, 2, "Mitä värejä on Suomen lipussa?")
k_id = get_kysymys_id("Mitä värejä on Suomen lipussa?")[0]
insert_vve(k_id, False, "punainen")
insert_vve(k_id, False, "vihreä")
insert_vve(k_id, True, "valkoinen")
insert_vve(k_id, True, "sininen")

c.execute('SELECT * FROM Vastausvaihtoehdot WHERE kysymys_id = (?) AND onko_oikein = TRUE', (k_id,))
print(c.fetchall())

conn.close()