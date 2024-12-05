
#!../visapeli-venv/venv/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, render_template, session, url_for, jsonify
from flask_cors import CORS
from functools import wraps
from filelock  import FileLock, Timeout
#from tietokanta.lisaaKantaan import get_kysymyksia_lkm_looppaamalla, tkOperaatio, tarkista_onko_oikein
import time, json, math, random, uuid, sqlite3, requests, bisect


app = Flask(__name__)
CORS(app)


# Reitit ------------------------------------------------------------------------------------------------------------------------------------------


# Palauttaa default-html:n, kun sivu ladataan
@app.route("/", methods=['GET'])
def index():
    #testaa onko uusi päivä ja päivitä päivänvisa?
    return redirect(request.base_url + "ValitseAihe", 301)
    #return "helou", 200


@app.route("/ValitseAihe", methods=['GET'])
def ValitseAihe():
    return render_template("index.html")


@app.route("/Peli/<path:aihe>", methods=['GET'])
def Peli(aihe):
    return render_template("index.html")


@app.route("/ErrorPage", methods=['GET'])
def Error():
    return render_template("index.html")


@app.route('/heartbeat', methods=['POST'])
def Heartbeat():
    aika = math.floor(time.time())
    id = request.json["kayttajaID"]

    data = lueJSONTiedosto("users.json")

    data[id]["heartbeat"] = aika

    for user in list(data):
        if (aika - data[user]["heartbeat"]) > 30:
            del data[user]

    kirjoitaJSONTiedostoon("users.json", data)
       
    return "", 200



@app.route("/annaAiheet", methods=["GET"])
def annaAiheet():
    return tkOperaatio(lambda c: haeAiheet(c), 'tietokanta/tietokanta.db')


# Asettaa käyttäjälle käyttäjänimen, tai valitsee randomin. Palauttaa käyttäjänimen.
# attr: nimi, random, käyttäjän_id
# return: nimi
@app.route("/asetaNimi", methods=["POST"])
def asetaNimi():
    id = request.json["kayttajaID"]
    rnd = request.json["rnd"]
    nimi = request.json["nimi"]

    if rnd:
        nimi = requests.get("http://users.jyu.fi/~rajuruok/cgi-bin/visanimi/nimi.cgi/", headers={
            "Accept": "text/plain"
        }).text

    data = lueJSONTiedosto("users.json")
    
    exists = 200
    if not id in data:
        exists = 201

    data[id]["nimi"] = nimi

    kirjoitaJSONTiedostoon("users.json", data)

    return nimi, exists

# Palauttaa clientille käyttäjäspesifin ID:n
# attr: None
# return: id
@app.route('/annaID', methods=['GET'])
def annaID():
    id = None
    liveUsers = lueJSONTiedosto("users.json")

    id = (str)(uuid.uuid4())

    maksimi = math.floor(random.random() * tkOperaatio(lambda c: hae_kysymykset_lkm(c), 'tietokanta/tietokanta.db'))

    liveUsers[id] = { "aihe": "", "heartbeat": math.floor(time.time()), "nimi": "", "indeksi": maksimi, "pisteet": 0 }
    
    kirjoitaJSONTiedostoon("users.json", liveUsers)

    return id, 200


# Asettaa aiheen käyttäjälle
# attr: { userID, aihe}
# return onnistuiko?
@app.route('/asetaAihe', methods=['POST'])
def asetaAihe():
    id = request.json['kayttajaID']
    aihe = request.json['aihe']

    maara = 10

    data = lueJSONTiedosto("users.json")

    aihe_id = tkOperaatio(lambda c: hae_aihe_id(aihe, c), 'tietokanta/tietokanta.db')
    kysymykset = tkOperaatio(lambda c: hae_n_kysymys_id(aihe_id, data[id]["indeksi"], maara, c), 'tietokanta/tietokanta.db')

    if len(kysymykset) < maara:
        kysymykset.extend(tkOperaatio(lambda c: hae_n_kysymys_id(aihe_id, 0, maara - len(kysymykset), c)), 'tietokanta/tietokanta.db')

    if len(kysymykset) > 0:
        data[id]["indeksi"] = kysymykset[len(kysymykset) - 1]

    data[id]['aihe'] = aihe
    data[id]['pisteet'] = 0
    data[id]['indeksi'] += maara

    kirjoitaJSONTiedostoon("users.json", data)

    return { "aiheData": data[id], "kysymykset": kysymykset }, 200


