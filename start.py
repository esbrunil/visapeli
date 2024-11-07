# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, render_template, session, url_for
from flask_cors import CORS
from functools import wraps
import time, json, math, random


app = Flask(__name__)
CORS(app)


# Palauttaa default-html:n, kun sivu ladataan
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/ValitseAihe", methods=['GET'])
def ValitseAihe():
    return render_template("index.html")

@app.route("/Peli/<path:aihe>", methods=['GET'])
def Peli(aihe):
    return render_template("peli.html")


# Palauttaa clientille käyttäjäspesifin ID:n
# attr: None
# return: id
@app.route('/annaID', methods=['GET'])
def annaID():
    id = None
    with open('users.json', 'r') as users:
        liveUsers = json.load(users)

    #ID ajanhetken perusteella. Jos ID on jo varattu, pyöritetään silmukkaa, kunnes vapaa ID löytyy.
    while True:
        varattu = False
        id = (str)(math.floor(time.time()))

        if id in liveUsers:
            varattu = True

        if not varattu:
            break

    liveUsers[id] = {"aihe": ""}
    
    with open('users.json', 'w') as users:
        json.dump(liveUsers, users, indent=2)

    return id, 200


# Asettaa aiheen käyttäjälle
# attr: { userID, aihe}
# return onnistuiko?
@app.route('/asetaAihe', methods=['POST'])
def asetaAihe():
    id = request.json['kayttajaID']
    aihe = request.json['aihe']

    with open('users.json', 'r') as users:
        data = json.load(users)
    
    data[id]['aihe'] = aihe

    with open('users.json', 'w') as users:
        json.dump(data, users, indent=2)

    kysymykset = []
    with open('kysymykset.json',  'r') as qF:
        qData = json.load(qF)
    
    for q in qData[aihe]:
        kysymykset.append(q)

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
    vastaus = request.json['vastaus']
    kysymysID = request.json['kysymysID']
    kayttajaID = request.json['kayttajaID'] #tai aihe?

    with open('kysymykset.json', 'r') as kysymykset:
        data = json.load(kysymykset)
    
    # hae tässä datasta haluttu tieto, eli oikeiden vastausten taulukko
    # tarkista
    # palauta mitä?
    return data, 200
