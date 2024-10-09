#!/home/rajuruok/public_html/cgi-bin/visapeli/venv/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
#from flask_cors import CORS
#import time, json, threading

app = Flask(__name__)
#CORS(app)

@app.route('/', methods=['GET'])
def index():
    return render_template("jotain.html")