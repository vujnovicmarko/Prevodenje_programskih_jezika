from NKA import NKA


class epsNKA:
    def __init__(self, stanja, prih_stanja, poc_stanje, slova, prijelazi):
        self.stanja = stanja
        self.prih_stanja = prih_stanja
        self.poc_stanje = poc_stanje
        self.slova = slova
        self.prijelazi = prijelazi

    def epsOkruzenje(self, stanja):
        pom_stanja = set()
        while pom_stanja != stanja:
            pom_stanja = stanja.copy()
            for s in pom_stanja:
                if "eps" in self.prijelazi[s]:
                    stanja = stanja.union(self.prijelazi[s]["eps"])
        return stanja

    def uNKA(self):
        prih_stanja = self.prih_stanja
        okruzenje = self.epsOkruzenje({self.poc_stanje})
        for ps in prih_stanja:
            if ps in okruzenje:
                prih_stanja = prih_stanja.union({self.poc_stanje})
                break

        slova = self.slova

        poc_stanje = set()
        poc_stanje.add(self.poc_stanje)
        poc_stanje = self.epsOkruzenje(poc_stanje)

        prijelazi = {}
        for stanje in self.stanja:
            prijelazi[stanje] = {}
            for slovo in slova:
                prijelazi[stanje][slovo] = set()
                okruzenje = self.epsOkruzenje({stanje})
                for pom_stanje in okruzenje:
                    prijelazi[stanje][slovo] = prijelazi[stanje][slovo].union(
                        self.epsOkruzenje(self.prijelazi[pom_stanje][slovo])
                    )

        return NKA(
            self.stanja,
            prih_stanja,
            poc_stanje,
            slova,
            prijelazi,
        )
