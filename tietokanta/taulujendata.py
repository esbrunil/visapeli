import random

class Taulujendata:
    def __init__(self, type, aihe, kysymys, oikea_vastaus, vve):
        self.type=type
        if(type=="multiple"):
            self.vastauksia=4
            self.oikea_vastaus=2
        else:
            self.vastauksia=2
            self.oikea_vastaus=int(eval(oikea_vastaus)) #2*O1 aikavaativuus
        self.aihe = aihe
        self.kysymys = kysymys
        #tietokantaa varten sekoitetaan vastausvaihtoehdot
        i = 0
        d = {}
        while i < len(vve):
            d.update({vve[i]:False})
            i += 1
        d.update({oikea_vastaus: True})
        l = list(d.items())
        random.shuffle(l)
        d=dict(l)
        self.vve = d
    
    def aihe(self) -> str:
        return self.aihe
    
    def vastauksia(self, value: int):
        self.vastauksia = value
    
    def vastauksia(self) -> int:
        return self.vastauksia
    
    def oikea_vastaus(self) -> int:
        return self.oikea_vastaus
    
    def kysymys(self) -> str:
        return self.kysymys
    
    def vve(self) -> dict:
        return self.vve
    
    def __repr__(self):
        return f"Taulujendata(type={self.type}, aihe={self.aihe}, kysymys={self.kysymys}, oikea_vastaus={self.oikea_vastaus}, vve={self.vve})"