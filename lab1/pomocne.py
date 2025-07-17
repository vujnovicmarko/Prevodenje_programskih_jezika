from Automat import Automat


def parsiraj_regex_def(linija, regex_def):
    naziv, regex = linija.split(" ")
    naziv = naziv[1:-1]
    regex = reduciraj_regex(regex, regex_def)
    regex_def[naziv] = regex


def reduciraj_regex(regex, regex_def):
    for n in regex_def:
        ref = "{" + n + "}"
        indeks = 0
        while indeks != -1:
            indeks = regex.find(ref)
            if indeks == -1 or not je_operator(regex, indeks):
                continue
            else:
                regex = (
                    regex[:indeks]
                    + "("
                    + regex_def[n]
                    + ")"
                    + regex[indeks + len(ref) :]
                )
    return regex


def parsiraj_listu(linija, lst):
    linija = linija.split(" ")[1:]
    lst.extend(linija)


def parsiraj_pravila(linija, stanje_regex, regex_def):
    indeks = linija.find(">")
    stanje, regex = linija[1:indeks], linija[indeks + 1 :]
    regex = reduciraj_regex(regex, regex_def)

    linija = input()
    linija = input()
    pravila = []
    while linija != "}":
        pravila.append(linija)
        linija = input()
    stanje_regex[stanje].extend([(regex, pravila)])


def je_operator(regex, indeks):
    brojac = 0
    while indeks - 1 >= 0 and regex[indeks - 1] == "\\":
        brojac = brojac + 1
        indeks = indeks - 1
    return brojac % 2 == 0


def regex_u_automat(regex):
    izbori = []
    br_zagrada = 0
    pomocna = 0
    for indeks in range(len(regex)):
        if regex[indeks] == "(" and je_operator(regex, indeks):
            br_zagrada = br_zagrada + 1
        elif regex[indeks] == ")" and je_operator(regex, indeks):
            br_zagrada = br_zagrada - 1
        elif br_zagrada == 0 and regex[indeks] == "|" and je_operator(regex, indeks):
            izbori.append(regex[pomocna:indeks])
            pomocna = indeks + 1
    if izbori:
        izbori.append(regex[pomocna:])

    automat = Automat()
    lijevo_stanje = automat.lijevo_stanje
    desno_stanje = automat.desno_stanje

    if izbori:
        for izbor in izbori:
            pom_automat = regex_u_automat(izbor)
            pom_automat.povecajOznake(len(automat.stanja))
            for pom_stanje in pom_automat.stanja:
                automat.stanja.add(pom_stanje)
            automat.lijevo_stanje.dodaj_epsilon_prijelaz(pom_automat.lijevo_stanje)
            pom_automat.desno_stanje.dodaj_epsilon_prijelaz(automat.desno_stanje)

    else:
        prefiks = False
        zadnje_stanje = lijevo_stanje
        indeks = 0
        while indeks < len(regex):
            a, b = None, None
            if prefiks:
                prefiks = False
                prijelazni_znak = None
                if regex[indeks] == "t":
                    prijelazni_znak = "\t"
                elif regex[indeks] == "n":
                    prijelazni_znak = "\n"
                elif regex[indeks] == "_":
                    prijelazni_znak = " "
                else:
                    prijelazni_znak = regex[indeks]

                a = automat.dodaj_stanje()
                b = automat.dodaj_stanje()
                a.dodaj_prijelaz(b, prijelazni_znak)
            else:
                if regex[indeks] == "\\":
                    prefiks = True
                    indeks = indeks + 1
                    continue

                if regex[indeks] != "(":
                    a = automat.dodaj_stanje()
                    b = automat.dodaj_stanje()
                    if regex[indeks] == "$":
                        a.dodaj_epsilon_prijelaz(b)
                    else:
                        a.dodaj_prijelaz(b, regex[indeks])
                else:
                    j = 0
                    br_zagrada = 0
                    for i in range(len(regex[indeks:])):
                        if regex[indeks + i] == "(" and je_operator(regex, indeks + i):
                            br_zagrada = br_zagrada + 1
                        elif regex[indeks + i] == ")" and je_operator(
                            regex, indeks + i
                        ):
                            br_zagrada = br_zagrada - 1
                            if br_zagrada == 0:
                                j = indeks + i
                                break

                    pom_automat = regex_u_automat(regex[indeks + 1 : j])
                    pom_automat.povecajOznake(len(automat.stanja))
                    for pom_stanje in pom_automat.stanja:
                        automat.stanja.add(pom_stanje)
                    a = pom_automat.lijevo_stanje
                    b = pom_automat.desno_stanje
                    indeks = j

            if indeks + 1 < len(regex) and regex[indeks + 1] == "*":
                x = a
                y = b
                a = automat.dodaj_stanje()
                b = automat.dodaj_stanje()
                a.dodaj_epsilon_prijelaz(x)
                y.dodaj_epsilon_prijelaz(b)
                a.dodaj_epsilon_prijelaz(b)
                y.dodaj_epsilon_prijelaz(x)
                indeks = indeks + 1

            zadnje_stanje.dodaj_epsilon_prijelaz(a)
            zadnje_stanje = b

            indeks = indeks + 1

        zadnje_stanje.dodaj_epsilon_prijelaz(desno_stanje)

    return automat


def atm_u_tablica(atm):
    tablica = [{} for _ in range(len(atm.stanja))]
    for stanje in atm.stanja:
        for znak in stanje.susjedi:
            tablica[stanje.oznaka][znak] = set()
            for susjed in stanje.susjedi[znak]:
                tablica[stanje.oznaka][znak].add(susjed.oznaka)
    return tablica


def tablica_u_atm(tablica):
    atm = Automat()
    for _ in range(len(tablica) - 2):
        atm.dodaj_stanje()

    for indeks, prijelazi in enumerate(tablica):
        stanje = atm.dohvati_stanje(indeks)
        for znak, susjedi in prijelazi.items():
            for susjed in susjedi:
                stanje.dodaj_prijelaz(atm.dohvati_stanje(susjed), znak)

    return atm


def postavi_automate(aps):
    for ap in aps:
        atm = ap[0]
        atm.tren_stanje = set()
        atm.tren_stanje.add(atm.lijevo_stanje)