@app.route('/haeKysymys', methods=['POST'])
def haeKysymys():
    userID = request.json['kayttajaID']
    qID = request.json['kysymysID']

    kysymys = tkOperaatio(lambda c: hae_kysymys(qID, c), 'tietokanta/tietokanta.db')

    return kysymys[qID], 200



# Tarkistaa annetun vastauksen
# attr: { vastaus, kysymysID, kayttajaID}
# return oikeiden määrä?
@app.route('/tarkistaVastaus', methods=['POST'])
def tarkistaVastaus():
    kysymys = (int)(request.json["kysymysID"])
    vastaus = (int)(request.json['vastausID'])
    #aika = (int)(request.json["aika"])
    #id = request.json["kayttajaID"]

    aika = 2000
    data = lueJSONTiedosto("users.json")
    id = next(iter(data))

    aika = 2000

    ov = tkOperaatio(lambda c: hae_kysymys_ksm_ov(kysymys, c), 'tietokanta/tietokanta.db')[0][1]
    if ov <= 1:
        onko_oikein = vastaus == ov

    else: onko_oikein = tkOperaatio(lambda c: tarkista_onko_oikein(vastaus, c), 'tietokanta/tietokanta.db')[0][0]


    pisteet = 0
    if onko_oikein:
        pisteet = min(10000, (2000 + aika))
        data = lueJSONTiedosto("users.json")
        data[id]["pisteet"] += pisteet
        kirjoitaJSONTiedostoon("users.json", data)


    #return ((str)(onko_oikein)).lower(), 200
    return jsonify({"onkoOikein": ((str)(onko_oikein)).lower(), "pisteet": pisteet }), 200


# Antaa käyttäjän pisteet
# attr: id
# return: pisteet
@app.route("/annaPisteet", methods=["POST"])
def annaPisteet():
    id = request.json["kayttajaID"]
    data = lueJSONTiedosto("users.json")  
    return data[id]["pisteet"], 200


# Lisää pelin päätteeksi käyttäjäen tarvittaessa hall of fameen
# attr: käyttäjän id
# return: json-objekti, jossa pisteet ja hall of fame data
@app.route("/paataPeli", methods=["POST"])
def paataPeli(id):
    #id = request.json["kayttajaID"]
    data = lueJSONTiedosto("users.json")  

    tkOperaatio(lambda c: lisaa_jos_ansaitsee(c, data[id]), "tietokanta/paivakanta.db")

    hof = tkOperaatio(lambda c: anna_hof(c, data[id]["aihe"]), "tietokanta/paivakanta.db")

    return hof


# Yleiset funktiot ------------------------------------------------------------------------------------------------------------------------------------------

# Tietokanta ------------------------------------------------------------------------------------------------------------------------------------------


# Hakee tietokannasta siten, että kanta avataan ja suljetaan vain kerran. Argumentin funktio määrittelee tietokantaoperaation
def tkOperaatio(func, osoite):
    conn = sqlite3.connect(osoite)
    c = conn.cursor()
    res = func(c)
    conn.commit()
    conn.close()
    return res


def anna_hof(c, aihe):
    aihe_id = tkOperaatio(lambda c: hae_aihe_id(aihe, c), "tietokanta/tietokanta.db")
    c.execute(f"SELECT * FROM HallOfFame WHERE aihe_id = {aihe_id}")
    return c.fetchall()



