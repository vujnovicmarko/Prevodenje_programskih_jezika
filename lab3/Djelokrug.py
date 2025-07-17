class Djelokrug:
    def __init__(self):
        self.roditelj = None
        self.tablica_znakova = {}
        self.tablica_funkcija = {}
        self.definirane_funkcije = []
        self.pov = None
        self.parametri = []
        self.petlja = False

    def deklarirajIdentifikator(self, idn, tip, vrijednost):
        if idn not in self.tablica_znakova:
            self.tablica_znakova[idn] = (tip, vrijednost)
            return True
        return False

    def deklarirajFunkciju(self, idn, parametri, pov):
        if idn not in self.tablica_funkcija:
            self.tablica_funkcija[idn] = set()
        self.tablica_funkcija[idn].add((parametri, pov))

    def definirajFunkciju(self, idn, parametri, pov):
        self.deklarirajFunkciju(idn, parametri, pov)
        self.definirane_funkcije.append(idn)
