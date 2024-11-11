#!../visapeli-venv/venv/bin/python

import requests, json, sys

aiheet = {
    "historia": "&category=23",
    "yleistieto": "&category=9",
    "maantieto": "&category=22"
}

RED = '\033[31m'
GREEN = '\033[32m'
WARNING = '\033[93m'
BLUE = '\033[34m'
RESET = '\033[0m'

def main():

    if len(sys.argv) > 2:
        print("Kirjoita korkeitaan yksi aihe")
        return
    
    elif len(sys.argv) == 2:
        if (sys.argv[1].lower() not in aiheet):
            print("Virheellinen aihe")
            return
       
        aihe = aiheet[sys.argv[1].lower()]

    elif len(sys.argv) == 1:
        aihe = ""

    if aihe == "":
        print("\n Haetaan 50 kysymystä mistä vaan aiheesta...")
    else:
        print("Haetaan 50 kysymystä aiheesta " + sys.argv[1].lower() + "...")

    url = 'https://opentdb.com/api.php?amount=10' + aihe

    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response if it was successful
        data = response.json()
        print("Datan haku onnistui... \n")
    else:
        print(f"{RED}Datan haku epäonnistui: {RESET}", response.status_code)

    with open('apiKysymykset.json', 'r') as tk:
        file_data = json.load(tk)

    for item in data['results']:
        if (item in file_data):
            print(f"{WARNING} kohde on jo datassa, ohitetaan {item}{RESET} \n")
            continue
        file_data.append(item)

    with open('apiKysymykset.json', 'w') as tk:
        json.dump(file_data, tk, indent=2)

    print(f"{GREEN}Data päivitetty{RESET}")

if __name__ == '__main__':
    main()