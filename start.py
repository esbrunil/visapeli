# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, render_template, session, url_for
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def index():
    return render_template("jotain.html")