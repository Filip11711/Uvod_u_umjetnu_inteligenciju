import sys, codecs
from queue import PriorityQueue

class Cvor():
    def __init__(self, ime, cijena, broj, roditelj):
        self.ime = ime
        self.cijena = cijena
        self.broj = broj
        self.roditelj = roditelj
    def __lt__(self, other):
        selfPriority = (self.cijena, self.ime)
        otherPriority = (other.cijena, other.ime)
        return selfPriority < otherPriority

class BFS():
    def __init__(self, poc_ime_stanja, zav_imena_stanja, prijelazi):
        self.poc_stanje = Cvor(poc_ime_stanja, 0, 1, -1)
        self.open = [self.poc_stanje]
        self.closed = set()
        self.zav_imena_stanja = zav_imena_stanja
        self.prijelazi = prijelazi
        self.string = ""
        self.start()
    
    def start(self):
        while len(self.open) > 0:
            stanje = self.open.pop(0)
            if stanje.ime in self.zav_imena_stanja:
                self.success(stanje)
                return
            self.closed.add(stanje.ime)
            before_sorted = []
            for prijelaz in self.prijelazi[stanje.ime]:
                if self.check(prijelaz[0]):
                    before_sorted.append(Cvor(prijelaz[0], stanje.cijena + float(prijelaz[1]), stanje.broj + 1, stanje))
            after_sorted = sorted(before_sorted, key=lambda x: x.ime)
            for next_state in after_sorted:
                self.open.append(next_state)
        self.fail()

    def check(self, ime):
        if ime in self.closed:
            return False
        return True

    def rekurzivna(self, stanje):
        if stanje.roditelj == -1:
            self.string += stanje.ime
            return
        else:
            self.rekurzivna(stanje.roditelj)
            self.string += " => " + stanje.ime
            return
    
    def fail(self):
        print("[FOUND_SOLUTION]: no")

    def success(self, stanje):
        self.rekurzivna(stanje)
        print("[FOUND_SOLUTION]: yes")
        print("[STATES_VISITED]: " + str(len(self.closed)))
        print("[PATH_LENGTH]: " + str(stanje.broj))
        print("[TOTAL_COST]: " + str(round(stanje.cijena, 1)))
        print("[PATH]: " + self.string)


class UCS():
    def __init__(self, poc_ime_stanja, zav_imena_stanja, prijelazi):
        self.poc_stanje = Cvor(poc_ime_stanja, 0, 1, -1)
        self.open = PriorityQueue()
        self.open.put(self.poc_stanje)
        self.closed = set()
        self.zav_imena_stanja = zav_imena_stanja
        self.prijelazi = prijelazi
        self.string = ""
        self.start()

    def start(self):
        while not self.open.empty():
            stanje = self.open.get()
            if stanje.ime in self.zav_imena_stanja:
                self.success(stanje)
                return
            self.closed.add(stanje.ime)
            for prijelaz in self.prijelazi[stanje.ime]:
                if self.check(prijelaz[0]):
                    self.open.put(Cvor(prijelaz[0], stanje.cijena + float(prijelaz[1]), stanje.broj + 1, stanje))
        self.fail()

    def check(self, ime):
        if ime in self.closed:
            return False
        return True
    
    def rekurzivna(self, stanje):
        if stanje.roditelj == -1:
            self.string += stanje.ime
            return
        else:
            self.rekurzivna(stanje.roditelj)
            self.string += " => " + stanje.ime
            return
    
    def fail(self):
        print("[FOUND_SOLUTION]: no")

    def success(self, stanje):
        self.rekurzivna(stanje)
        print("[FOUND_SOLUTION]: yes")
        print("[STATES_VISITED]: " + str(len(self.closed)))
        print("[PATH_LENGTH]: " + str(stanje.broj))
        print("[TOTAL_COST]: " + str(round(stanje.cijena, 1)))
        print("[PATH]: " + self.string)

