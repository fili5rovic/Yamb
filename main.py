# region LKG
seed = 7


def dohvati_seed():
    return seed


def postavi_seed(newSeed):
    global seed
    seed = newSeed


def lkg(a, c, m):
    if not (m > 0 and 0 <= a < m and 0 <= c < m):
        return -1
    else:
        x = dohvati_seed()
        x = (a * x + c) % m
        postavi_seed(x)  # generise novi seed na osnovu ove vrednosti.
        slucajan_broj = x / (m - 1)
    return slucajan_broj


def lkg_binarno(a=1103515245, c=12345, m=2 ** 32):
    slucajan_broj = lkg(a, c, m)
    slucajan_broj = 1 if slucajan_broj > 0.5 else 0
    return slucajan_broj


def bacanje_kockice():
    x = 6
    while x > 5:
        x = lkg_binarno()
        x = 2 * x + lkg_binarno()
        x = 2 * x + lkg_binarno()
    return x + 1


def baci_n_kockica(n):
    niz = []
    for i in range(0, n):
        niz.append(bacanje_kockice())
    return niz


# endregion


# region Bojenje
def print_rgb_bg(text, r, g, b, r1, g1, b1, end='\n'):
    print('\033[38;2;' + str(r) + ';' + str(g) + ';' + str(b) + ';48;2;' + str(r1) + ';' + str(g1) + ';' + str(
        b1) + 'm' + text + '\033[0m', end=end)


def print_rgb(text, r, g, b, end='\n'):
    print('\033[38;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm' + text + '\033[0m', end=end)


def print_red(text, end='\n'):
    print('\33[31m\33[1m' + text + '\033[0m', end=end)


def print_blue(text, end='\n'):
    print('\33[94m' + text + '\033[0m', end=end)


def print_white_bg(text, end='\n'):
    print('\033[47m' + text + '\033[0m', end=end)


def print_green_italic(text, end='\n'):
    print('\33[32m\33[3m' + text + '\033[0m', end=end)


def print_green(text, end='\n'):
    print('\33[32m' + text + '\033[0m', end=end)


def print_with_borders(text):
    print(text + '\n―――――――――――――――――――――――――――――――――――――――――――――')


# endregion

def ispisi_kockice_lepo(niz_bacenih_kockica):
    print('{:^63}'.format('Vrednosti na kockicama:'))
    print('{:^22}'.format(' '), end='')
    for kocka in niz_bacenih_kockica:
        print('\33[7m\33[1m ' + str(kocka) + ' \033[0m', end=' ')
    print('\n')


matrica = [-1]
c = []
v = []
r = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
isCompressed = True

na_dole_indeks = 0
na_gore_indeks = 9


def vrati_vrednost_po_indeksu(niz_kockica, indeks):
    vrednost = 50
    if indeks < 6:
        x = niz_kockica.count(indeks + 1)
        vrednost = x * (indeks + 1)
    elif indeks == 6:
        vrednost = kenta(niz_kockica)
    elif indeks == 7:
        vrednost = ful(niz_kockica)
    elif indeks == 8:
        vrednost = poker(niz_kockica)
    elif indeks == 9:
        vrednost = jamb(niz_kockica)
    return vrednost


def upisi_na_dole(niz_kockica):
    global na_dole_indeks
    vrednost = vrati_vrednost_po_indeksu(niz_kockica, na_dole_indeks)
    upisi_vrednost(na_dole_indeks, 0, vrednost)
    na_dole_indeks += 1


def upisi_na_gore(niz_kockica):
    global na_gore_indeks
    vrednost = vrati_vrednost_po_indeksu(niz_kockica, na_gore_indeks)
    upisi_vrednost(na_gore_indeks, 1, vrednost)
    na_gore_indeks -= 1


