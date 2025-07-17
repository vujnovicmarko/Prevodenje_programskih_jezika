from MojSyntaxError import MojSyntaxError
from pomocne import *

def provjeri(cvor, djelokrug):
    lijevo = cvor.oznaka

    if not lijevo.startswith("<") or not lijevo.endswith(">"):
        r1 = lijevo.find(" ")
        r2 = lijevo.find(" ", r1 + 1)
        zavrsni_znak, redak, znakovi = (
            lijevo[:r1],
            lijevo[r1 + 1 : r2],
            lijevo[r2 + 1 :],
        )

        if zavrsni_znak == "IDN":
            idn(znakovi, cvor, djelokrug)
        elif zavrsni_znak == "BROJ":
            broj(znakovi, cvor, djelokrug)
        elif zavrsni_znak == "ZNAK":
            znak(znakovi, cvor, djelokrug)
        elif zavrsni_znak == "NIZ_ZNAKOVA":
            nizZnakova(znakovi, cvor, djelokrug)
        else:
            raise SyntaxError
        return

    desno = []
    for dijete in cvor.djeca:
        if not dijete.oznaka.startswith("<") or not dijete.oznaka.endswith(">"):
            r1 = dijete.oznaka.find(" ")
            r2 = dijete.oznaka.find(" ", r1 + 1)

            zavrsni_znak, redak, znakovi = (
                dijete.oznaka[:r1],
                dijete.oznaka[r1 + 1 : r2],
                dijete.oznaka[r2 + 1 :],
            )

            desno.append(f"{zavrsni_znak}({redak},{znakovi})")
        else:
            desno.append(dijete.oznaka)

    try:
        if lijevo == "<primarni_izraz>":
            primarniIzraz(cvor, djelokrug)
        elif lijevo == "<postfiks_izraz>":
            postfiksIzraz(cvor, djelokrug)
        elif lijevo == "<lista_argumenata>":
            listaArgumenata(cvor, djelokrug)
        elif lijevo == "<unarni_izraz>":
            unarniIzraz(cvor, djelokrug)
        elif lijevo == "<unarni_operator>":
            pass
        elif lijevo == "<cast_izraz>":
            castIzraz(cvor, djelokrug)
        elif lijevo == "<ime_tipa>":
            imeTipa(cvor, djelokrug)
        elif lijevo == "<specifikator_tipa>":
            specifikatorTipa(cvor, djelokrug)
        elif lijevo == "<multiplikativni_izraz>":
            multiplikativniIzraz(cvor, djelokrug)
        elif lijevo == "<aditivni_izraz>":
            aditivniIzraz(cvor, djelokrug)
        elif lijevo == "<odnosni_izraz>":
            odnosniIzraz(cvor, djelokrug)
        elif lijevo == "<jednakosni_izraz>":
            jednakosniIzraz(cvor, djelokrug)
        elif lijevo == "<bin_i_izraz>":
            binIIzraz(cvor, djelokrug)
        elif lijevo == "<bin_xili_izraz>":
            binXiliIzraz(cvor, djelokrug)
        elif lijevo == "<bin_ili_izraz>":
            binIliIzraz(cvor, djelokrug)
        elif lijevo == "<log_i_izraz>":
            logIIzraz(cvor, djelokrug)
        elif lijevo == "<log_ili_izraz>":
            logIliIzraz(cvor, djelokrug)
        elif lijevo == "<izraz_pridruzivanja>":
            izrazPridruzivanja(cvor, djelokrug)
        elif lijevo == "<izraz>":
            izraz(cvor, djelokrug)
        elif lijevo == "<slozena_naredba>":
            slozenaNaredba(cvor, djelokrug)
        elif lijevo == "<lista_naredbi>":
            listaNaredbi(cvor, djelokrug)
        elif lijevo == "<naredba>":
            naredba(cvor, djelokrug)
        elif lijevo == "<izraz_naredba>":
            izrazNaredba(cvor, djelokrug)
        elif lijevo == "<naredba_grananja>":
            naredbaGrananja(cvor, djelokrug)
        elif lijevo == "<naredba_petlje>":
            naredbaPetlje(cvor, djelokrug)
        elif lijevo == "<naredba_skoka>":
            naredbaSkoka(cvor, djelokrug)
        elif lijevo == "<prijevodna_jedinica>":
            prijevodnaJedinica(cvor, djelokrug)
        elif lijevo == "<vanjska_deklaracija>":
            vanjskaDeklaracija(cvor, djelokrug)
        elif lijevo == "<definicija_funkcije>":
            definicijaFunkcije(cvor, djelokrug)
        elif lijevo == "<lista_parametara>":
            listaParametara(cvor, djelokrug)
        elif lijevo == "<deklaracija_parametra>":
            deklaracijaParametra(cvor, djelokrug)
        elif lijevo == "<lista_deklaracija>":
            listaDeklaracija(cvor, djelokrug)
        elif lijevo == "<deklaracija>":
            deklaracija(cvor, djelokrug)
        elif lijevo == "<lista_init_deklaratora>":
            listaInitDeklaratora(cvor, djelokrug)
        elif lijevo == "<init_deklarator>":
            initDeklarator(cvor, djelokrug)
        elif lijevo == "<izravni_deklarator>":
            izravniDeklarator(cvor, djelokrug)
        elif lijevo == "<inicijalizator>":
            inicijalizator(cvor, djelokrug)
        elif lijevo == "<lista_izraza_pridruzivanja>":
            listaIzrazaPridruzivanja(cvor, djelokrug)
        else:
            raise SyntaxError
    except ValueError:
        raise MojSyntaxError(lijevo, desno)

    for dijete in cvor.djeca:
        if dijete.greska:
            raise MojSyntaxError(lijevo, desno)

    return lijevo


def primarniIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka.split()[0] == "IDN":
        provjeri(cvor.djeca[0], djelokrug)
        if not jeDeklariran(cvor.djeca[0].ime, djelokrug):
            cvor.djeca[0].greska = True
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
        cvor.parametri = cvor.djeca[0].parametri
        cvor.pov = cvor.djeca[0].pov
    elif cvor.djeca[0].oznaka.split()[0] == "BROJ":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = "int"
        cvor.lizraz = False
    elif cvor.djeca[0].oznaka.split()[0] == "ZNAK":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = "char"
        cvor.lizraz = False
    elif cvor.djeca[0].oznaka.split()[0] == "NIZ_ZNAKOVA":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = "niz.const.char"
        cvor.lizraz = False
    elif cvor.djeca[0].oznaka.split()[0] == "L_ZAGRADA":
        provjeri(cvor.djeca[1], djelokrug)
        cvor.tip = cvor.djeca[1].tip
        cvor.lizraz = cvor.djeca[1].lizraz
    return


def postfiksIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<primarni_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
        cvor.parametri = cvor.djeca[0].parametri
        cvor.pov = cvor.djeca[0].pov
    elif cvor.djeca[1].oznaka.split()[0] == "L_UGL_ZAGRADA":
        provjeri(cvor.djeca[0], djelokrug)
        if not jednako(cvor.djeca[0].tip, "niz.X"):
            raise ValueError
        provjeri(cvor.djeca[2], djelokrug)
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        cvor.tip = cvor.djeca[0].tip[4:]
        cvor.lizraz = not jednako(cvor.djeca[1].tip[4:], "const.T")
    elif cvor.djeca[1].oznaka.split()[0] == "OP_INC" or cvor.djeca[1].oznaka.split()[0] == "OP_DEC":
        provjeri(cvor.djeca[0], djelokrug)
        if cvor.djeca[0].lizraz != True:
            raise ValueError
        if not svodljiv(cvor.djeca[0].tip, "int"):
            raise ValueError
        cvor.tip = "int"
        cvor.lizraz = False
    elif cvor.djeca[2].oznaka.split()[0] == "D_ZAGRADA":
        provjeri(cvor.djeca[0], djelokrug)
        if not jednako(cvor.djeca[0].tip, "funkcija.['void']." + str(cvor.djeca[0].pov)):
            raise ValueError
        cvor.tip = cvor.djeca[0].pov
        cvor.lizraz = False
    elif cvor.djeca[2].oznaka == "<lista_argumenata>":
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[2], djelokrug)
        if not jednako(cvor.djeca[0].tip, "funkcija." + str(cvor.djeca[0].parametri) + "." + str(cvor.djeca[0].pov)):
            raise ValueError
        if len(cvor.djeca[2].tipovi) != len(cvor.djeca[0].parametri):
            raise ValueError
        else:
            for i in range(len(cvor.djeca[2].tipovi)):
                if not svodljiv(cvor.djeca[2].tipovi[i], cvor.djeca[0].parametri[i]):
                    raise ValueError
                    break
        cvor.tip = cvor.djeca[0].pov
        cvor.lizraz = False
    return


