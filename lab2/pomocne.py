import queue


def parsiraj_listu(linije, lst):
    linije = linije.split(" ")[1:]
    lst.extend(linije)


def dohvatljivaStanja(prijelazi, poc_stanje, sviZnakovi):
    rezultat = set()
    rezultat.add(poc_stanje)
    q = queue.Queue()
    q.put(poc_stanje)

    while not q.empty():
        stanje = q.get()
        stanje = stanje[1:-1].split("|")
        for slovo in sviZnakovi:
            slj_stanja = set()
            for s in stanje:
                slj_stanja = slj_stanja.union(prijelazi[s][slovo])
            slj_stanja = "[" + "|".join(sorted(list(slj_stanja))) + "]"
            if slj_stanja not in rezultat and slj_stanja != "[]":
                rezultat.add(slj_stanja)
                q.put(slj_stanja)

    return rezultat


def pronadiProdukciju(naredba, ulaz):
    lz, dz = naredba.find("("), naredba.find(")")
    naredba = naredba[lz + 1 : dz]
    c = naredba.find("-")
    lijevo, desno = naredba[:c], naredba[c + 2 :]
    produkcija = lijevo + "\n " + desno
    return ulaz.find(produkcija)


def sastavljenaOd(niz, znakovi):
    for znak in niz:
        if znak not in znakovi:
            return False
    return True


def napraviPrazneZnakove(produkcije):
    prazniZnakovi = []
    for lijevo in produkcije:
        for desno in produkcije[lijevo]:
            if desno == "$":
                prazniZnakovi.append(lijevo)

    pom_lst = []
    while pom_lst != prazniZnakovi:
        pom_lst = prazniZnakovi.copy()
        for lijevo in produkcije:
            for desno in produkcije[lijevo]:
                if sastavljenaOd(desno, prazniZnakovi):
                    prazniZnakovi.append(lijevo)

    return prazniZnakovi


def zapocinjeIzravnoZnakovima(nz, produkcije, prazniZnakovi):
    izravniZnakovi = set()
    for desno in produkcije[nz]:
        znakovi = desno.split(" ")
        for i in range(len(znakovi)):
            if i == 0:
                izravniZnakovi.add(znakovi[i])
            else:
                if znakovi[i - 1] in prazniZnakovi:
                    izravniZnakovi.add(znakovi[i])
                else:
                    break

    return izravniZnakovi


def napraviZapocinje(nezavrsni_znakovi, sviZnakovi, produkcije, prazniZnakovi):
    zapocinjeTablica = {}

    for z in sviZnakovi:
        if z == "<struct_lista_deklaratora>":
            pass
        zapocinjeTablica[z] = {}
        if z not in nezavrsni_znakovi:
            izravniZnakovi = {z}
        else:
            izravniZnakovi = zapocinjeIzravnoZnakovima(z, produkcije, prazniZnakovi)
        for sz in sviZnakovi:
            if sz in izravniZnakovi:
                zapocinjeTablica[z][sz] = 1
            else:
                zapocinjeTablica[z][sz] = 0

    return zapocinjeTablica


def tranzitivno(zapocinjeTablica, sviZnakovi):
    for i in sviZnakovi:
        zapocinjeTablica[i][i] = 1
        for z in sviZnakovi:
            for j in sviZnakovi:
                if zapocinjeTablica[z][i] == 1 and zapocinjeTablica[i][j] == 1:
                    zapocinjeTablica[z][j] = 1

    return zapocinjeTablica


def zapocinje(z, zapocinjeTablica, zavrsni_znakovi):
    rez = set()
    for zz in zavrsni_znakovi:
        if zapocinjeTablica[z][zz] == 1:
            rez.add(zz)
    return rez


def napraviPrijelaze(
    poc_stanje,
    produkcije,
    zapocinjeSkupovi,
    prazniZnakovi,
    nezavrsni_znakovi,
    slova,
):
    prijelazi = {}
    LR_stavke = set()
    q = queue.Queue()
    q.put(poc_stanje)

    while not q.empty():
        stavka = q.get()
        LR_stavke.add(stavka)
        if stavka.startswith("<struct_deklaracija>"):
            pass
        if stavka not in prijelazi:
            prijelazi[stavka] = {}
            for s in slova:
                prijelazi[stavka][s] = set()
            prijelazi[stavka]["eps"] = set()
        c, z = stavka.find("-"), stavka.find(",")
        lijevo, desno, znakovi = stavka[:c], stavka[c + 2 : z], stavka[z + 2 : -1]
        desno, znakovi = desno.split(" "), znakovi.split(",")
        tocka = desno.index(".")
        slj_znak = None

        if tocka == len(desno) - 1:
            continue
        else:
            slj_znak = desno[tocka + 1]
            if slj_znak in nezavrsni_znakovi:
                desno_od_slj_znaka = desno[tocka + 2 :]
                zapocinjeZnakovima = set()
                prazno = True

                for sz in desno_od_slj_znaka:
                    zapocinjeZnakovima = zapocinjeZnakovima.union(zapocinjeSkupovi[sz])
                    if "&" not in zapocinjeSkupovi[sz]:
                        break

                for sz in desno_od_slj_znaka:
                    if sz not in prazniZnakovi:
                        prazno = False
                        break

                if prazno:
                    zapocinjeZnakovima = zapocinjeZnakovima.union(znakovi)

                for desno_prod in produkcije[slj_znak]:
                    if desno_prod == "$":
                        slj_stavka = (
                            slj_znak
                            + "->.,{"
                            + ",".join(sorted(list(zapocinjeZnakovima)))
                            + "}"
                        )
                        prijelazi[stavka]["eps"].add(slj_stavka)
                        if slj_stavka not in LR_stavke:
                            q.put(slj_stavka)
                    else:
                        slj_stavka = (
                            slj_znak
                            + "->. "
                            + desno_prod
                            + ",{"
                            + ",".join(sorted(list(zapocinjeZnakovima)))
                            + "}"
                        )
                        prijelazi[stavka]["eps"].add(slj_stavka)
                        if slj_stavka not in LR_stavke:
                            q.put(slj_stavka)

        desno[tocka], desno[tocka + 1] = desno[tocka + 1], desno[tocka]
        slj_stavka = (
            lijevo + "->" + " ".join(desno) + ",{" + ",".join(sorted(znakovi)) + "}"
        )
        prijelazi[stavka][slj_znak].add(slj_stavka)
        if slj_stavka not in LR_stavke:
            q.put(slj_stavka)

    return prijelazi, LR_stavke
