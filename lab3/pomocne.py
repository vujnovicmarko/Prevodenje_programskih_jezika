from Cvor import Cvor
from Djelokrug import Djelokrug

def parsirajProdukcije(ulaz):
    ulaz = ulaz.replace("\n\t", " ")
    produkcije = {}
    for linija in ulaz.splitlines():
        lijevo, desno = linija.split(" ::= ")
        desno = desno.split(" | ")
        produkcije[lijevo] = desno

    return produkcije


def parsirajStablo(linije, nivo=1):
    cvor = Cvor(linije[0].strip())

    if len(linije) == 1:
        return cvor

    linije = linije[1:]
    indeksi_djece = []

    for i, linija in enumerate(linije):
        if linija[:nivo].strip() == "" and linija[nivo] != " ":
            indeksi_djece.append(i)

    for indeks in range(len(indeksi_djece)):
        if indeks == len(indeksi_djece) - 1:
            cvor.dodajDijete(
                parsirajStablo(
                    linije[indeksi_djece[indeks] :],
                    nivo + 1,
                )
            )
        else:
            cvor.dodajDijete(
                parsirajStablo(
                    linije[indeksi_djece[indeks] : indeksi_djece[indeks + 1]],
                    nivo + 1,
                )
            )

    return cvor

def jeDeklariran(idn, djelokrug):
    if idn in djelokrug.tablica_znakova or idn in djelokrug.tablica_funkcija:
        return djelokrug
    elif djelokrug.roditelj:
        return jeDeklariran(idn, djelokrug.roditelj)
    else:
        return False

def uPetlji(djelokrug):
    if djelokrug.petlja:
        return True
    elif djelokrug.roditelj:
        return uPetlji(djelokrug.roditelj)
    else:
        return False

def povFunkcije(djelokrug):
    if djelokrug.pov:
        return djelokrug.pov
    elif djelokrug.roditelj:
        return povFunkcije(djelokrug.roditelj)
    else:
        return None

def postojiFunkcija(ime, djelokrug):
    if ime in djelokrug.definirane_funkcije:
        return True
    elif djelokrug.roditelj:
        return postojiFunkcija(ime, djelokrug.roditelj)
    else:
        return False

def dohvatiGlobalni(djelokrug):
    if djelokrug.roditelj:
        return dohvatiGlobalni(djelokrug.roditelj)
    else:
        return djelokrug

def noviDjelokrug(djelokrug):
    novi = Djelokrug()
    novi.roditelj = djelokrug
    return novi

def zavrsniCvor(cvor):
    if cvor.djeca:
        return zavrsniCvor(cvor.djeca[0])
    else:
        return cvor

def provjeriPrefiks(znak):
    if znak == "\\n":
        return True
    elif znak == "\\t":
        return True
    elif znak == "\\0":
        return True
    elif znak == "\\'":
        return True
    elif znak == '\\"':
        return True
    elif znak == "\\\\":
        return True
    else:
        return False

def jednako(cvor_tip, pravilo_tip):
    if "X" in pravilo_tip:
        return jednako(cvor_tip, pravilo_tip.replace("X", "T")) or jednako(cvor_tip, pravilo_tip.replace("X", "const.T"))
    if "T" in pravilo_tip:
        return jednako(cvor_tip, pravilo_tip.replace("T", "int")) or jednako(cvor_tip, pravilo_tip.replace("T", "char"))

    return cvor_tip == pravilo_tip


def svodljiv(cvor_tip, pravilo_tip):
    if "X" in pravilo_tip:
        return svodljiv(cvor_tip, pravilo_tip.replace("X", "T")) or svodljiv(cvor_tip, pravilo_tip.replace("X", "const.T"))
    if "T" in pravilo_tip:
        return svodljiv(cvor_tip, pravilo_tip.replace("T", "int")) or svodljiv(cvor_tip, pravilo_tip.replace("T", "char"))
    if cvor_tip == pravilo_tip:
        return True
    if cvor_tip == "int" and pravilo_tip == "const.int" or cvor_tip == "const.int" and pravilo_tip == "int":
        return True
    if cvor_tip == "char" and pravilo_tip == "const.char" or cvor_tip == "const.char" and pravilo_tip == "char":
        return True
    if cvor_tip == "char" and pravilo_tip == "int":
        return True
    if cvor_tip == "niz.int" and pravilo_tip == "niz.const.int" or cvor_tip == "niz.char" and pravilo_tip == "niz.const.char":
        return True

    return False

def intUChar(cvor):
    if cvor.tip != "int" and cvor.tip != "const.int":
        return False

    if 0 <= cvor.vrijednost <= 255:
        return True

    return False