def listaArgumenata(cvor, djelokrug):
    if len(cvor.djeca) == 1:
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tipovi = [cvor.djeca[0].tip]
    elif len(cvor.djeca) == 3:
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[2], djelokrug)
        cvor.tipovi = cvor.djeca[0].tipovi
        cvor.tipovi.append(cvor.djeca[2].tip)
    return


def unarniIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<postfiks_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif cvor.djeca[0].oznaka.split()[0] == "OP_INC" or cvor.djeca[0].oznaka.split()[0] == "OP_DEC":
        provjeri(cvor.djeca[1], djelokrug)
        if cvor.djeca[1].lizraz != True:
            raise ValueError
        if not svodljiv(cvor.djeca[1].tip, "int"):
            raise ValueError
        cvor.tip = "int"
        cvor.lizraz = False
    elif cvor.djeca[0].oznaka == "<unarni_operator>":
        provjeri(cvor.djeca[1], djelokrug)
        if not svodljiv(cvor.djeca[1].tip, "int"):
            raise ValueError
        cvor.tip = "int"
        cvor.lizraz = False
    return


def castIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<unarni_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif cvor.djeca[0].oznaka.split()[0] == "L_ZAGRADA":
        provjeri(cvor.djeca[1], djelokrug)
        provjeri(cvor.djeca[3], djelokrug)
        if not svodljiv(cvor.djeca[3].tip, cvor.djeca[1].tip) and not intUChar(cvor.djeca[3]):
            raise ValueError
        cvor.tip = cvor.djeca[1].tip
        cvor.lizraz = False
    return


