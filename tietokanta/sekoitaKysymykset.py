import sqlite3, random, sys

# 
# Sekoittaa tietokannan kysymykset
#


def sekoita():
    conn = sqlite3.connect("tietokanta.db")
    c = conn.cursor()

    c.execute(f"SELECT COUNT(*) FROM Kysymykset")
    maara = c.fetchone()[0]

    c.execute("SELECT id FROM Kysymykset")

    arr = [tup[0] for tup in c.fetchall()]
    shuf = random.sample(arr, len(arr))

    i = 0
    temp_offset = max(arr) + 1
    for id in arr:
        sys.stdout.write(f"\rAlustetaan: {i}/{maara}")
        c.execute(f"UPDATE Kysymykset SET id = {id + temp_offset} WHERE id = {id}")
        c.execute(f"UPDATE Vastausvaihtoehdot SET kysymys_id = {id + temp_offset} WHERE kysymys_id = {id}")
        i+=1

    i = 0
    for id in arr:
        sys.stdout.write(f"\rSekoitetaan: {i}/{maara}")
        c.execute(f"UPDATE Kysymykset SET id = {shuf[i]} WHERE id = {id + temp_offset}")
        c.execute(f"UPDATE Vastausvaihtoehdot SET kysymys_id = {shuf[i]} WHERE kysymys_id = {id + temp_offset}")
        i += 1


    conn.commit()
    conn.close()



sekoita()