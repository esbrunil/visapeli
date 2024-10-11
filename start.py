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
@app.route('/annaID', methods=['GET'])
def annaID():
    id = None
    with open('users.json', 'r') as users:
        liveUsers = json.load(users)

    while True:
        varattu = False
        id = (str)(math.floor(time.time()))

        if id in liveUsers:
            varattu = True

        if not varattu:
            break

    liveUsers[id] = {"aihe": "history"}
    
    with open('users.json', 'w') as users:
        json.dump(liveUsers, users, indent=2)

    return id, 200


