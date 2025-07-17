from pomocne import *
import os


def generiraj():
    regex_def = {}
    stanja = []
    nazivi = []
    stanje_regex = {}
    stanje_automat = {}

    tablica_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "analizator/tablica.txt")
    )

    try:
        while True:
            linija = input()
            if linija[0] == "{":
                parsiraj_regex_def(linija, regex_def)
            elif linija[0:2] == "%X":
                parsiraj_listu(linija, stanja)
                for stanje in stanja:
                    stanje_regex[stanje] = []
                    stanje_automat[stanje] = []
            elif linija[0:2] == "%L":
                parsiraj_listu(linija, nazivi)
            else:
                parsiraj_pravila(linija, stanje_regex, regex_def)
    except EOFError:
        pass

    for stanje, rp_list in stanje_regex.items():
        for rp in rp_list:
            atm = regex_u_automat(rp[0])
            stanje_automat[stanje].extend([(atm, rp[1])])

    with open(tablica_path, "w") as tablica:
        tablica.write("%X ")
        for stanje in stanja:
            tablica.write(f"{stanje} ")

        tablica.write("\n%L ")
        for naziv in nazivi:
            tablica.write(f"{naziv} ")
        tablica.write("\n")

        for stanje in stanje_automat:
            for ap in stanje_automat[stanje]:
                tablica.write(stanje + ":" + ",".join(ap[1]) + "\n")
                tablica.write(repr(atm_u_tablica(ap[0])) + "\n")


if __name__ == "__main__":
    generiraj()
