#!../visapeli-venv/venv/bin/python
# -*- coding: utf-8 -*-
# suorittaa Flask-sovellukset CGI-ohjelmina users.jyu.fi-palvelimella
import sys
from wsgiref.handlers import CGIHandler
from werkzeug.debug import DebuggedApplication

try:
  from start import app as application

  if __name__ == '__main__':
         handler = CGIHandler()
         application.debug = True
         handler.run(DebuggedApplication(application))

except:
  print("Content-Type: text/plain;charset=UTF-8\n")
  print("Syntaksivirhe:\n")
  for err in sys.exc_info():
        print(err)