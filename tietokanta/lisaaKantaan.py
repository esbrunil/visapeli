import sqlite3, json, os
from kysymyssetti import Kysymyssetti


#suluissa :memory:, niin tekee vain muistiin
conn = sqlite3.connect('tietokanta/tietokanta.db')
#conn = sqlite3.connect(':memory:')
c = conn.cursor()

print(os.getcwd())

def insert_aihe(aihe):
    with conn:
        c.execute('''INSERT INTO Aiheet (aihe) VALUES (?)''', (aihe,))

def insert_kysymys(aihe_id, vastauksia, oikea_vastaus, kysymys):
    with conn:
        c.execute('''INSERT INTO Kysymykset (aihe_id, vastauksia, oikea_vastaus, kysymys) VALUES (?,?,?,?)''', 
                  (aihe_id, vastauksia, oikea_vastaus, kysymys))
        
def insert_vve(kysymys_id, teksti, onko_oikein):
    with conn:
        c.execute('''INSERT INTO Vastausvaihtoehdot (kysymys_id, vve_teksti, onko_oikein) VALUES (?,?,?)''',
              (kysymys_id, teksti, onko_oikein))

def get_aihe_id(aihe):
    c.execute('SELECT id FROM Aiheet WHERE aihe = ?', (aihe,))
    return c.fetchone()

def get_aihe(aihe):
    c.execute('SELECT aihe FROM Aiheet WHERE aihe = ?', (aihe,))
    return c.fetchone()

def get_aiheen_kysymysten_lkm(aihe_id):
    c.execute('''SELECT COUNT(id) FROM Kysymykset WHERE aihe_id = ?''', (aihe_id,))
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

def get_kysymys(kysymys):
    c.execute('SELECT kysymys FROM Kysymykset WHERE kysymys = ?', (kysymys,))
    return c.fetchone()

def get_kysymys_id(kysymys):
    c.execute('SELECT id FROM Kysymykset WHERE kysymys = ?', (kysymys,))
    return c.fetchone()

def get_kysymyksen_oikea_vastaus(kysymys_id):
    c.execute('SELECT oikea_vastaus FROM Kysymykset WHERE id = ?', (kysymys_id,))
    return c.fetchone()

def get_vve_totuudet(kysymys_id):
    c.execute('SELECT onko_oikein FROM Vastausvaihtoehdot WHERE kysymys_id = ?', (kysymys_id,))
    return c.fetchall()

#Tämä palauttaa aina halutun määrän id:itä
#Jos ei löydy riittävästi id:itä maksimiin mennessä, niin jatketaan id:stä 1
#Olettaa, että tietokannassa on kysymyksiä > lkm
def get_kysymyksia_lkm_looppaamalla(aihe, aloitusId, lkm):
    aihe_id = get_aihe_id(aihe)[0]
    tulos = get_kysymyksia_lkm_aloittaenIdsta(aihe_id, aloitusId, lkm)
    if(len(tulos) < lkm):
        lkm = lkm - len(tulos)
        tulos = tulos + get_kysymyksia_lkm_aloittaenIdsta(aihe_id, 1, lkm)
    return tulos

def get_kysymyksia_lkm_aloittaenIdsta(aihe_id, aloitusId, lkm):
    c.execute('''SELECT id 
                 FROM Kysymykset 
                 WHERE aihe_id = ? AND id >= ?
                 LIMIT ?''', (aihe_id, aloitusId, lkm))
    return c.fetchall()

def get_vastauksia(id):
    c.execute('SELECT vastauksia FROM Kysymykset WHERE id = ?', (id,))
    return c.fetchone()

with open('tietokanta/apiKysymykset.json', 'r') as kysym:
    data = json.load(kysym)
ksetti = Kysymyssetti(data)

for kysymys in ksetti.kysymykset:
    if(get_aihe(kysymys.aihe) == None):
        insert_aihe(kysymys.aihe)
    if(get_kysymys(kysymys.kysymys) == None):
        insert_kysymys(get_aihe_id(kysymys.aihe)[0],kysymys.vastauksia,
                    kysymys.oikea_vastaus,kysymys.kysymys)
        if(kysymys.oikea_vastaus == 2):
            k_id = get_kysymys_id(kysymys.kysymys)[0]
            for key, value in kysymys.vve.items():
                insert_vve(k_id, key, value)

if __name__ == "__main__":
    print(get_aiheet())
    print(get_kysymykset())
    print(get_vve())
    result = get_kysymyksia_lkm_looppaamalla("History", 2, 3)
    #result2 = get_kysymyksia_lkm_aloittaenIdsta("History", 2, 3)
    #result3 = result + result2
    ids = [row[0] for row in result]
    print(ids)
    #print(result3)
    print(get_aiheen_kysymysten_lkm(1)[0])

#tästä alaspäin periaatteessa tarkistamisen toteutus

conn.close()