class AStar():
    def __init__(self, poc_ime_stanja, zav_imena_stanja, prijelazi, heuristika):
        self.poc_stanje = Cvor(poc_ime_stanja, 0, 1, -1)
        self.open = [self.poc_stanje]
        self.closed = []
        self.zav_imena_stanja = zav_imena_stanja
        self.prijelazi = prijelazi
        self.heuristika = heuristika
        self.string = ""
        self.start()

    def start(self):
        while len(self.open) > 0:
            stanje = self.open.pop(0)
            if stanje.ime in self.zav_imena_stanja:
                self.success(stanje)
                return
            self.closed.append(stanje)
            for prijelaz in self.prijelazi[stanje.ime]:
                if self.check(prijelaz, stanje.cijena):
                    self.open.append(Cvor(prijelaz[0], stanje.cijena + float(prijelaz[1]), stanje.broj + 1, stanje))
            self.open = sorted(self.open, key=lambda x: (x.cijena + float(self.heuristika[x.ime]), x.ime))
        self.fail()

    def check(self, prijelaz, trenutna_cijena):
        for i, stanje in enumerate(self.closed):
            if stanje.ime == prijelaz[0]:
                if stanje.cijena <= float(prijelaz[1]) + trenutna_cijena:
                    return False
                else:
                    self.closed.pop(i)
                    return True
        for i, stanje in enumerate(self.open):
            if stanje.ime == prijelaz[0]:
                if stanje.cijena <= float(prijelaz[1]) + trenutna_cijena:
                    return False
                else:
                    self.open.pop(i)
                    return True
        return True
    
    def rekurzivna(self, stanje):
        if stanje.roditelj == -1:
            self.string += stanje.ime
            return
        else:
            self.rekurzivna(stanje.roditelj)
            self.string += " => " + stanje.ime
            return
    
    def fail(self):
        print("[FOUND_SOLUTION]: no")

    def success(self, stanje):
        self.rekurzivna(stanje)
        print("[FOUND_SOLUTION]: yes")
        print("[STATES_VISITED]: " + str(len(self.closed)))
        print("[PATH_LENGTH]: " + str(stanje.broj))
        print("[TOTAL_COST]: " + str(round(stanje.cijena, 1)))
        print("[PATH]: " + self.string)


class HStar():
    def __init__(self, poc_ime_stanja, zav_imena_stanja, prijelazi):
        self.poc_stanje = Cvor(poc_ime_stanja, 0, 1, -1)
        self.open = PriorityQueue()
        self.open.put(self.poc_stanje)
        self.closed = set()
        self.zav_imena_stanja = zav_imena_stanja
        self.prijelazi = prijelazi

    def start(self):
        while not self.open.empty():
            stanje = self.open.get()
            if stanje.ime in self.zav_imena_stanja:
                return stanje.cijena
            self.closed.add(stanje.ime)
            for prijelaz in self.prijelazi[stanje.ime]:
                if self.check(prijelaz[0]):
                    self.open.put(Cvor(prijelaz[0], stanje.cijena + float(prijelaz[1]), stanje.broj + 1, stanje))
        return -1

    def check(self, ime):
        if ime in self.closed:
            return False
        return True



class Optimistic():
    def __init__(self, prijelazi, heuristika, zav_imena_stanja):
        self.prijelazi = prijelazi
        self.heuristika = heuristika
        self.zav_imena_stanja = zav_imena_stanja
        self.uspjesnost = True
        self.start()

    def start(self):
        for stanje in sorted(self.heuristika):
            HStar_object = HStar(stanje, self.zav_imena_stanja, self.prijelazi)
            hstar = HStar_object.start()
            if self.heuristika[stanje] <= hstar:
                print("[CONDITION]: [OK] h(" + stanje +") <= h*: " + str(round(float(self.heuristika[stanje]), 1)) +" <= " + str(round(float(hstar), 1)))
            else:
                print("[CONDITION]: [ERR] h(" + stanje +") <= h*: " + str(round(float(self.heuristika[stanje]), 1)) +" <= " + str(round(float(hstar), 1)))
                self.uspjesnost = False
        if self.uspjesnost:
            print("[CONCLUSION]: Heuristic is optimistic.")
        else:
            print("[CONCLUSION]: Heuristic is not optimistic.")


