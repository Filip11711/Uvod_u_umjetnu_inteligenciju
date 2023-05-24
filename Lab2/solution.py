import sys, codecs

class Literal():
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        if self.value == 0:
            return "~" + self.name
        return self.name
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return self.name == other.name and self.value == other.value

class Klauzula():
    def __init__(self, literali, roditelj_1, roditelj_2, broj):
        self.literali = []
        self.roditelj_1 = roditelj_1
        self.roditelj_2 = roditelj_2
        self.broj = broj
        for literal in literali:
            self.literali.append(Literal(literal[0], literal[1]))
    def __str__(self):
        literali = [literal.__str__() for literal in self.literali]
        return " v ".join(literali)
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        if len(self.literali) == len(other.literali):
            for literal in self.literali:
                if literal not in other.literali:
                    return False
            return True
        else:
            return False
    def __le__(self, other):
        if len(self.literali) <= len(other.literali):
            for literal in self.literali:
                if literal not in other.literali:
                    return False
            return True
        else:
            return False

class Naredba():
    def __init__(self, klauzula, akcija):
        self.klauzula = klauzula
        self.akcija = akcija
    def __str__(self):
        return self.klauzula.__str__() + " " + self.akcija
    def __repr__(self):
        return self.__str__()

class Asistent():
    def __init__(self, klauzule, naredbe):
        self.klauzule = klauzule
        self.naredbe = naredbe
        self.start()

    def start(self):
        for naredba in self.naredbe:
            if naredba.akcija == "provjeri":
                provjeri = Resolve(self.klauzule, naredba.klauzula)
            elif naredba.akcija == "dodaj":
                naredba.klauzula.broj = len(self.klauzule) + 1
                self.klauzule.append(naredba.klauzula)
                print("Added " + naredba.klauzula.__str__())
            elif naredba.akcija == "ukloni":
                for i, klauzula in enumerate(self.klauzule):
                    if klauzula == naredba.klauzula:
                        self.klauzule.pop(i)
                        break
                print("removed " + naredba.klauzula.__str__())

class Resolve():
    def __init__(self, klauzule, cilj):
        global brojac
        self.klauzule = klauzule
        self.cilj = cilj
        self.Sos = negiraj(cilj, len(self.klauzule)+1)
        brojac = len(self.klauzule) + len(self.Sos) + 1
        self.start()

    def start(self):
        NIL_klauzula = self.algoritam()
        if NIL_klauzula:
            for klauzula in self.klauzule:
                print(str(klauzula.broj) + ". " + klauzula.__str__())
            for klauzula in negiraj(self.cilj, len(self.klauzule)+1):
                print(str(klauzula.broj) + ". " + klauzula.__str__())
            print("===============")
            ispis(NIL_klauzula)
            print("===============")
            print("[CONCLUSION]: " + self.cilj.__str__() + " is true")
        else:
            print("[CONCLUSION]: " + self.cilj.__str__() + " is unknown")

    
    def algoritam(self):
        while True:
            nove_klauzule = []
            for klauzula_1, klauzula_2 in odaberi_klauzule(self.klauzule, self.Sos):
                rezolvente = self.rijesi(klauzula_1, klauzula_2)
                chech = find_NIL(rezolvente)
                if chech:
                    return chech
                nove_klauzule = dodaj(rezolvente, nove_klauzule)
            if not nove_klauzule:
                return None
            for klauzula in nove_klauzule:
                self.Sos.append(klauzula)

    def rijesi(self, klauzula_1, klauzula_2):
        rezolvente = []
        if len(klauzula_1.literali) == 1 and len(klauzula_2.literali) == 1:
            if komplement(klauzula_1.literali[0], klauzula_2.literali[0]):
                rezolvente.append(Klauzula([["NIL", 1]], klauzula_1, klauzula_2, 0))
                return rezolvente
        for i, literal_1 in enumerate(klauzula_1.literali):
            for j, literal_2 in enumerate(klauzula_2.literali):
                if komplement(literal_1, literal_2):
                    klauzula = Klauzula([], klauzula_1, klauzula_2, 0)
                    literali_1 = klauzula_1.literali[::]
                    literali_1.pop(i)
                    literali_2 = klauzula_2.literali[::]
                    literali_2.pop(j)
                    klauzula.literali += literali_1
                    klauzula.literali += literali_2
                    if nevazna(klauzula):
                        break
                    klauzula = faktoriziraj(klauzula)
                    if self.redundantna(klauzula):
                        break
                    rezolvente.append(klauzula)
                    break
        return rezolvente
                
    def redundantna(self, klauzula):
        for klauzula_1 in self.klauzule:
            if klauzula_1 <= klauzula:
                return True
        for klauzula_2 in self.Sos:
            if klauzula_2 <= klauzula:
                return True
        return False