def imeTipa(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<specifikator_tipa>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
    elif cvor.djeca[0].oznaka.split()[0] == "KR_CONST":
        provjeri(cvor.djeca[1], djelokrug)
        if jednako(cvor.djeca[1].tip, "void"):
            raise ValueError
        cvor.tip = "const." + cvor.djeca[1].tip
    return


def specifikatorTipa(cvor, djelokrug):
    if cvor.djeca[0].oznaka.split()[0] == "KR_VOID":
        cvor.tip = "void"
    elif cvor.djeca[0].oznaka.split()[0] == "KR_CHAR":
        cvor.tip = "char"
    elif cvor.djeca[0].oznaka.split()[0] == "KR_INT":
        cvor.tip = "int"
    return


def multiplikativniIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<cast_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif len(cvor.djeca) == 3:
        provjeri(cvor.djeca[0], djelokrug)
        if not svodljiv(cvor.djeca[0].tip, "int"):
            raise ValueError
        if not provjeri(cvor.djeca[2], djelokrug):
            raise ValueError
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        cvor.tip = "int"
        cvor.lizraz = False
    return


def aditivniIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<multiplikativni_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif cvor.djeca[1].oznaka.split()[0] == "PLUS" or cvor.djeca[1].oznaka.split()[0] == "MINUS":
        provjeri(cvor.djeca[0], djelokrug)
        if not svodljiv(cvor.djeca[0].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[2], djelokrug)
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        cvor.tip = "int"
        cvor.lizraz = False
    return


def odnosniIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<aditivni_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif len(cvor.djeca) == 3:
        provjeri(cvor.djeca[0], djelokrug)
        if not svodljiv(cvor.djeca[0].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[2], djelokrug)
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        cvor.tip = "int"
        cvor.lizraz = False
    return


def jednakosniIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<odnosni_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif len(cvor.djeca) == 3:
        provjeri(cvor.djeca[0], djelokrug)
        if not svodljiv(cvor.djeca[0].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[2], djelokrug)
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        cvor.tip = "int"
        cvor.lizraz = False
    return


def binIIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<jednakosni_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif cvor.djeca[0].oznaka == "<bin_i_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        if not svodljiv(cvor.djeca[0].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[2], djelokrug)
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        cvor.tip = "int"
        cvor.lizraz = False
    return


def binXiliIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<bin_i_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif cvor.djeca[0].oznaka == "<bin_xili_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        if not svodljiv(cvor.djeca[0].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[2], djelokrug)
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        cvor.tip = "int"
        cvor.lizraz = False
    return


def binIliIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<bin_xili_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif cvor.djeca[0].oznaka == "<bin_ili_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        if not svodljiv(cvor.djeca[0].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[2], djelokrug)
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        cvor.tip = "int"
        cvor.lizraz = False
    return


def logIIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<bin_ili_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif cvor.djeca[0].oznaka == "<log_i_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        if not svodljiv(cvor.djeca[0].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[2], djelokrug)
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        cvor.tip = "int"
        cvor.lizraz = False
    return


def logIliIzraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<log_i_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif cvor.djeca[0].oznaka == "<log_ili_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        if not svodljiv(cvor.djeca[0].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[2], djelokrug)
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        cvor.tip = "int"
        cvor.lizraz = False
    return


def izrazPridruzivanja(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<log_ili_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif cvor.djeca[0].oznaka == "<postfiks_izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        if cvor.djeca[0].lizraz != True:
            raise ValueError
        provjeri(cvor.djeca[2], djelokrug)
        if not svodljiv(cvor.djeca[2].tip, cvor.djeca[0].tip):
            raise ValueError
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = False
    return


def izraz(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<izraz_pridruzivanja>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
        cvor.lizraz = cvor.djeca[0].lizraz
    elif cvor.djeca[0].oznaka == "<izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[2], djelokrug)
        cvor.tip = cvor.djeca[2].tip
        cvor.lizraz = False
    return


def slozenaNaredba(cvor, djelokrug):
    if cvor.djeca[1].oznaka == "<lista_naredbi>":
        provjeri(cvor.djeca[1], djelokrug)
    elif cvor.djeca[1].oznaka == "<lista_deklaracija>":
        provjeri(cvor.djeca[1], djelokrug)
        provjeri(cvor.djeca[2], djelokrug)
    return


def listaNaredbi(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<naredba>":
        provjeri(cvor.djeca[0], djelokrug)
    elif cvor.djeca[0].oznaka == "<lista_naredbi>":
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[1], djelokrug)
    return


def naredba(cvor, djelokrug):
    provjeri(cvor.djeca[0], djelokrug)
    return


def izrazNaredba(cvor, djelokrug):
    if cvor.djeca[0].oznaka.split()[0] == "TOCKAZAREZ":
        cvor.tip = "int"
    elif cvor.djeca[0].oznaka == "<izraz>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tip = cvor.djeca[0].tip
    return


def naredbaGrananja(cvor, djelokrug):
    if len(cvor.djeca) == 5:
        provjeri(cvor.djeca[2], djelokrug)
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[4], djelokrug)
    elif len(cvor.djeca) == 7:
        provjeri(cvor.djeca[2], djelokrug)
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[4], djelokrug)
        provjeri(cvor.djeca[6], djelokrug)
    return


def naredbaPetlje(cvor, djelokrug):
    if cvor.djeca[0].oznaka.split()[0] == "KR_WHILE":
        novi = noviDjelokrug(djelokrug)
        novi.petlja = True
        provjeri(cvor.djeca[2], novi)
        if not svodljiv(cvor.djeca[2].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[4], novi)
    elif cvor.djeca[4].oznaka.split()[0] == "D_ZAGRADA":
        novi = noviDjelokrug(djelokrug)
        novi.petlja = True
        provjeri(cvor.djeca[2], novi)
        provjeri(cvor.djeca[3], novi)
        if not svodljiv(cvor.djeca[3].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[5], novi)
    elif cvor.djeca[4].oznaka == "<izraz>":
        novi = noviDjelokrug(djelokrug)
        novi.petlja = True
        provjeri(cvor.djeca[2], novi)
        provjeri(cvor.djeca[3], novi)
        if not svodljiv(cvor.djeca[3].tip, "int"):
            raise ValueError
        provjeri(cvor.djeca[4], novi)
        provjeri(cvor.djeca[6], novi)
    return


def naredbaSkoka(cvor, djelokrug):
    if cvor.djeca[0].oznaka.split()[0] == "KR_CONTINUE" or cvor.djeca[0].oznaka.split()[0] == "KR_BREAK":
        if not uPetlji(djelokrug):
            raise ValueError
    elif cvor.djeca[1].oznaka.split()[0] == "TOCKAZAREZ":
        pov = povFunkcije(djelokrug)
        if pov != "void":
            raise ValueError
    elif cvor.djeca[1].oznaka == "<izraz>":
        provjeri(cvor.djeca[1], djelokrug)
        pov = povFunkcije(djelokrug)
        if pov == None or not svodljiv(cvor.djeca[1].tip, pov):
            raise ValueError
    return


def prijevodnaJedinica(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<vanjska_deklaracija>":
        provjeri(cvor.djeca[0], djelokrug)
    elif cvor.djeca[0].oznaka == "<prijevodna_jedinica>":
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[1], djelokrug)
    return


def vanjskaDeklaracija(cvor, djelokrug):
    provjeri(cvor.djeca[0], djelokrug)
    return


def definicijaFunkcije(cvor, djelokrug):
    if cvor.djeca[3].oznaka.split()[0] == "KR_VOID":
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[1], djelokrug)
        if jednako(cvor.djeca[0].tip, "const.T"):
            raise ValueError
        if postojiFunkcija(cvor.djeca[1].ime, djelokrug):
            raise ValueError
        glob_djelokrug = dohvatiGlobalni(djelokrug)
        if cvor.djeca[1].ime in glob_djelokrug.tablica_funkcija:
            funk = glob_djelokrug.tablica_funkcija[cvor.djeca[1].ime].pop()
            parametri, pov = funk[0], funk[1]
            glob_djelokrug.tablica_funkcija[cvor.djeca[1].ime].add(funk)
            if parametri != "void" or pov != cvor.djeca[0].tip:
                raise ValueError
        djelokrug.deklarirajFunkciju(cvor.djeca[1].ime, str(["void"]), cvor.djeca[0].tip)
        djelokrug.definirajFunkciju(cvor.djeca[1].ime, str(["void"]), cvor.djeca[0].tip)
        novi = noviDjelokrug(djelokrug)
        novi.petlja = djelokrug.petlja
        novi.pov = cvor.djeca[0].tip
        novi.parametri = ['void']
        provjeri(cvor.djeca[5], novi)
    elif cvor.djeca[3].oznaka == "<lista_parametara>":
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[1], djelokrug)
        if jednako(cvor.djeca[0].tip, "const.T"):
            raise ValueError
        if postojiFunkcija(cvor.djeca[1].ime, djelokrug):
            raise ValueError
        novi = noviDjelokrug(djelokrug)
        novi.petlja = djelokrug.petlja
        novi.pov = cvor.djeca[0].tip
        novi.parametri = cvor.djeca[3].tipovi
        provjeri(cvor.djeca[3], novi)
        glob_djelokrug = dohvatiGlobalni(djelokrug)
        if cvor.djeca[1].ime in glob_djelokrug.tablica_funkcija:
            funk = glob_djelokrug.tablica_funkcija[cvor.djeca[1].ime].pop()
            parametri, pov = funk[0], funk[1]
            glob_djelokrug.tablica_funkcija[cvor.djeca[1].ime].add(funk)
            if parametri != cvor.djeca[3].tipovi or pov != cvor.djeca[0].tip:
                raise ValueError
        djelokrug.deklarirajFunkciju(cvor.djeca[1].ime, str(cvor.djeca[3].tipovi), cvor.djeca[0].tip)
        djelokrug.definirajFunkciju(cvor.djeca[1].ime, str(cvor.djeca[3].tipovi), cvor.djeca[0].tip)
        provjeri(cvor.djeca[5], novi)
    return