class Consistent():
    def __init__(self, prijelazi, heuristika):
        self.prijelazi = prijelazi
        self.heuristika = heuristika
        self.uspjesnost = True
        self.start()

    def start(self):
        for stanje_sad in sorted(self.prijelazi):
            for stanje_next in self.prijelazi[stanje_sad]:
                if int(self.heuristika[stanje_sad]) <= int(self.heuristika[stanje_next[0]]) + int(stanje_next[1]):
                    print("[CONDITION]: [OK] h(" + stanje_sad + ") <= h(" + stanje_next[0] + ") + c: " +
                          str(round(float(self.heuristika[stanje_sad]), 1)) + " <= " + str(round(float(self.heuristika[stanje_next[0]]), 1)) + " + " + str(round(float(stanje_next[1]), 1)))
                else:
                    print("[CONDITION]: [ERR] h(" + stanje_sad + ") <= h(" + stanje_next[0] + ") + c: " +
                          str(round(float(self.heuristika[stanje_sad]), 1)) + " <= " + str(round(float(self.heuristika[stanje_next[0]]), 1)) + " + " + str(round(float(stanje_next[1]), 1)))
                    self.uspjesnost = False
        if self.uspjesnost:
            print("[CONCLUSION]: Heuristic is consistent.")
        else:
            print("[CONCLUSION]: Heuristic is not consistent.")

def p_stanja(prostor_stanja):
    global poc_ime_stanja, zav_imena_stanja, prijelazi
    prijelazi = {}
    with codecs.open("Test/" + prostor_stanja, "r", "utf-8") as f:
        lines = f.readlines()
    lines = [line for line in lines if line[0] != "#"]
    lines = ["".join(line.splitlines()) for line in lines]
    poc_ime_stanja = lines[0]
    lines.pop(0)
    zav_imena_stanja = lines[0].split()
    lines.pop(0)
    for line in lines:
        line = line.split(":")
        stanje = line[0]
        if len(line) > 1:
            line = line[1].split()
        else:
            line = []
        for i, l in enumerate(line):
            line[i] = l.split(",")
        prijelazi[stanje] = line

def h(heuristika):
    heuristic = {}
    with codecs.open("Test/" + heuristika, "r", "utf-8") as f:
        lines = f.readlines()
    lines = [line for line in lines if line[0] != "#"]
    for line in lines:
        line = "".join(line.splitlines())
        line = line.split(": ")
        heuristic[line[0]] = int(line[1])
    return heuristic


n = len(sys.argv)

if n == 5:
    if sys.argv[1] == "--alg":
        algoritam = sys.argv[2]
    elif sys.argv[1] == "--ss":
        prostor_stanja = sys.argv[2]
    if sys.argv[3] == "--alg":
        algoritam = sys.argv[4]
    elif sys.argv[3] == "--ss":
        prostor_stanja = sys.argv[4]
    heuristika = -1
if n == 7:
    if sys.argv[1] == "--alg":
        algoritam = sys.argv[2]
    elif sys.argv[1] == "--ss":
        prostor_stanja = sys.argv[2]
    elif sys.argv[1] == "--h":
        heuristika = sys.argv[2]
    if sys.argv[3] == "--alg":
        algoritam = sys.argv[4]
    elif sys.argv[3] == "--ss":
        prostor_stanja = sys.argv[4]
    elif sys.argv[3] == "--h":
        heuristika = sys.argv[4]
    if sys.argv[5] == "--alg":
        algoritam = sys.argv[6]
    elif sys.argv[5] == "--ss":
        prostor_stanja = sys.argv[6]
    elif sys.argv[5] == "--h":
        heuristika = sys.argv[6]
