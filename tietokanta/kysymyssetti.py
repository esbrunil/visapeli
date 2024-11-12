import json, random
from taulujendata import Taulujendata

class Kysymyssetti:
    def __init__(self, json_data):
        self.kysymykset = []
        self.lataa_kysymyset(json_data)

    def lataa_kysymyset(self, json_data):
        for item in json_data:
            kysymys = Taulujendata(
                type=item.get('type'),
                aihe=item.get('category'),
                kysymys=item.get('question'),
                oikea_vastaus=item.get('correct_answer'),
                vve=item.get('incorrect_answers', [])
            )
            self.kysymykset.append(kysymys)

    def __repr__(self):
        return f"QuestionSet(kysymykset={self.kysymykset})"

if __name__ == "__main__":
    with open('./Visapeli/tietokanta/pk.json', 'r') as kysym:
        data = json.load(kysym)
    ksetti = Kysymyssetti(data)

    for kysymys in ksetti.kysymykset:
        print(kysymys)
        print(kysymys.vastauksia)