import random
import copy

is_player_move = False
n2_spisok = ()
k_rez=0#!!!
o_rez=0

def end_message(s):
    global is_player_move
    z='Игра завершена'
    if s==1:
        print(z, 'Вы победили!Нажми "Да" что бы начать заново.')
    if s==2:
        print(z, 'Вы проиграли!Нажми "Да" что бы начать заново.')
    if s==3:
        print(z, 'Ходов больше нет.Нажми "Да" что бы начать заново.')

def hod_kompjutera(move_board):  # !!!
    pole = move_board
    n2_spisok = proverka_hk(pole, 1, (), [])
    print("spisok hodov:", n2_spisok)
    if n2_spisok:  # проверяем наличие доступных ходов
        kh = len(n2_spisok)  # количество ходов
        th = random.randint(0, kh - 1)  # случайный ход
        dh = len(n2_spisok[th])  # длина хода
        for h in n2_spisok:  # !!!для отладки!!!
            h = h  # !!!для отладки!!!
        for i in range(dh - 1):
            # выполняем ход
            n2_spisok = [(hod[1], 7-hod[0]) for hod in n2_spisok]#вращяем доску
            return n2_spisok
            #return hod(pole, n2_spisok[th][i][0], n2_spisok[th][i][1], n2_spisok[th][1 + i][0], n2_spisok[th][1 + i][1])
        n2_spisok = []  # очищаем список ходов
        f_hi = True  # ход игрока доступен

    # определяем победителя
    s_k, s_i = skan(pole)
    if not (s_i):
        end_message(2)
    elif not (s_k):
        end_message(1)
    elif is_player_move and not (spisok_hi()):
        end_message(3)
    elif not (is_player_move) and not (spisok_hk(pole)):
        end_message(3)

def prosmotr_hodov_eat(pole,spisok):#проверка наличия обязательных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            spisok=prosmotr_hodov_k1p(pole,spisok,x,y)
    return spisok

def prosmotr_hodov_k1p(pole, spisok,x,y):
    if pole[y][x]==3:#пешка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2:
                    if pole[y+iy+iy][x+ix+ix]==0:
                        spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка
    if pole[y][x]==4:#пешка с короной
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0#определение правильности хода
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                    if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2:
                        osh+=1
                    if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or osh==2:
                        if osh>0:spisok.pop()#удаление хода из списка
                        break
    return spisok