def listaParametara(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<deklaracija_parametra>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tipovi = [cvor.djeca[0].tip]
        cvor.imena = [cvor.djeca[0].ime]
    elif cvor.djeca[0].oznaka == "<lista_parametara>":
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[2], djelokrug)
        if cvor.djeca[2].ime in cvor.djeca[0].imena:
            raise ValueError
        cvor.tipovi = cvor.djeca[0].tipovi
        cvor.tipovi.append(cvor.djeca[2].tip)
        cvor.imena = cvor.djeca[0].imena
        cvor.imena.append(cvor.djeca[2].ime)
    return


def deklaracijaParametra(cvor, djelokrug):
    if len(cvor.djeca) == 2:
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[1], djelokrug)
        if jednako(cvor.djeca[0].tip, "void"):
            raise ValueError
        djelokrug.deklarirajIdentifikator(cvor.djeca[1].ime, cvor.djeca[0].tip, None)
        cvor.tip = cvor.djeca[0].tip
        cvor.ime = cvor.djeca[1].ime
    elif len(cvor.djeca) == 4:
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[1], djelokrug)
        if jednako(cvor.djeca[0].tip, "void"):
            raise ValueError
        djelokrug.deklarirajIdentifikator(cvor.djeca[1].ime, "niz." + cvor.djeca[0].tip, None)
        cvor.tip = "niz." + cvor.djeca[0].tip
        cvor.ime = cvor.djeca[1].ime
    return


