import sqlite3, json
from kysymyssetti import Kysymyssetti

#suluissa :memory:, niin tekee vain muistiin
conn = sqlite3.connect('kysymykset.db')
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


def insert_aihe(aihe):
    with conn:
        c.execute('''INSERT INTO Aiheet (aihe) VALUES (?)''', (aihe,))

def insert_kysymys(aihe_id, vastauksia, oikea_vastaus, kysymys):
    with conn:
        c.execute('''INSERT INTO Kysymykset (aihe_id, vastauksia, oikea_vastaus, kysymys) VALUES (?,?,?,?)''', 
                  (aihe_id, vastauksia, oikea_vastaus, kysymys))
        
def insert_vve(kysymys_id, teksti, onko_oikein):
    c.execute('''INSERT INTO Vastausvaihtoehdot (kysymys_id, vve_teksti, onko_oikein) VALUES (?,?,?)''',
              (kysymys_id, teksti, onko_oikein))

def get_aihe_id(aihe):
    c.execute('SELECT id FROM Aiheet WHERE aihe = ?', (aihe,))
    return c.fetchone()

def get_aihe(aihe):
    c.execute('SELECT aihe FROM Aiheet WHERE aihe = ?', (aihe,))
    return c.fetchone()

def get_aiheet():
    c.execute("SELECT * FROM Aiheet")
    return c.fetchall()

def get_kysymykset():
    c.execute("SELECT * FROM Kysymykset")
    return c.fetchall()

def get_vve():
    c.execute("SELECT * FROM Vastausvaihtoehdot")
    return c.fetchall()

def get_kysymys_id(kysymys):
    c.execute('SELECT id FROM Kysymykset WHERE kysymys = ?', (kysymys,))
    return c.fetchone()

def get_vastauksia(id):
    c.execute('SELECT vastauksia FROM Kysymykset WHERE id = ?', (id,))
    return c.fetchone()

'''
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
'''

with open('./Visapeli/tietokanta/pk.json', 'r') as kysym:
    data = json.load(kysym)
ksetti = Kysymyssetti(data)

print(get_aihe("historia") == None)

for kysymys in ksetti.kysymykset:
    if(get_aihe(kysymys.aihe) == None):
        insert_aihe(kysymys.aihe)
    insert_kysymys(get_aihe_id(kysymys.aihe)[0],kysymys.vastauksia,
                   kysymys.oikea_vastaus,kysymys.kysymys)
    if(kysymys.oikea_vastaus == 2):
        k_id = get_kysymys_id(kysymys.kysymys)[0]
        for key, value in kysymys.vve.items():
            insert_vve(k_id, key, value)

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