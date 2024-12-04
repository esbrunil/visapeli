import sqlite3

conn = sqlite3.connect("paivakanta.db")
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS HallOfFame (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aihe_id INTEGER NOT NULL,
        nimi TEXT NOT NULL,
        pisteet INTEGER NOT NULL
    )     
''')