def prosmotr_hodov_move(pole, spisok):#проверка наличия остальных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            if pole[y][x]==3:#пешка
                for ix,iy in (-1,1),(1,1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if pole[y+iy][x+ix]==0:
                            spisok.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                        if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if pole[y+iy*2][x+ix*2]==0:
                                    spisok.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка
            if pole[y][x]==4:#пешка с короной
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0#определение правильности хода
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if pole[y+iy*i][x+ix*i]==0:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                            if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2:
                                osh+=1
                            if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or osh==2:
                                break
    return spisok

def spisok_hk(pole):  # составляем список ходов компьютера
    spisok = prosmotr_hodov_eat(pole, [])  # здесь проверяем обязательные ходы
    if not (spisok):
        spisok = prosmotr_hodov_move(pole, [])  # здесь проверяем оставшиеся ходы
    return spisok

def proverka_hk(pole, tur, n_spisok, spisok):  # !!!
    move_set = ()
    global l_rez, k_rez, o_rez
    if not (spisok):  # если список ходов пустой...
        spisok = spisok_hk(pole)  # заполняем

    if spisok:
        k_pole = copy.deepcopy(pole)  # копируем поле
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in spisok:  # проходим все ходы по списку
            t_spisok = hod(pole, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_spisok:  # если существует ещё ход
                move_set = move_set + (proverka_hk(pole, tur, (n_spisok + ((poz1_x, poz1_y),)), t_spisok))
            else:
                proverka_hi(pole, tur, [])
                if tur == 1:
                    t_rez = o_rez / k_rez
                    if not (move_set):  # записыаем если пустой
                        move_set = (n_spisok + ((poz1_x, poz1_y), (poz2_x, poz2_y)))
                        l_rez = t_rez  # сохряняем наилучший результат
                    else:
                        if t_rez == l_rez:
                            move_set = move_set + (n_spisok + ((poz1_x, poz1_y), (poz2_x, poz2_y)))
                        if t_rez > l_rez:
                            move_set = ()
                            move_set = (n_spisok + ((poz1_x, poz1_y), (poz2_x, poz2_y)))
                            l_rez = t_rez  # сохряняем наилучший результат
                    o_rez = 0
                    k_rez = 0

            pole = copy.deepcopy(k_pole)  # возвращаем поле
            return move_set
    else:  # ???
        s_k, s_i = skan(pole)  # подсчёт результата хода
        o_rez += (s_k - s_i)
        k_rez += 1

def spisok_hi(pole):  # составляем список ходов игрока
    spisok = prosmotr_hodov_i1(pole)  # здесь проверяем обязательные ходы
    if not (spisok):
        spisok = prosmotr_hodov_i2(pole, spisok)  # здесь проверяем оставшиеся ходы
    return spisok

def prosmotr_hodov_i1(pole):#проверка наличия обязательных ходов
    spisok=[]#список ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            spisok=prosmotr_hodov_i1p(pole, spisok,x,y)
    return spisok

def prosmotr_hodov_i1p(pole, spisok,x,y):
    if pole[y][x]==1:#пешка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4:
                    if pole[y+iy+iy][x+ix+ix]==0:
                        spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка
    if pole[y][x]==2:#пешка с короной
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0#определение правильности хода
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                    if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4:
                        osh+=1
                    if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or osh==2:
                        if osh>0:spisok.pop()#удаление хода из списка
                        break
    return spisok

def prosmotr_hodov_i2(pole, spisok):#проверка наличия остальных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            if pole[y][x]==1:#пешка
                for ix,iy in (-1,-1),(1,-1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if pole[y+iy][x+ix]==0:
                            spisok.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                        if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if pole[y+iy*2][x+ix*2]==0:
                                    spisok.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка
            if pole[y][x]==2:#пешка с короной
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0#определение правильности хода
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if pole[y+iy*i][x+ix*i]==0:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                            if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4:
                                osh+=1
                            if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or osh==2:
                                break
    return spisok

def proverka_hi(pole, tur, spisok):
    global k_rez, o_rez
    if not (spisok):
        spisok = spisok_hi(pole)

    ur = 3

    if spisok:  # проверяем наличие доступных ходов
        k_pole = copy.deepcopy(pole)  # копируем поле
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in spisok:
            t_spisok = hod(pole, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_spisok:  # если существует ещё ход
                proverka_hi(pole, tur, t_spisok)
            else:
                if tur < ur:
                    proverka_hk(pole, tur + 1, (), [])
                else:
                    s_k, s_i = skan(pole)  # подсчёт результата хода
                    o_rez += (s_k - s_i)
                    k_rez += 1

            pole = copy.deepcopy(k_pole)  # возвращаем поле
    else:  # доступных ходов нет
        s_k, s_i = skan(pole)  # подсчёт результата хода
        o_rez += (s_k - s_i)
        k_rez += 1

def skan(pole):  # подсчёт пешек на поле
    s_i = 0
    s_k = 0
    for i in range(8):
        for ii in pole[i]:
            if ii == 1: s_i += 1
            if ii == 2: s_i += 3
            if ii == 3: s_k += 1
            if ii == 4: s_k += 3
    return s_k, s_i

def hod(pole, poz1_x, poz1_y, poz2_x, poz2_y):
    # превращение
    if poz2_y == 0 and pole[poz1_y][poz1_x] == 1:
        pole[poz1_y][poz1_x] = 2
    # превращение
    if poz2_y == 7 and pole[poz1_y][poz1_x] == 3:
        pole[poz1_y][poz1_x] = 4
    # делаем ход
    pole[poz2_y][poz2_x] = pole[poz1_y][poz1_x]
    pole[poz1_y][poz1_x] = 0

    # рубим пешку игрока
    kx = ky = 1
    if poz1_x < poz2_x: kx = -1
    if poz1_y < poz2_y: ky = -1
    x_poz, y_poz = poz2_x, poz2_y
    while (poz1_x != x_poz) or (poz1_y != y_poz):
        x_poz += kx
        y_poz += ky
        if pole[y_poz][x_poz] != 0:
            pole[y_poz][x_poz] = 0
            if pole[poz2_y][poz2_x] == 3 or pole[poz2_y][poz2_x] == 4:  # ...компьютера
                return prosmotr_hodov_k1p(pole, [], poz2_x, poz2_y)  # возвращаем список доступных ходов
            elif pole[poz2_y][poz2_x] == 1 or pole[poz2_y][poz2_x] == 2:  # ...игрока
                return prosmotr_hodov_i1p(pole, [], poz2_x, poz2_y)  # возвращаем список доступных ходов