def ispis(klauzula):
    global brojac
    if klauzula.broj == 0:
        ispis(klauzula.roditelj_1)
        ispis(klauzula.roditelj_2)
        klauzula.broj = brojac
        brojac += 1
        tuple_ = (klauzula.roditelj_1.broj, klauzula.roditelj_2.broj)
        tuple_ = tuple(sorted(tuple_))
        print(str(klauzula.broj) + ". " + klauzula.__str__() + " " + str(tuple_))
        return
    else:
        return

def find_NIL(rezolvente):
    for klauzula in rezolvente:
        if klauzula.literali[0].name == "NIL":
            return klauzula
    return None

def odaberi_klauzule(klauzule, Sos):
    odabrane_klauzule = []
    for i in range(len(Sos)):
        for j in range(i, len(Sos)):
            if i != j:
                odabrane_klauzule.append((Sos[i], Sos[j]))
        for j in range(len(klauzule)):
            odabrane_klauzule.append((Sos[i], klauzule[j]))
    return odabrane_klauzule

def komplement(literal_1, literal_2):
    if literal_1.name == literal_2.name and literal_1.value != literal_2.value:
        return True
    return False

def nevazna(klauzula):
    for i in range(len(klauzula.literali)):
        for j in range(i, len(klauzula.literali)):
            if i != j:
                if komplement(klauzula.literali[i], klauzula.literali[j]):
                    return True
    return False

def faktoriziraj(klauzula):
    for i in range(len(klauzula.literali)):
        if i < len(klauzula.literali):
            for j in range(len(klauzula.literali)-1, i, -1):
                if klauzula.literali[i] == klauzula.literali[j]:
                    klauzula.literali.pop(j)
    return klauzula

def dodaj(rezolvente, klauzule):
    for rezolventa in rezolvente:
        if rezolventa not in klauzule:
            klauzule.append(rezolventa)
    return klauzule

def negiraj(klauzula, counter):
    negirano = []
    for i, literal in enumerate(klauzula.literali):
        if literal.value == 1:
            novi_literal = Literal(literal.name, 0)
        else:
            novi_literal = Literal(literal.name, 1)
        nova_klauzula = Klauzula([], None, None, counter+i)
        nova_klauzula.literali.append(novi_literal)
        negirano.append(nova_klauzula)
    return negirano

def ucitaj_klauzule(datoteka_klauzule):
    with codecs.open("Test/" + datoteka_klauzule, "r", "utf-8") as f:
        lines = f.readlines()

    lines = [line.lower() for line in lines if line[0] != '#']
    lines = ["".join(line.splitlines()) for line in lines]
    
    klauzule = []
    for i, line in enumerate(lines):
        literali = []
        skup_literala = line.split(" v ")
        for literal in skup_literala:
            if literal[0] == '~':
                literal = literal[1:]
                literali.append([literal, 0])
            else:
                literali.append([literal, 1])
        klauzule.append(Klauzula(literali, None, None, i+1))

    return klauzule
        

def ucitaj_naredbe(datoteka_naredbi):
    with codecs.open("Test/" + datoteka_naredbi, "r", "utf-8") as f:
        lines = f.readlines()

    lines = [line.lower() for line in lines if line[0] != '#']
    lines = ["".join(line.splitlines()) for line in lines]

    naredbe = []
    for line in lines:
        if line[-1] == '?':
            akcija = "provjeri"
        elif line[-1] == '+':
            akcija = "dodaj"
        elif line[-1] == '-':
            akcija = "ukloni"
        line = line[:(len(line) - 2)]

        literali = []
        skup_literala = line.split(" v ")
        for literal in skup_literala:
            if literal[0] == '~':
                literal = literal[1:]
                literali.append([literal, 0])
            else:
                literali.append([literal, 1])
        naredbe.append(Naredba(Klauzula(literali, None, None, 0), akcija))

    return naredbe

n = len(sys.argv)

if n == 3 and sys.argv[1] == "resolution":
    klauzule = ucitaj_klauzule(sys.argv[2])
    resolve = Resolve(klauzule[:len(klauzule)-1], klauzule[-1])
if n == 4 and sys.argv[1] == "cooking":
    klauzule = ucitaj_klauzule(sys.argv[2])
    naredbe = ucitaj_naredbe(sys.argv[3])
    asistent = Asistent(klauzule, naredbe)