if n == 6:
    if sys.argv[1] == "--check-optimistic":
        algoritam = "optimistic"
        if sys.argv[2] == "--ss":
            prostor_stanja = sys.argv[3]
        elif sys.argv[2] == "--h":
            heuristika = sys.argv[3]
        if sys.argv[4] == "--ss":
            prostor_stanja = sys.argv[5]
        elif sys.argv[4] == "--h":
            heuristika = sys.argv[5]
    elif sys.argv[1] == "--check-consistent":
        algoritam = "consistent"
        if sys.argv[2] == "--ss":
            prostor_stanja = sys.argv[3]
        elif sys.argv[2] == "--h":
            heuristika = sys.argv[3]
        if sys.argv[4] == "--ss":
            prostor_stanja = sys.argv[5]
        elif sys.argv[4] == "--h":
            heuristika = sys.argv[5]
    elif sys.argv[1] == "--ss":
        prostor_stanja = sys.argv[2]
        if sys.argv[3] == "--check-optimistic":
            algoritam = "optimistic"
            if sys.argv[4] == "--ss":
                prostor_stanja = sys.argv[5]
            elif sys.argv[4] == "--h":
                heuristika = sys.argv[5]
        elif sys.argv[3] == "--check-consistent":
            algoritam = "consistent"
            if sys.argv[4] == "--ss":
                prostor_stanja = sys.argv[5]
            elif sys.argv[4] == "--h":
                heuristika = sys.argv[5]
        elif sys.argv[3] == "--ss":
            prostor_stanja = sys.argv[4]
            if sys.argv[5] == "--check-optimistic":
                algoritam = "optimistic"
            elif sys.argv[5] == "--check-consistent":
                algoritam = "consistent"
        elif sys.argv[3] == "--h":
            heuristika = sys.argv[4]
            if sys.argv[5] == "--check-optimistic":
                algoritam = "optimistic"
            elif sys.argv[5] == "--check-consistent":
                algoritam = "consistent"
    elif sys.argv[1] == "--h":
        heuristika = sys.argv[2]
        if sys.argv[3] == "--check-optimistic":
            algoritam = "optimistic"
            if sys.argv[4] == "--ss":
                prostor_stanja = sys.argv[5]
            elif sys.argv[4] == "--h":
                heuristika = sys.argv[5]
        elif sys.argv[3] == "--check-consistent":
            algoritam = "consistent"
            if sys.argv[4] == "--ss":
                prostor_stanja = sys.argv[5]
            elif sys.argv[4] == "--h":
                heuristika = sys.argv[5]
        elif sys.argv[3] == "--ss":
            prostor_stanja = sys.argv[4]
            if sys.argv[5] == "--check-optimistic":
                algoritam = "optimistic"
            elif sys.argv[5] == "--check-consistent":
                algoritam = "consistent"
        elif sys.argv[3] == "--h":
            heuristika = sys.argv[4]
            if sys.argv[5] == "--check-optimistic":
                algoritam = "optimistic"
            elif sys.argv[5] == "--check-consistent":
                algoritam = "consistent"

p_stanja(prostor_stanja)
if heuristika != -1:
    heuristic = h(heuristika)

if algoritam == "bfs":
    print("# BFS")
    create = BFS(poc_ime_stanja, zav_imena_stanja, prijelazi)
if algoritam == "ucs":
    print("# UCS")
    create = UCS(poc_ime_stanja, zav_imena_stanja, prijelazi)
if algoritam == "astar":
    print("# A-STAR " + heuristika)
    create = AStar(poc_ime_stanja, zav_imena_stanja, prijelazi, heuristic)
if algoritam == "optimistic":
    print("# HEURISTIC-OPTIMISTIC " + heuristika)
    create = Optimistic(prijelazi, heuristic, zav_imena_stanja)
if algoritam == "consistent":
    print("# HEURISTIC-CONSISTENT " + heuristika)
    create = Consistent(prijelazi, heuristic)
