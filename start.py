
#!../visapeli-venv/venv/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, render_template, session, url_for, jsonify
from flask_cors import CORS
from functools import wraps
from filelock  import FileLock, Timeout
#from tietokanta.lisaaKantaan import get_kysymyksia_lkm_looppaamalla, haeKannasta, tarkista_onko_oikein
import time, json, math, random, uuid, sqlite3, requests


app = Flask(__name__)
CORS(app)


# Reitit ------------------------------------------------------------------------------------------------------------------------------------------


# Palauttaa default-html:n, kun sivu ladataan
@app.route("/", methods=['GET'])
def index():
    #testaa onko uusi päivä ja päivitä päivänvisa?
    #return redirect(request.base_url + "ValitseAihe", 301)
    return "helou", 200


@app.route("/ValitseAihe", methods=['GET'])
def ValitseAihe():
    return render_template("index.html")

@app.route("/Peli/Results", methods=['GET'])
def Results():
    return render_template("index.html")

@app.route("/Peli/<path:aihe>", methods=['GET'])
def Peli(aihe):
    return render_template("index.html")

@app.route('/heartbeat', methods=['POST'])
def Heartbeat():
    aika = math.floor(time.time())
    id = request.json["kayttajaID"]

    data = lueJSONTiedosto("users.json")

    data[id]["heartbeat"] = aika

    for user in list(data):
        if (aika - data[user]["heartbeat"]) > 10:
            del data[user]

    kirjoitaJSONTiedostoon("users.json", data)

            
    return "", 200


# Asettaa käyttäjälle käyttäjänimen, tai valitsee randomin. Palauttaa käyttäjänimen.
# attr: nimi, random, käyttäjän_id
# return: nimi
@app.route("/asetaNimi", methods={"POST"})
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
        print("not")
        exists = 201

    data[id]["nimi"] = nimi

    kirjoitaJSONTiedostoon("users.json", data)

    return nimi, exists

# Palauttaa clientille käyttäjäspesifin ID:n
# attr: None
# return: id
@app.route('/annaID', methods=['GET'])
def annaID():
    #luo indeksi, joka välillä 1 ja max lkm aiheista i mod h
    #connect ja close
    id = None
    liveUsers = lueJSONTiedosto("users.json")

    id = (str)(uuid.uuid4())

    maksimi = math.floor(random.random() * haeKannasta(lambda c: hae_taulujen_maksimi(c)))

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
    
    data[id]['aihe'] = aihe
    data[id]['pisteet'] = 0

    kirjoitaJSONTiedostoon("users.json", data)

    aihe_id = haeKannasta(lambda c: hae_aihe_id(aihe, c))
    kysymykset = haeKannasta(lambda c: hae_n_kysymys_id(aihe_id[0], data[id]["indeksi"], maara, c))

    if len(kysymykset) < maara:
        kysymykset.extend(haeKannasta(lambda c: hae_n_kysymys_id(aihe_id[0], 0, maara - len(kysymykset), c)))

    if len(kysymykset) > 0:
        data[id]["indeksi"] = kysymykset[len(kysymykset) - 1]

    return { "aiheData": data[id], "kysymykset": kysymykset }, 200


@app.route('/haeKysymys', methods=['POST'])
def haeKysymys():
    userID = request.json['kayttajaID']
    qID = request.json['kysymysID']

    kysymys = haeKannasta(lambda c: hae_kysymys(qID, c))

    return kysymys[qID], 200



# Tarkistaa annetun vastauksen
# attr: { vastaus, kysymysID, kayttajaID}
# return oikeiden määrä?
@app.route('/tarkistaVastaus', methods=['POST'])
def tarkistaVastaus():
    kysymys = (int)(request.json["kysymysID"])
    vastaus = (int)(request.json['vastausID'])
    aika = (int)(request.json["aika"])
    id = request.json["kayttajaID"]

    aika = 2000

    if vastaus >= 0:
        ov = haeKannasta(lambda c: hae_kysymys_ksm_ov(kysymys, c))[0][1]
        print(ov)
        if ov <= 1:
            onko_oikein = vastaus == ov

        else: onko_oikein = haeKannasta(lambda c: tarkista_onko_oikein(vastaus, c))[0][0]

    else: 
        onko_oikein = False

    pisteet = 0
    if onko_oikein:
        pisteet = min(10000, (2000 + aika))
        data = lueJSONTiedosto("users.json")
        data[id]["pisteet"] += pisteet
        kirjoitaJSONTiedostoon("users.json", data)


    #return ((str)(onko_oikein)).lower(), 200
    return jsonify({ "onkoOikein": ((str)(onko_oikein)).lower(), "pisteet": pisteet }), 200


# Antaa käyttäjän pisteet
# attr: id
# return: pisteet
@app.route("/annaPisteet", methods=["POST"])
def annaPisteet():
    id = request.json["kayttajaID"]
    data = lueJSONTiedosto("users.json")    
    return data[id]["pisteet"], 200


# Yleiset funktiot ------------------------------------------------------------------------------------------------------------------------------------------

# Tietokanta ------------------------------------------------------------------------------------------------------------------------------------------


# Hakee tietokannasta siten, että kanta avataan ja suljetaan vain kerran. Argumentin funktio määrittelee tietokantaoperaation
def haeKannasta(func):
    conn = sqlite3.connect('tietokanta/tietokanta.db')
    c = conn.cursor()
    res = func(c)
    conn.close()
    return res


# Hakee n-kysymyksen id:t jostain luvusta lähtien tietyltä aiheelta
def hae_n_kysymys_id(aihe, alku, maara, c):
    c.execute(f"SELECT id FROM Kysymykset WHERE id > {alku} AND aihe_id = {aihe} LIMIT {maara}")
    return [item[0] for item in c.fetchall()]


# Hakee aiheen id:n tekstin perusteella
def hae_aihe_id(aihe, c):
    c.execute(f"SELECT id FROM Aiheet WHERE aihe = ?", (aihe,))
    return c.fetchone()


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
    c.execute(f"SELECT * FROM Aiheet")
    aiheet = c.fetchall()
    maksimi = 0
    for aihe in aiheet:
        c.execute(f"SELECT COUNT(*) FROM Kysymykset WHERE aihe_id = {aihe[0]}")
        maara = c.fetchone()
        if maara[0] > maksimi:
            maksimi = maara[0]
    return maksimi

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