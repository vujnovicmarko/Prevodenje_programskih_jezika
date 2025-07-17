import sys
from pomocne import *
from epsNKA import epsNKA
import os


def generiraj():
    nezavrsni_znakovi = []
    zavrsni_znakovi = []
    sinkronizacijski_znakovi = []
    produkcije = {}
    nezavrsni_z = None

    tablica_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "analizator/tablica.txt")
    )

    ulaz = sys.stdin.read()
    for linija in ulaz.splitlines():
        if linija[0:2] == "%V":
            parsiraj_listu(linija, nezavrsni_znakovi)
        elif linija[0:2] == "%T":
            parsiraj_listu(linija, zavrsni_znakovi)
        elif linija[0:4] == "%Syn":
            parsiraj_listu(linija, sinkronizacijski_znakovi)
        else:
            if linija[0] == "<":
                nezavrsni_z = linija
                if nezavrsni_z not in produkcije:
                    produkcije[nezavrsni_z] = []
            else:
                produkcije[nezavrsni_z].append(linija[1:])

    produkcije["<'>"] = [nezavrsni_znakovi[0]]
    nezavrsni_znakovi.insert(0, "<'>")

    prazniZnakovi = napraviPrazneZnakove(produkcije)
    sviZnakovi = nezavrsni_znakovi + zavrsni_znakovi
    zapocinjeTablica = napraviZapocinje(
        nezavrsni_znakovi, sviZnakovi, produkcije, prazniZnakovi
    )

    zapocinjeTablica = tranzitivno(zapocinjeTablica, sviZnakovi)

    zapocinjeSkupovi = {}
    for z in sviZnakovi:
        zapocinjeSkupovi[z] = zapocinje(z, zapocinjeTablica, zavrsni_znakovi)

    slova = set(nezavrsni_znakovi).union(set(zavrsni_znakovi))
    poc_stanje = "<'>->. " + nezavrsni_znakovi[1] + ",{&}"

    prijelazi, LR_stavke = napraviPrijelaze(
        poc_stanje,
        produkcije,
        zapocinjeSkupovi,
        prazniZnakovi,
        nezavrsni_znakovi,
        slova,
    )

    epsNka = epsNKA(LR_stavke, LR_stavke, poc_stanje, slova, prijelazi)

    dka = epsNka.uNKA().uDKA()

    zavrsni_znakovi.append("&")
    akcija = {}
    novoStanje = {}
    for stanje in dka.stanja:
        novoStanje[stanje] = {}
        akcija[stanje] = {}
        for zz in zavrsni_znakovi:
            akcija[stanje][zz] = "Odbaci()"
        for nz in nezavrsni_znakovi:
            novoStanje[stanje][nz] = "Odbaci()"

    for stanje in dka.stanja:
        stavke = stanje[1:-1].split("|")
        naredbe = {}
        for zz in zavrsni_znakovi:
            naredbe[zz] = set()

        for stavka in stavke:
            if stavka == "<'>->" + nezavrsni_znakovi[1] + " .,{&}":
                akcija[stanje]["&"] = "Prihvati()"
                continue

            c, z = stavka.find("-"), stavka.find(",")
            lijevo, desno, znakovi = (
                stavka[:c],
                stavka[c + 2 : z],
                stavka[z + 2 : -1],
            )
            desno, znakovi = desno.split(" "), znakovi.split(",")
            tocka = desno.index(".")

            if tocka == len(desno) - 1:
                for zz in znakovi:
                    if desno[:-1] != []:
                        naredbe[zz].add(
                            "Reduciraj(" + lijevo + "->" + " ".join(desno[:-1]) + ")"
                        )
                    else:
                        naredbe[zz].add("Reduciraj(" + lijevo + "->$)")
            else:
                slj_znak = desno[tocka + 1]
                prijelaz = dka.prijelazi[stanje][slj_znak]
                if slj_znak in zavrsni_znakovi and prijelaz != "[]":
                    naredbe[slj_znak].add("Pomakni(" + prijelaz + ")")

        for zz in zavrsni_znakovi:
            if akcija[stanje][zz] == "Odbaci()":
                if len(naredbe[zz]) == 1:
                    akcija[stanje][zz] = naredbe[zz].pop()
                elif naredbe[zz] != set():
                    min_index = len(ulaz)
                    for naredba in naredbe[zz]:
                        if naredba.startswith("Pomakni"):
                            akcija[stanje][zz] = naredba
                            break
                        else:
                            index = pronadiProdukciju(naredba, ulaz)
                            if index < min_index:
                                min_index = index
                                akcija[stanje][zz] = naredba
                    print("Doslo je do proturjecja", file=sys.stderr)
                    print("Moguce naredbe: " + str(naredbe), file=sys.stderr)
                    print(
                        "Odabrana naredba: " + str(akcija[stanje][zz]), file=sys.stderr
                    )

    for stanje in dka.stanja:
        for nz in nezavrsni_znakovi:
            prijelaz = dka.prijelazi[stanje][nz]
            if prijelaz != "[]":
                novoStanje[stanje][nz] = "Stavi(" + prijelaz + ")"

    with open(tablica_path, "w") as tablica:
        tablica.write(str(sinkronizacijski_znakovi))
        tablica.write("\n")
        tablica.write(dka.poc_stanje)
        tablica.write("\n")
        tablica.write(str(akcija))
        tablica.write("\n")
        tablica.write(str(novoStanje))


if __name__ == "__main__":
    generiraj()
