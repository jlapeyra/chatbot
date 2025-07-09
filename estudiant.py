from dataclasses import dataclass
from enum import Enum
import json



@dataclass
class Estudiant:
    username:str
    titulacio:str
    fase_inicial:bool
    matriculades:list
    ects_superats:float

    def desc(self):
        fi = "en fase inicial" if self.fase_inicial else "amb la fase inicial superada"
        return f"estudiant de {self.titulacio} {fi} amb {self.ects_superats} ECTS superats, matriculat a {", ".join([m["sigles"] for m in self.matriculades])}"


with open('data/assignatures_detall.json', 'r', encoding='utf-8') as f:
    ASSIGNATURES = json.load(f)

def load_assig(titulacio, sigles_list):
    return [
        a
        for a in ASSIGNATURES
        if a.get('titulacio') == titulacio and a.get('sigles') in sigles_list
    ]

USUARI = Estudiant(
    username='aitor.tilla',
    titulacio='GEI',
    fase_inicial=True,
    ects_superats=0,
    matriculades='PRO1 IC FM F'.split()
)
USUARI.matriculades = load_assig(USUARI.titulacio, USUARI.matriculades)