import sqlite3, random

# 
# Sekoittaa tietokannan kysymykset
#


def sekoita():
    conn = sqlite3.connect("tietokanta.db")
    c = conn.cursor()

    c.execute("SELECT id FROM Kysymykset")

    arr = [tup[0] for tup in c.fetchall()]
    shuf = random.sample(arr, len(arr))

    temp_offset = max(arr) + 1
    for id in arr:
        c.execute(f"UPDATE Kysymykset Set id = {id + temp_offset} WHERE id = {id}")

    print(shuf)

    i = 0
    for id in arr:
        c.execute(f"UPDATE Kysymykset SET id = {shuf[i]} WHERE id = {id + temp_offset}")
        i += 1


    conn.commit()
    conn.close()



sekoita()