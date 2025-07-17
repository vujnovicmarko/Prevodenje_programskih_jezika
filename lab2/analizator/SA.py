import sys
import os
from Cvor import Cvor


def analiziraj():
    sinkronizacijski_znakovi = None
    poc_stanje = None
    akcija = None
    novoStanje = None
    tablica_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "tablica.txt")
    )

    leksicke_jedinke = []
    ulaz = sys.stdin.readlines()

    for linija in ulaz:
        praznina1 = linija.find(" ")
        uni = linija[:praznina1]
        praznina2 = linija.find(" ", praznina1 + 1)
        redak = linija[praznina1 + 1 : praznina2]
        znakovi = linija[praznina2 + 1 : -1]
        leksicke_jedinke.append((uni, redak, znakovi))

    with open(tablica_path, "r") as tablica:
        sinkronizacijski_znakovi = eval(tablica.readline())
        poc_stanje = tablica.readline()
        akcija = eval(tablica.readline())
        novoStanje = eval(tablica.readline())

    index = 0
    leksicke_jedinke.append(("&", "0", "&"))
    stog = []
    stog.append("kraj")
    stog.append(poc_stanje[:-1])
    stablo = []

    while index < len(leksicke_jedinke):
        tren_stanje = stog[-1]
        slovo = leksicke_jedinke[index][0]
        naredba = akcija[tren_stanje][slovo]
        zagrada = naredba.find("(")
        arg = naredba[zagrada + 1 : -1]

        if naredba.startswith("Pomakni"):
            stog.append(slovo)
            stablo.append(Cvor(" ".join(leksicke_jedinke[index])))
            stog.append(arg)
            index = index + 1
        elif naredba.startswith("Reduciraj"):
            crtica = arg.find("-")
            lijevo, desno = arg[:crtica], arg[crtica + 2 :]
            if desno == "$":
                r = 0
                djete = Cvor(desno)
                unutrasnji_cvor = Cvor(lijevo)
                unutrasnji_cvor.dodajDijete(djete)
                stablo.append(unutrasnji_cvor)
            else:
                desno = desno.split(" ")
                r = len(desno) * 2
                unutrasnji_cvor = Cvor(lijevo)
                djeca = stablo[-(r // 2) :]
                for dijete in djeca:
                    unutrasnji_cvor.dodajDijete(dijete)
                stablo = stablo[: -(r // 2)]
                stablo.append(unutrasnji_cvor)

                stog = stog[:-r]

            tren_stanje = stog[-1]
            stog.append(lijevo)
            slj_stanje = novoStanje[tren_stanje][lijevo][6:-1]
            stog.append(slj_stanje)
        elif naredba == "Odbaci()":
            print("Pogreska u retku " + leksicke_jedinke[index][1], file=sys.stderr)
            ocekivani_znakovi = []
            for s in akcija[tren_stanje]:
                if not akcija[tren_stanje][s].startswith("Odbaci"):
                    ocekivani_znakovi.append(s)

            print(
                "Znakovi koji nebi izazvali pogresku: " + str(ocekivani_znakovi),
                file=sys.stderr,
            )

            print(
                "Procitani uniformi znak: " + leksicke_jedinke[index][0],
                file=sys.stderr,
            )
            print(
                "Znakovni prikaz u izvornom kodu programa: "
                + leksicke_jedinke[index][2],
                file=sys.stderr,
            )

            while slovo not in sinkronizacijski_znakovi:
                index = index + 1
                slovo = leksicke_jedinke[index][0]

            while akcija[tren_stanje][slovo].startswith("Odbaci"):
                stog = stog[:-2]
                stablo = stablo[:-1]
                tren_stanje = stog[-1]

        elif naredba == "Prihvati()":
            stablo[0].ispisiStablo()
            break


if __name__ == "__main__":
    analiziraj()