def rucna(niz_kockica):
    print_green_italic('➤ Unesite indeks reda prikazane tabele po sledećem pravilu:')
    print('\n➤ Redovima (1-6) odgovaraju njihovi indeksi')
    print('➤ 7  - Kenta')
    print('➤ 8  - Ful')
    print('➤ 9  - Poker')
    print('➤ 10 - Jamb\n')
    while (True):
        print('\33[92m➢ ', end=' ')
        indeks = input().strip()
        print('\33[0m', end='')
        if 1 <= int(indeks) <= 10:
            if vrati_vrednost(int(indeks) - 1, 2) != 0:
                print_red('➤ Na ovoj poziciji ste već igrali ručnu...')
            else:
                break
        else:
            print_red('➤ Molimo Vas da unesete neku od ponuđenih opcija...')
    indeks = int(indeks)
    vrednost = vrati_vrednost_po_indeksu(niz_kockica, indeks - 1)
    upisi_vrednost(indeks - 1, 2, vrednost)
    ispisi_matricu_jamb(matrica)


def vrati_vrednost(red, kolona):
    if isCompressed:
        return csr_u_matricu()[red][kolona]
    return matrica[red][kolona]


def niz_podskup(manji, veci):
    return all(manji.count(x) <= veci.count(x) for x in manji)


def kenta(niz_kockica):
    global broj_bacanja
    if niz_podskup([1, 2, 3, 4, 5], niz_kockica) or niz_podskup([2, 3, 4, 5, 6], niz_kockica):
        if broj_bacanja == 1:
            return 66
        elif broj_bacanja == 2:
            return 56
        return 46
    return 0


def ful(niz_kockica):
    razlicite_vrednosti_niza = set([])
    for x in niz_kockica:
        razlicite_vrednosti_niza.add(x)
    if len(razlicite_vrednosti_niza) != 2:
        return 0
    else:
        x = list(razlicite_vrednosti_niza)
        if (niz_kockica.count(x[0]) == 3 and niz_kockica.count(x[1]) == 2) or (
                niz_kockica.count(x[1]) == 3 and niz_kockica.count(x[0]) == 2):
            return 30 + sum(niz_kockica)
        return 0


def poker(niz_kockica):
    razlicite_vrednosti_niza = set([])
    for x in niz_kockica:
        razlicite_vrednosti_niza.add(x)
    if len(razlicite_vrednosti_niza) != 2:
        return 0
    else:
        x = list(razlicite_vrednosti_niza)
        if niz_kockica.count(x[0]) == 4 or niz_kockica.count(x[1]) == 4:
            return 40 + sum(niz_kockica)
        return 0


def jamb(niz_kockica):
    razlicite_vrednosti_niza = set([])
    for x in niz_kockica:
        razlicite_vrednosti_niza.add(x)
    if len(razlicite_vrednosti_niza) != 1:
        return 0
    return 50 + sum(niz_kockica)


#  region CSR i matrica
def upisi_vrednost(red, kolona, vrednost):
    global isCompressed, matrica
    if len(v) > 6:
        if isCompressed:
            matrica = csr_u_matricu()
            isCompressed = False
        matrica[red][kolona] = vrednost + 0.0001
    else:
        dodaj_uz_csr(red, kolona, vrednost + 0.0001)


# NE KORISTI DIREKTNO
def dodaj_uz_csr(red, kolona, vrednost):
    c.insert(red + 1, kolona)
    v.insert(red + 1, vrednost)
    for i in range(red + 1, len(r)):
        r[i] += 1


def csr_u_matricu():
    matrica = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0],
               [0, 0, 0],
               [0, 0, 0],
               [0, 0, 0],
               [0, 0, 0],
               [0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]
    for i in range(0, len(r) - 1):
        start = r[i]
        end = r[i + 1]
        for x in range(start, end):
            matrica[i][c[x]] = v[x]
    return matrica


def matrica_puna():
    global isCompressed
    m = matrica
    if isCompressed:
        m = csr_u_matricu()
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == 0:
                return False
    return True


def ispisi_matricu_jamb(m):
    global isCompressed
    if isCompressed:
        m = csr_u_matricu()
    print('\n                   ╭──────────┰─────────────╮')
    a = ['1', '2', '3', '4', '5', '6', 'kenta', 'ful', 'poker', 'jamb']
    for i in range(0, len(m)):
        print("                   │", end='')
        print_rgb("{:^10s}".format(a[i]), 105, 105, 105, end='│ ')
        for j in range(0, len(m[0])):
            if m[i][j] == 0:
                print_rgb("{:^3}".format(m[i][j]), 240, 240, 240, end=' ')
            else:
                print_rgb("{:^3}".format(int(m[i][j])), 255, 128, 0, end=' ')
        if (i != len(m) - 1):
            print('│\n                   ┠──────────╂─────────────┨')
        else:
            print('│\n                   ╰──────────┻─────────────╯')
    print()


