from Stanje import Stanje


class Automat:
    def __init__(self):
        self.stanja = set()
        self.lijevo_stanje = self.dodaj_stanje()
        self.desno_stanje = self.dodaj_stanje()
        self.tren_stanje = set()
        self.tren_stanje.add(self.lijevo_stanje)

    def dodaj_stanje(self):
        stanje = Stanje(len(self.stanja))
        self.stanja.add(stanje)
        return stanje

    def dohvati_stanje(self, oznaka):
        for stanje in self.stanja:
            if stanje.oznaka == oznaka:
                return stanje
        return self.dodaj_stanje()

    def prihvati(self, znak):
        self.epsOkruzenje()
        self.prihvatiZnak(znak)
        self.epsOkruzenje()

        return self.desno_stanje in self.tren_stanje

    def epsOkruzenje(self):
        pom_stanja = set()
        while pom_stanja != self.tren_stanje:
            pom_stanja = self.tren_stanje
            for stanje in self.tren_stanje:
                if "eps" in stanje.susjedi.keys():
                    self.tren_stanje = self.tren_stanje.union(stanje.susjedi["eps"])

    def prihvatiZnak(self, znak):
        pom_stanja = set()
        for stanje in self.tren_stanje:
            if znak in stanje.susjedi.keys():
                pom_stanja = pom_stanja.union(stanje.susjedi[znak])
        self.tren_stanje = pom_stanja

    def povecajOznake(self, broj):
        for stanje in self.stanja:
            stanje.oznaka += broj
