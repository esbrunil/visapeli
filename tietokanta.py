import sqlite3
from kysymys import Kysymys

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
    CREATE TABLE IF NOT EXISTS KSetti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aihe_id INTEGER,
        kysymys TEXT NOT NULL,
        FOREIGN KEY (aihe_id) REFERENCES Aiheet (id) ON DELETE CASCADE
    )
''')

#autoincrementin voi jättää pois?
c.execute('''
          CREATE TABLE Kysymys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kysymykset_id INTEGER,
            kysymys TEXT NOT NULL,
            o TEXT NOT NULL,
            vve TEXT NOT NULL,
            lkm INT NOT NULL,
            FOREIGN KEY (kysymykset_id) REFERENCES KSetti (id) ON DELETE CASCADE
        )
''')

#vve = vastausvaihtoehdot
#käytetään luokkaa? Ei tarvita tällöin tuota lkm?
def insert_kysymys(kysymys):
    with conn:
        c.execute('''INSERT INTO Kysymys (kysymys, o, vve, lkm) VALUES (?,?,?,?)''', 
                  (kysymys.kysymys, kysymys.o, kysymys.vastausvaihtoehdot, kysymys.lkm))
        

def insert_aihe(aihe):
    with conn:
        c.execute('''INSERT INTO Aiheet (aihe) VALUES (?)''', (aihe,))


def insert_ksetti(aihe_id, kysymys):
    with conn:
        c.execute('''INSERT INTO KSetti (aihe_id, kysymys) VALUES (?,?)''', (aihe_id, kysymys))

def get_aihe_id(aihe):
    c.execute('SELECT id FROM Aiheet WHERE aihe = ?', (aihe,))
    return c.fetchone()

def get_aiheet():
    c.execute("SELECT * FROM Aiheet")
    return c.fetchall()

def get_ksetti():
    c.execute("SELECT * FROM KSetti")
    return c.fetchall()

def get_o():
    c.execute("SELECT * FROM Kysymys")
    return c.fetchall()

def get_lkm(id):
    c.execute('SELECT lkm FROM Kysymys WHERE id = :id', {'id': id})
    return c.fetchone()

def get_lkm2(id):
    c.execute('SELECT lkm FROM Kysymys WHERE id = ?', (id,))
    return c.fetchone()

#minkälainen tämän tulisi olla? Kaikki vaihtoehdot?
def update_pay(emp, pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})


def remove_kysymys(id):
    with conn:
        c.execute('DELETE from Kysymys WHERE id = ?', (id,))


aihe = "Historia"
insert_aihe(aihe)
insert_ksetti(get_aihe_id(aihe)[0],"Paistaako ulkona aurinko?")
loytyyko = get_ksetti()
for row in loytyyko:
    print(row)

'''
qyssar = ["joo","ei","mega","giga"]
k1 = Kysymys(8,"joo, etet",[0,1],qyssar)
k2 = Kysymys(9,"bjoo, etet",[0,2],qyssar)
insert_kysymys(k1)
insert_kysymys(k2)
loytyko = get_o()
for row in loytyko:
    print(row)

remove_kysymys(1)
loytyko = get_o()
for row in loytyko:
    print(row)
insert_kysymys(k1)
print("jalkeen:")
loytyko = get_o()
for row in loytyko:
    print(row)
#id = get_lkm2(1)
#print(id[0])

'''
conn.close()