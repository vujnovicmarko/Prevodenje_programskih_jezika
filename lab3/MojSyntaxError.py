class MojSyntaxError(SyntaxError):
    def __init__(self, lijevo, desno):
        poruka = f"{lijevo} ::= {' '.join(desno)}"
        super().__init__(poruka)
        self.lijevo = lijevo
        self.desno = desno
