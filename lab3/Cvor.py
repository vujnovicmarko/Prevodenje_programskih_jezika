class Cvor:
    def __init__(self, oznaka):
        self.oznaka = oznaka
        self.djeca = []
        self.lizraz = False
        self.tip = ""
        self.tipovi = []
        self.ime = ""
        self.imena = []
        self.vrijednost = 0
        self.br_elem = 0
        self.pov = None
        self.parametri = []
        self.ntip = ""
        self.greska = False

    def dodajDijete(self, dijete):
        if dijete not in self.djeca:
            self.djeca.append(dijete)
            dijete.roditelj = self
            return True
        return False

    def __str__(self):
        return self.oznaka

    def ispisiStablo(self, nivo=0):
        print(" " * nivo + str(self))
        for dijete in self.djeca:
            dijete.ispisiStablo(nivo + 1)
