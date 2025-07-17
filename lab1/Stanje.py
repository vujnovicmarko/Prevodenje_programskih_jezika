class Stanje:
    def __init__(self, oznaka, susjedi=None):
        self.oznaka = oznaka
        self.susjedi = susjedi if susjedi is not None else {}

    def dodaj_prijelaz(self, drugo, znak):
        if znak not in self.susjedi:
            self.susjedi[znak] = set()

        self.susjedi[znak].add(drugo)

    def dodaj_epsilon_prijelaz(self, drugo):
        self.dodaj_prijelaz(drugo, "eps")

    def __eq__(self, drugo):
        if isinstance(drugo, Stanje):
            return self.oznaka == drugo.oznaka
        return False

    def __hash__(self):
        return hash(self.oznaka)
