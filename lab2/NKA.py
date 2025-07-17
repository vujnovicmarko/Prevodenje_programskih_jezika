from DKA import DKA
from pomocne import dohvatljivaStanja


class NKA:
    def __init__(self, stanja, prih_stanja, poc_stanje, slova, prijelazi):
        self.stanja = stanja
        self.prih_stanja = prih_stanja
        self.poc_stanje = poc_stanje
        self.slova = slova
        self.prijelazi = prijelazi

    def uDKA(self):
        poc_stanje = "[" + "|".join(sorted(list(self.poc_stanje))) + "]"

        stanja = dohvatljivaStanja(self.prijelazi, poc_stanje, self.slova)

        prih_stanja = set()
        for stanje in stanja:
            podstanje = stanje[1:-1].split("|")
            for s in self.prih_stanja:
                if s in podstanje:
                    prih_stanja.add(stanje)
                    break

        prijelazi = {}
        for stanje in stanja:
            prijelazi[stanje] = {}
            for slovo in self.slova:
                if stanje == "[]":
                    prijelazi[stanje][slovo] = "[]"
                    continue
                prijelazi[stanje][slovo] = set()
                podstanje = stanje[1:-1].split("|")
                for ps in podstanje:
                    prijelazi[stanje][slovo] = prijelazi[stanje][slovo].union(
                        self.prijelazi[ps][slovo]
                    )
                prijelazi[stanje][slovo] = (
                    "[" + "|".join(sorted(list(prijelazi[stanje][slovo]))) + "]"
                )

        return DKA(stanja, prih_stanja, poc_stanje, self.slova, prijelazi)
