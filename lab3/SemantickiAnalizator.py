import sys
from provjeri import provjeri
from pomocne import parsirajStablo
from Djelokrug import Djelokrug


def analiziraj():
    ulaz = sys.stdin.readlines()

    stablo = parsirajStablo(ulaz)
    glob_djelokrug = Djelokrug()

    try:
        provjeri(stablo, glob_djelokrug)

        main = False
        for ime in glob_djelokrug.tablica_funkcija:
            funk = glob_djelokrug.tablica_funkcija[ime].pop()
            parametri, tip = funk[0], funk[1]
            glob_djelokrug.tablica_funkcija[ime].add(funk)
            if ime == "main" and parametri == str(["void"]) and tip == "int":
                main = True
                break

        if not main:
            print("main")

    except SyntaxError as e:
        print(f"{e}")




if __name__ == "__main__":
    analiziraj()