# endregion

def trenutni_bodovi():
    x = matrica
    if isCompressed:
        x = csr_u_matricu()
    suma_na_dole = 0
    suma_na_gore = 0
    suma_rucna = 0
    for i in range(0, len(x)):
        suma_na_dole += int(x[i][0])
        suma_na_gore += int(x[i][1])
        suma_rucna += int(x[i][2])
    suma = suma_na_dole + suma_na_gore + suma_rucna
    print_green('{:^65}'.format('╭───────────┰────────────╮'))
    print_green('{:^65}'.format('│  NA DOLE  │' + '{:^12}'.format(suma_na_dole) + '│'))
    print_green('{:^65}'.format('┠───────────╂────────────┨'))
    print_green('{:^65}'.format('│  NA GORE  │' + '{:^12}'.format(suma_na_gore) + '│'))
    print_green('{:^65}'.format('┠───────────╂────────────┨'))
    print_green('{:^65}'.format('│   RUČNA   │' + '{:^12}'.format(suma_rucna) + '│'))
    print_green('{:^65}'.format('┠───────────╂────────────┨'))
    print_green('{:^65}'.format('│  UKUPNO   │' + '{:^12}'.format(suma) + '│'))
    print_green('{:^65}'.format('╰───────────┻────────────╯'))


def resetuj_talon():
    global matrica, c, v, r, isCompressed, na_dole_indeks, na_gore_indeks, broj_bacanja
    matrica = [-1]
    c = []
    v = []
    r = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    na_dole_indeks = 0
    na_gore_indeks = 9
    broj_bacanja = 0
    isCompressed = True