def listaDeklaracija(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<deklaracija>":
        provjeri(cvor.djeca[0], djelokrug)
    elif cvor.djeca[0].oznaka == "<lista_deklaracija>":
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[1], djelokrug)
    return


def deklaracija(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<ime_tipa>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.djeca[1].ntip = cvor.djeca[0].tip
        provjeri(cvor.djeca[1], djelokrug)
    return


def listaInitDeklaratora(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<init_deklarator>":
        cvor.djeca[0].ntip = cvor.ntip
        provjeri(cvor.djeca[0], djelokrug)
    elif cvor.djeca[0].oznaka == "<lista_init_deklaratora>":
        cvor.djeca[0].ntip = cvor.ntip
        provjeri(cvor.djeca[0], djelokrug)
        cvor.djeca[2].ntip = cvor.ntip
        provjeri(cvor.djeca[2], djelokrug)
    return


def initDeklarator(cvor, djelokrug):
    if len(cvor.djeca) == 1:
        cvor.djeca[0].ntip = cvor.ntip
        provjeri(cvor.djeca[0], djelokrug)
        if jednako(cvor.djeca[0].tip, "const.T") or jednako(cvor.djeca[0].tip, "niz.const.T"):
            raise ValueError
    elif len(cvor.djeca) == 3:
        cvor.djeca[0].ntip = cvor.ntip
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[2], djelokrug)
        if jednako(cvor.djeca[0].tip, "int") or jednako(cvor.djeca[0].tip, "const.int"):
            if not svodljiv(cvor.djeca[2].tip, "int"):
                raise ValueError
        elif jednako(cvor.djeca[0].tip, "char") or jednako(cvor.djeca[0].tip, "const.char"):
            if not svodljiv(cvor.djeca[2].tip, "char"):
                raise ValueError
        elif jednako(cvor.djeca[0].tip, "niz.T") or jednako(cvor.djeca[0].tip, "niz.const.T"):
            if cvor.djeca[2].br_elem > cvor.djeca[0].br_elem:
                raise ValueError
            for tip in cvor.djeca[2].tipovi:
                if not svodljiv(tip, "T"):
                    raise ValueError
                    break
        else:
            raise ValueError
    return


def izravniDeklarator(cvor, djelokrug):
    if len(cvor.djeca) == 1:
        provjeri(cvor.djeca[0], djelokrug)
        if jednako(cvor.ntip, "void"):
            raise ValueError
        if cvor.djeca[0].ime in djelokrug.tablica_znakova:
            raise ValueError
        djelokrug.deklarirajIdentifikator(cvor.djeca[0].ime, cvor.ntip, cvor.djeca[0].vrijednost)
        cvor.tip = cvor.ntip
    elif cvor.djeca[1].oznaka.split()[0] == "L_UGL_ZAGRADA":
        provjeri(cvor.djeca[0], djelokrug)
        if jednako(cvor.ntip, "void"):
            raise ValueError
        if cvor.djeca[0].ime in djelokrug.tablica_znakova:
            raise ValueError
        provjeri(cvor.djeca[2], djelokrug)
        if cvor.djeca[2].vrijednost <= 0 or cvor.djeca[2].vrijednost > 1024:
            raise ValueError
        djelokrug.deklarirajIdentifikator(cvor.djeca[0].ime, "niz." + cvor.ntip, cvor.djeca[0].vrijednost)
        cvor.tip = "niz." + cvor.ntip
        cvor.br_elem = cvor.djeca[2].vrijednost
    elif cvor.djeca[2].oznaka.split()[0] == "KR_VOID":
        provjeri(cvor.djeca[0], djelokrug)
        if cvor.djeca[0].ime in djelokrug.tablica_funkcija:
            funk = djelokrug.tablica_funkcija[cvor.djeca[0].ime].pop()
            parametri, tip = funk[0], funk[1]
            djelokrug.tablica_funkcija[cvor.djeca[0].ime].add(funk)
            if "funkcija.['void']." + cvor.ntip != "funkcija." + parametri + "." + tip:
                raise ValueError
        djelokrug.deklarirajFunkciju(cvor.djeca[0].ime, str(["void"]), cvor.ntip)
        cvor.tip = "funkcija.['void']." + cvor.ntip
    elif cvor.djeca[2].oznaka == "<lista_parametara>":
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[2], djelokrug)
        if cvor.djeca[0].ime in djelokrug.tablica_funkcija:
            funk = djelokrug.tablica_funkcija[cvor.djeca[0].ime].pop()
            parametri, tip = funk[0], funk[1]
            djelokrug.tablica_funkcija[cvor.djeca[0].ime].add(funk)
            if "funkcija." + str(cvor.djeca[2].tipovi) + "." + cvor.ntip != "funkcija." + parametri + "." + tip:
                raise ValueError
        djelokrug.deklarirajFunkciju(cvor.djeca[0].ime, str(cvor.djeca[2].tipovi), cvor.ntip)
    return


