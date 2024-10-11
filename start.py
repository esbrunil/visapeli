# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, render_template, session, url_for
from flask_cors import CORS
from functools import wraps
import time, json, math

app = Flask(__name__)
CORS(app)


# Palauttaa default-html:n, kun sivu ladataan
@app.route("/", methods=['GET'])
def index():
    return render_template("jotain.html")


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
    id = request.json['userID']
    aihe = request.json['aihe']

    with open('users.json', 'r') as users:
        data = json.load(users)
    
    data[id]['aihe'] = aihe

    with open('users.json', 'w') as users:
        json.dump(data, users, indent=2)

    return data[id], 200