broj_bacanja = 0
def menu_glavni():
    global na_dole_indeks, na_gore_indeks, broj_bacanja
    x = -1
    bacene_kockice_niz = []
    dodaj_uz_csr(-1, 0, 0)
    broj_bacanja = 0
    print_green_italic(
        '\n➤ Dobrodošli u igru Jamb!\n➤ Ispred Vas se nalazi interaktivni meni sa opcijama za igru.\n➤ Srećno!\n')
    validan_unos = True
    while x != '0':
        if matrica_puna():
            break
        if validan_unos == True:
            print_white_bg("╭───────────────────────────────────────────────────────────────╮")
            print_white_bg("│                     ▷ \33[3mInteraktivni meni ◁                     │")
            print_white_bg("├───────────────────────────────────────────────────────────────┤")
            print_white_bg('│  1 → Stvaranje praznog talona                                 │')
            print_white_bg('│  2 → Ispis talona i bodova                                    │')
            if x != '3':
                print_white_bg('│  3 → Baci kockice                                             │')
            if len(bacene_kockice_niz) == 0:
                print_white_bg('│  4 → Pomoć prijatelja                                         │')
            if x == '3' and broj_bacanja < 3:
                print_white_bg(
                    '│  5 → Ponovo baci kockice. ({}/2)                               │'.format(3 - broj_bacanja))
            if len(bacene_kockice_niz) > 0:
                if na_dole_indeks < 10:
                    print_white_bg('│  6 → Igraj na dole                                            │')
                if na_gore_indeks >= 0:
                    print_white_bg('│  7 → Igraj na gore                                            │')
                if broj_bacanja == 1:
                    print_white_bg('│  8 → Igraj ručnu                                              │')
            print_white_bg('│  0 → Prekini igru                                             │')
            print_white_bg('╰───────────────────────────────────────────────────────────────╯')
        else:
            print_red('➤ Molimo Vas da unesete neku od ponuđenih opcija...')
        print('\n\33[92m➢ ', end=' ')
        x = input()
        print('\33[0m')
        if x == '1':
            x = -1
            bacene_kockice_niz = []
            broj_bacanja = 0
            resetuj_talon()
            ispisi_matricu_jamb(matrica)
            validan_unos = True
        elif x == '2':
            broj_bacanja = 1
            ispisi_matricu_jamb(matrica)
            trenutni_bodovi()
            validan_unos = True
        elif x == '3' and len(bacene_kockice_niz) == 0:
            bacene_kockice_niz = baci_n_kockica(5)
            ispisi_kockice_lepo(bacene_kockice_niz)
            broj_bacanja = 1
            validan_unos = True
        elif x == '4' and len(bacene_kockice_niz) == 0:
            print_green_italic('\n                      Pomoć prijatelja...\n')
            bacene_kockice_niz = baci_n_kockica(5)
            ispisi_kockice_lepo(bacene_kockice_niz)
            broj_bacanja = 1
            upisana_vrednost = False
            for i in range(0, 10):
                if vrati_vrednost(i, 2) == 0:
                    vr = vrati_vrednost_po_indeksu(bacene_kockice_niz, i)
                    if vr > 0:
                        upisi_vrednost(i, 2, vr)
                        upisana_vrednost = True
                        break
            # ako nema kombinacija za rucnu, idi ovde
            if (upisana_vrednost == False):
                if na_dole_indeks > 9:
                    if na_gore_indeks >= 0:
                        upisi_na_gore(bacene_kockice_niz)
                    else:
                        for i in range(0, 10):
                            if vrati_vrednost(i, 2) == 0:
                                vr = vrati_vrednost_po_indeksu(bacene_kockice_niz, i)
                                upisi_vrednost(i, 2, vr)
                                break
                elif na_gore_indeks < 0:
                    if na_dole_indeks < 10:
                        upisi_na_dole(bacene_kockice_niz)
                    else:
                        for i in range(0, 10):
                            if vrati_vrednost(i, 2) == 0:
                                vr = vrati_vrednost_po_indeksu(bacene_kockice_niz, i)
                                upisi_vrednost(i, 2, vr)
                                break
                else:
                    suma_na_dole = vrati_vrednost_po_indeksu(bacene_kockice_niz, 0)
                    suma_na_gore = vrati_vrednost_po_indeksu(bacene_kockice_niz, 1)
                    if suma_na_dole >= suma_na_gore:
                        upisi_na_dole(bacene_kockice_niz)
                    elif na_gore_indeks >= 0:
                        upisi_na_gore(bacene_kockice_niz)
            ispisi_matricu_jamb(matrica)
            bacene_kockice_niz = []
            validan_unos = True
        elif x == '5' and 0 < broj_bacanja < 3:
            print_green('➤', end='')
            print_green_italic(' Unesite vrednosti kockica koje želite da zadržite, odvojene razmakom: ')
            dobro_unete = 0
            y = 0
            while (dobro_unete == 0):
                print_green('\n➢ ', end=' ')
                y = [int(a) for a in input().split()]
                if niz_podskup(y, bacene_kockice_niz):
                    dobro_unete = 1
                if dobro_unete == 0:
                    print_red('\n➤ Molimo Vas da unesete tačne vrednosti')
            novo_bacanje = baci_n_kockica(5 - len(y))
            broj_bacanja += 1
            y.extend(novo_bacanje)
            bacene_kockice_niz = y
            ispisi_kockice_lepo(bacene_kockice_niz)
            x = '3'
            validan_unos = True
        elif x == '6' and na_dole_indeks < 10 and len(bacene_kockice_niz) > 0:
            upisi_na_dole(bacene_kockice_niz)
            ispisi_matricu_jamb(matrica)
            bacene_kockice_niz = []
            validan_unos = True
        elif x == '7' and na_gore_indeks >= 0 and len(bacene_kockice_niz) > 0:
            upisi_na_gore(bacene_kockice_niz)
            ispisi_matricu_jamb(matrica)
            bacene_kockice_niz = []
            validan_unos = True
        elif x == '8' and broj_bacanja == 1:
            ispisi_matricu_jamb(matrica)
            rucna(bacene_kockice_niz)
            bacene_kockice_niz = []
            validan_unos = True
        else:
            validan_unos = False
    else:
        print_red('➤ Igra je prekinuta. ')
        return
    print_green('➤ Igra je gotova. Čestitamo!')
    ispisi_matricu_jamb(matrica)
    trenutni_bodovi()


menu_glavni()
