import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pomocne import *


def analiziraj():
    stanja = []
    nazivi = []
    tablica_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "tablica.txt")
    )
    stanje_automat = {}

    with open(tablica_path, "r") as tablica_datoteka:
        linija = tablica_datoteka.readline()
        while linija:
            if linija[0:2] == "%X":
                parsiraj_listu(linija, stanja)
                for stanje in stanja:
                    stanje_automat[stanje] = []
            elif linija[0:2] == "%L":
                parsiraj_listu(linija, nazivi)
            else:
                linija = linija.split(":")
                stanje, args = linija[0], linija[1]
                args = args.strip().split(",")

                linija = tablica_datoteka.readline()
                tablica = eval(linija)
                atm = tablica_u_atm(tablica)
                stanje_automat[stanje].extend([(atm, args)])

            linija = tablica_datoteka.readline()

    for stanje in stanje_automat:
        stanje_automat[stanje].reverse()

    tren_stanje = stanja[0]
    tren_linija = 1
    prvi = 0
    zadnji = 0
    kraj = 0
    prihvatljiva = []
    args = []
    ulaz = sys.stdin.read()

    while prvi < len(ulaz) - 1:
        znak = ulaz[kraj]
        if not prihvatljiva:
            prihvatljiva = [True for _ in range(len(stanje_automat[tren_stanje]))]

        for i, ap in enumerate(stanje_automat[tren_stanje]):
            if not prihvatljiva[i]:
                continue
            atm = ap[0]

            if atm.prihvati(znak):
                args = ap[1]
                zadnji = kraj

            if len(atm.tren_stanje) == 0:
                prihvatljiva[i] = False

            if not any(prihvatljiva) or kraj == len(ulaz) - 1:
                postavi_automate(stanje_automat[tren_stanje])
                prihvatljiva = []
                if args:
                    znakovi = ulaz[prvi : zadnji + 1]

                    if args[0] == "-":
                        uni_jed = ""
                    else:
                        uni_jed = args[0]

                    for arg in args:
                        if arg.startswith("VRATI_SE"):
                            broj = int(arg.split(" ")[1])
                            odmak = len(znakovi) - broj
                            zadnji = zadnji - odmak
                            znakovi = znakovi[:broj]

                    if uni_jed != "":
                        print(f"{uni_jed} {tren_linija} {znakovi}")

                    for arg in args:
                        if arg == "NOVI_REDAK":
                            tren_linija = tren_linija + 1
                        elif arg.startswith("UDJI_U_STANJE"):
                            tren_stanje = arg.split(" ")[1]

                    prvi = zadnji + 1
                    kraj = zadnji
                    args = []
                    break

                else:
                    print(f"{ulaz[prvi]}", file=sys.stderr)
                    kraj = prvi
                    prvi = prvi + 1
                    break

        kraj = kraj + 1


if __name__ == "__main__":
    analiziraj()