# Vaiheessa !
def lisaa_jos_ansaitsee(c, pelaaja):
    aihe = tkOperaatio(lambda c: hae_aihe_id(pelaaja["aihe"], c), "tietokanta/tietokanta.db")
    c.execute("INSERT INTO HallOfFame (aihe_id, nimi, pisteet) VALUES (?,?,?)", (aihe, pelaaja["nimi"], pelaaja["pisteet"]))
    c.execute("""
        DELETE FROM HallOfFame
        WHERE aihe_id = ? AND id NOT IN (
            SELECT id FROM HallOfFame ORDER BY pisteet DESC LIMIT 10
        )
    """, (aihe,))
    return


# Hakee n-kysymyksen id:t jostain luvusta lähtien tietyltä aiheelta
def hae_n_kysymys_id(aihe, alku, maara, c):
    c.execute(f"SELECT id FROM Kysymykset WHERE id > {alku} AND aihe_id = {aihe} LIMIT {maara}")
    return [item[0] for item in c.fetchall()]


# Hakee aiheen id:n tekstin perusteella
def hae_aihe_id(aihe, c):
    c.execute(f"SELECT id FROM Aiheet WHERE aihe = ?", (aihe,))
    return c.fetchone()[0]


# Hakee kysymyksen ja vastausvaihtoehdot kysymyksen id:n perusteella
def hae_kysymys(kysymysID, c):
    obj = { kysymysID: {
        "kysymys": "",
        "vastausvaihtoehdot": {}
    }}
    kysymys = hae_kysymys_ksm_ov(kysymysID, c)
    obj[kysymysID]["kysymys"] = kysymys[0][0]

    if kysymys[0][1] > 1:
        c.execute(f"SELECT id, vve_teksti FROM Vastausvaihtoehdot WHERE kysymys_id = {kysymysID}")
        vvet = c.fetchall()
        for vve in vvet:
            obj[kysymysID]["vastausvaihtoehdot"][vve[0]] = vve[1]

    else:
        obj[kysymysID]["vastausvaihtoehdot"] = { 0: "False", 1: "True" }

    return obj


# Hakee kysymyksen tekstin ja oikean vastauksen tyypin kysymyksen id:n perusteella
def hae_kysymys_ksm_ov(kysymysID, c):
    c.execute(f"SELECT kysymys, oikea_vastaus FROM Kysymykset WHERE id = {kysymysID}")
    return c.fetchall()


# Tarkistaa, onko vastaus oikein
def tarkista_onko_oikein(vastausID, c):
    c.execute(f"SELECT onko_oikein FROM (SELECT * FROM Vastausvaihtoehdot WHERE id = {vastausID})")
    return c.fetchall()


# Hakee maksimimäärän kysymyksiä per aihe
def hae_taulujen_maksimi(c):
    c.execute("SELECT * FROM Aiheet")
    aiheet = c.fetchall()
    maksimi = 0
    for aihe in aiheet:
        c.execute(f"SELECT COUNT(*) FROM Kysymykset WHERE aihe_id = {aihe[0]}")
        maara = c.fetchone()
        if maara[0] > maksimi:
            maksimi = maara[0]
    return maksimi


def hae_kysymykset_lkm(c):
    c.execute("SELECT COUNT(*) FROM Kysymykset")
    return c.fetchone()[0]


def haeAiheet(c):
    c.execute("SELECT * FROM Aiheet")
    return c.fetchall()

# Muut ------------------------------------------------------------------------------------------------------------------------------------------


def lueJSONTiedosto(tiedosto):
    lock_tied = f"{tiedosto}.lock"

    lock = FileLock(lock_tied, 5)

    try:
        with lock:
            try:
                with open(tiedosto, "r") as tied:
                    return json.load(tied)
            except json.JSONDecodeError:
                return {}
    except Timeout:
        return "timeout"
        

def kirjoitaJSONTiedostoon(tiedosto, data):
    lock_tied = f"{tiedosto}.lock"

    lock = FileLock(lock_tied, 5)

    try:
        with lock:
            with open(tiedosto, "w") as tied:
                json.dump(data, tied, indent=2)
    except Timeout:
        return "timeout"