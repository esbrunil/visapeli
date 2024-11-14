# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, render_template, session, url_for
from flask_cors import CORS
from functools import wraps
from filelock  import FileLock, Timeout
import time, json, math, random, uuid, sqlite3


app = Flask(__name__)
CORS(app)


# Reitit ------------------------------------------------------------------------------------------------------------------------------------------


# Palauttaa default-html:n, kun sivu ladataan
@app.route("/", methods=['GET'])
def index():
    #testaa onko uusi päivä ja päivitä päivänvisa?
    return redirect(request.base_url + "ValitseAihe", 301)


@app.route("/ValitseAihe", methods=['GET'])
def ValitseAihe():
    return render_template("index.html")

@app.route("/Peli/<path:aihe>", methods=['GET'])
def Peli(aihe):
    return render_template("peli.html")


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



# Palauttaa clientille käyttäjäspesifin ID:n
# attr: None
# return: id
@app.route('/annaID', methods=['GET'])
def annaID():
    #luo indeksi, joka välillä 1 ja max lkm aiheista i mod h
    #miten maksimi saadaan?
    #pitää varmaan luoda joku kyselyhässäkkä, joka palauttaa maksimin?

    id = None
    liveUsers = lueJSONTiedosto("users.json")

    id = (str)(uuid.uuid4())

    liveUsers[id] = {"aihe": "", "heartbeat": math.floor(time.time()), "nimi": ""}
    
    kirjoitaJSONTiedostoon("users.json", liveUsers)

    return id, 200


# Asettaa aiheen käyttäjälle
# attr: { userID, aihe}
# return onnistuiko?
@app.route('/asetaAihe', methods=['POST'])
def asetaAihe():
    id = request.json['kayttajaID']
    aihe = request.json['aihe']

    data = lueJSONTiedosto("users.json")
    
    data[id]['aihe'] = aihe

    kirjoitaJSONTiedostoon("users.json", data)

    kysymykset = []
    qData = lueJSONTiedosto("kysymykset.json")
    
    for q in qData[aihe]:
        kysymykset.append(q)
    #algoritmi:
    #aloitusindeksi = käyttäjän indeksi
    #kysymyslkm = montako kysymystä haetaan
    #i = 0
    #while i < kysymyslkm
    #hae kysymyksiä
    #i++

    #päivitä users.json indeksi
    random.shuffle(kysymykset)

    return { "aiheData": data[id], "kysymykset": kysymykset }, 200


@app.route('/haeKysymys', methods=['POST'])
def haeKysymys():
    userID = request.json['kayttajaID']
    qID = request.json['kysymysID']
    aihe = request.json['aihe']

    with open('kysymykset.json', 'r') as kysym:
        data = json.load(kysym)
        kysymys = data[aihe][qID]
        del kysymys['o']

    return kysymys, 200



# Tarkistaa annetun vastauksen
# attr: { vastaus, kysymysID, kayttajaID}
# return oikeiden määrä?
@app.route('/tarkistaVastaus', methods=['POST'])
def tarkistaVastaus():
    vastaus = request.json['vastausID']

    oikein = tarkista_onko_oikein(vastaus)
    
    # hae tässä datasta haluttu tieto, eli oikeiden vastausten taulukko
    # tarkista
    # palauta mitä?
    return (str)(oikein), 200


# Yleiset funktiot ------------------------------------------------------------------------------------------------------------------------------------------

def haeKannasta(query):
    conn = sqlite3.connect('tietokanta/tietokanta.db')
    c = conn.cursor()
    c.execute(query)
    res = c.fetchone()
    conn.close()
    return res


def tarkista_onko_oikein(vastausID):
    q = f"SELECT onko_oikein FROM (SELECT * FROM Vastausvaihtoehdot WHERE id = {vastausID})"
    return haeKannasta(q)[0]


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