def inicijalizator(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<izraz_pridruzivanja>":
        provjeri(cvor.djeca[0], djelokrug)
        zavrsni_znak = zavrsniCvor(cvor.djeca[0])
        if zavrsni_znak.oznaka == "NIZ_ZNAKOVA":
            cvor.br_elem = len(zavrsni_znak) + 1
            cvor.tipovi = str(["char"] * cvor.djeca[0].br_elem)
        else:
            cvor.tip = cvor.djeca[0].tip
    elif cvor.djeca[0].oznaka == "L_VIT_ZAGRADA":
        provjeri(cvor.djeca[1], djelokrug)
        cvor.br_elem = cvor.djeca[1].br_elem
        cvor.tipovi = cvor.djeca[1].tipovi
    return


def listaIzrazaPridruzivanja(cvor, djelokrug):
    if cvor.djeca[0].oznaka == "<izraz_pridruzivanja>":
        provjeri(cvor.djeca[0], djelokrug)
        cvor.tipovi = [cvor.djeca[0].tip]
        cvor.br_elem = 1
    elif cvor.djeca[0].oznaka == "<lista_izraza_pridruzivanja>":
        provjeri(cvor.djeca[0], djelokrug)
        provjeri(cvor.djeca[1], djelokrug)
        cvor.tipovi = cvor.djeca[0].tipovi
        cvor.tipovi.append(cvor.djeca[1].tip)
        cvor.br_elem = cvor.djeca[0].br_elem + 1
    return


def idn(znakovi, cvor, djelokrug):
    cvor.ime = znakovi
    cvor.lizraz = True
    djelokrug = jeDeklariran(znakovi, djelokrug)
    if djelokrug:
        if znakovi in djelokrug.tablica_znakova:
            dekl = djelokrug.tablica_znakova[znakovi]
            cvor.tip, cvor.vrijednost = dekl[0], dekl[1]
        elif znakovi in djelokrug.tablica_funkcija:
            funk = djelokrug.tablica_funkcija[znakovi].pop()
            cvor.tip, cvor.parametri, cvor.pov = "funkcija." + funk[0] + "." + funk[1], eval(funk[0]), funk[1]
            djelokrug.tablica_funkcija[znakovi].add(funk)
    return

def broj(znakovi, cvor, djelokrug):
    broj = int(znakovi)
    if not (-2147483648 <= broj <= 2147483647):
        cvor.greska = True
    cvor.tip = "int"
    cvor.vrijednost = int(znakovi)
    return


def znak(znakovi, cvor, djelokrug):
    if znakovi[0] == "'" and znakovi[-1] == "'":
        znakovi = znakovi[1:-1]
    if len(znakovi) > 1:
        if not provjeriPrefiks(znakovi):
            cvor.greska = True
            return
        else:
            znakovi = znakovi.encode("utf-8").decode("unicode_escape")
    ascii = ord(znakovi)
    if not (0 <= ascii <= 255):
        cvor.greska = True
    cvor.tip = "char"
    cvor.vrijednost = znakovi
    return


def nizZnakova(znakovi, cvor, djelokrug):
    i = 0
    while i < len(znakovi):
        if znakovi[i] == "\\":
            znak(znakovi[i : i + 2], cvor, djelokrug)
            i += 1
        else:
            znak(znakovi[i], cvor, djelokrug)
        i += 1

    cvor.tip = "niz.const.char"
    return
