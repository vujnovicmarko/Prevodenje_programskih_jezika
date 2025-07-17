class Cvor:
    def __init__(self, oznaka):
        self.oznaka = oznaka
        self.djeca = []

    def dodajDijete(self, dijete):
        if dijete not in self.djeca:
            self.djeca.append(dijete)
            return True
        return False

    def __str__(self):
        return self.oznaka

    def ispisiStablo(self, nivo=0):
        print(" " * nivo + str(self))
        for dijete in self.djeca:
            dijete.ispisiStablo(nivo + 1)
