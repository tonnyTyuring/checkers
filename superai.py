#Python 3.2.3 / IDLE 3.3.0
#Игра "Шашки". Автор: Волгин Ярослав
#08.08.2012-22.04.2013
import tkinter.messagebox
from tkinter import *
import random
import time
import copy

# gl_okno=Tk()#создаём окно
# gl_okno.title('Шашки')#заголовок окна
# doska=Canvas(gl_okno, width=800,height=800,bg='#FFFFFF')
# doska.pack()

n2_spisok=()#конечный список ходов компьютера
ur=2#количество предсказываемых компьютером ходов
k_rez=0#!!!
o_rez=0
figure_x=-1#клетка не задана
is_player_move=True#определение хода игрока(да)




def end_message(s):
    global is_player_move
    z='Игра завершена'
    if s==1:
        print(z, 'Вы победили!Нажми "Да" что бы начать заново.')
    if s==2:
        print(z, 'Вы проиграли!Нажми "Да" что бы начать заново.')
    if s==3:
        print(z, 'Ходов больше нет.Нажми "Да" что бы начать заново.')


# def mouse_click(event):#выбор клетки для хода 2
#     global figure_x, figure_y, figure_next_x, figre_next_y
#     global f_hi
#     x,y=(event.x)//100,(event.y)//100#вычисляем координаты клетки
#     if pole[y][x]==1 or pole[y][x]==2:#проверяем пешку игрока в выбранной клетке
#         doska.coords(red_frame, x * 100, y * 100, x * 100 + 100, y * 100 + 100)#рамка в выбранной клетке
#         figure_x, figure_y= x, y
#     else:
#         if figure_x!=-1:#клетка выбрана
#             figure_next_x, figre_next_y= x, y
#             if f_hi:#ход игрока?
#                 hod_igroka()
#                 if not(f_hi):
#                     time.sleep(0.5)
#                     hod_kompjutera()#передаём ход компьютеру
#                     #gl_okno.after(500,hod_kompjutera(0))#!!!#передаём ход компьютеру
#             figure_x=-1#клетка не выбрана
#             doska.coords(red_frame, -5, -5, -5, -5)#рамка вне поля



def make_move(board):
    return hod_kompjutera(board)



def hod_kompjutera(board):#!!!
    global is_player_move
    global n2_spisok
    proverka_hk(board,1,(),[])
    if n2_spisok:#проверяем наличие доступных ходов
        kh=len(n2_spisok)#количество ходов
        th=random.randint(0,kh-1)#случайный ход
        dh=len(n2_spisok[th])#длина хода
        for h in n2_spisok:#!!!для отладки!!!
            h=h#!!!для отладки!!!
        for i in range(dh-1):
            #выполняем ход
            return hod(board,n2_spisok[th][i][0],n2_spisok[th][i][1],n2_spisok[th][1+i][0],n2_spisok[th][1+i][1])
        n2_spisok=[]#очищаем список ходов
        f_hi=True#ход игрока доступен

    #определяем победителя
    s_k,s_i=skan(board)
    if not(s_i):
            end_message(2)
    elif not(s_k):
            end_message(1)
    elif f_hi and not(spisok_hi(board)):
            end_message(3)
    elif not(f_hi) and not(spisok_hk(board)):
            end_message(3)

def spisok_hk(board):#составляем список ходов компьютера
    spisok=prosmotr_hodov_eat(board,[])#здесь проверяем обязательные ходы
    if not(spisok):
        spisok=prosmotr_hodov_move(board,[])#здесь проверяем оставшиеся ходы
    return spisok

def proverka_hk(board,tur,n_spisok,spisok):#!!!
    global n2_spisok
    global l_rez,k_rez,o_rez
    if not(spisok):#если список ходов пустой...
        spisok=spisok_hk(board)#заполняем

    if spisok:
        k_pole=copy.deepcopy(board)#копируем поле
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:#проходим все ходы по списку
            t_spisok=hod(board,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_spisok:#если существует ещё ход
                proverka_hk(board, tur,(n_spisok+((poz1_x,poz1_y),)),t_spisok)
            else:
                proverka_hi(board,tur,[])
                if tur==1:
                    t_rez=o_rez/k_rez
                    if not(n2_spisok):#записыаем если пустой
                        n2_spisok=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                        l_rez=t_rez#сохряняем наилучший результат
                    else:
                        if t_rez==l_rez:
                            n2_spisok=n2_spisok+(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                        if t_rez>l_rez:
                            n2_spisok=()
                            n2_spisok=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                            l_rez=t_rez#сохряняем наилучший результат
                    o_rez=0
                    k_rez=0

            pole=copy.deepcopy(k_pole)#возвращаем поле
    else:#???
        s_k,s_i=skan(board)#подсчёт результата хода
        o_rez+=(s_k-s_i)
        k_rez+=1

def spisok_hi(board):#составляем список ходов игрока
    spisok=prosmotr_hodov_i1(board,[])#здесь проверяем обязательные ходы
    if not(spisok):
        spisok=prosmotr_hodov_i2(board,[])#здесь проверяем оставшиеся ходы
    return spisok
    
def proverka_hi(board, tur,spisok):
    global k_rez,o_rez
    global ur
    if not(spisok):
        spisok=spisok_hi(board)

    if spisok:#проверяем наличие доступных ходов
        k_pole=copy.deepcopy(board)#копируем поле
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:                    
            t_spisok=hod(board,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_spisok:#если существует ещё ход
                proverka_hi(board,tur,t_spisok)
            else:
                if tur<ur:
                    proverka_hk(board,tur+1,(),[])
                else:
                    s_k,s_i=skan(board)#подсчёт результата хода
                    o_rez+=(s_k-s_i)
                    k_rez+=1

            board=copy.deepcopy(k_pole)#возвращаем поле
    else:#доступных ходов нет
        s_k,s_i=skan(board)#подсчёт результата хода
        o_rez+=(s_k-s_i)
        k_rez+=1

def skan(board):#подсчёт пешек на поле
    s_i=0
    s_k=0
    for i in range(8):
        for ii in board[i]:
            if ii==1:s_i+=1
            if ii==2:s_i+=3
            if ii==3:s_k+=1
            if ii==4:s_k+=3
    return s_k,s_i

def hod_igroka(board):
    global figure_x,figure_y,figure_next_x,figre_next_y
    global is_player_move
    f_hi=False#считаем ход игрока выполненным
    spisok=spisok_hi(board)
    if spisok:
        if ((figure_x, figure_y), (figure_next_x, figre_next_y)) in spisok:#проверяем ход на соответствие правилам игры
            t_spisok=hod(1, figure_x, figure_y, figure_next_x, figre_next_y)#если всё хорошо, делаем ход
            if t_spisok:#если есть ещё ход той же пешкой
                f_hi=True#считаем ход игрока невыполненным
        else:
            f_hi=True#считаем ход игрока невыполненным
    # doska.update()#!!!обновление

def hod(board,poz1_x,poz1_y,poz2_x,poz2_y):
    # global pole
    # if f:render_board(poz1_x, poz1_y, poz2_x, poz2_y)#рисуем игровое поле
    #превращение
    if poz2_y==0 and board[poz1_y][poz1_x]==1:
        board[poz1_y][poz1_x]=2
    #превращение
    if poz2_y==7 and board[poz1_y][poz1_x]==3:
        board[poz1_y][poz1_x]=4
    #делаем ход
    # return poz1_x, poz1_y, poz2_x, poz2_y
    board[poz2_y][poz2_x]=board[poz1_y][poz1_x]
    board[poz1_y][poz1_x]=0

    # рубим пешку игрока
    kx=ky=1
    if poz1_x<poz2_x:kx=-1
    if poz1_y<poz2_y:ky=-1
    x_poz,y_poz=poz2_x,poz2_y
    while (poz1_x!=x_poz) or (poz1_y!=y_poz):
        x_poz+=kx
        y_poz+=ky
        if board[y_poz][x_poz]!=0:
            board[y_poz][x_poz]=0
            # if f:render_board(-1, -1, -1, -1)#рисуем игровое поле
            #проверяем ход той же пешкой...
            if board[poz2_y][poz2_x]==3 or board[poz2_y][poz2_x]==4:#...компьютера
                return prosmotr_hodov_k1p(board, [],poz2_x,poz2_y)#возвращаем список доступных ходов
            elif board[poz2_y][poz2_x]==1 or board[poz2_y][poz2_x]==2:#...игрока
                return prosmotr_hodov_i1p(board, [],poz2_x,poz2_y)#возвращаем список доступных ходов
    # return poz1_x, poz1_y, poz2_x, poz2_y
    # if f:render_board(poz1_x, poz1_y, poz2_x, poz2_y)#рисуем игровое поле

def prosmotr_hodov_eat(board,spisok):#проверка наличия обязательных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            spisok=prosmotr_hodov_k1p(board,spisok,x,y)
    return spisok

def prosmotr_hodov_k1p(board, spisok,x,y):
    if board[y][x]==3:#пешка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if board[y+iy][x+ix]==1 or board[y+iy][x+ix]==2:
                    if board[y+iy+iy][x+ix+ix]==0:
                        spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка
    if board[y][x]==4:#пешка с короной
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0#определение правильности хода
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                    if board[y+iy*i][x+ix*i]==1 or board[y+iy*i][x+ix*i]==2:
                        osh+=1
                    if board[y+iy*i][x+ix*i]==3 or board[y+iy*i][x+ix*i]==4 or osh==2:
                        if osh>0:spisok.pop()#удаление хода из списка
                        break
    return spisok

def prosmotr_hodov_move(board, spisok):#проверка наличия остальных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            if board[y][x]==3:#пешка
                for ix,iy in (-1,1),(1,1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if board[y+iy][x+ix]==0:
                            spisok.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                        if board[y+iy][x+ix]==1 or board[y+iy][x+ix]==2:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if board[y+iy*2][x+ix*2]==0:
                                    spisok.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка                  
            if board[y][x]==4:#пешка с короной
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0#определение правильности хода
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if board[y+iy*i][x+ix*i]==0:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                            if board[y+iy*i][x+ix*i]==1 or board[y+iy*i][x+ix*i]==2:
                                osh+=1
                            if board[y+iy*i][x+ix*i]==3 or board[y+iy*i][x+ix*i]==4 or osh==2:
                                break
    return spisok

def prosmotr_hodov_i1(board, spisok):#проверка наличия обязательных ходов
    spisok=[]#список ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            spisok=prosmotr_hodov_i1p(board,spisok,x,y)
    return spisok

def prosmotr_hodov_i1p(board, spisok,x,y):
    if board[y][x]==1:#пешка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if board[y+iy][x+ix]==3 or board[y+iy][x+ix]==4:
                    if board[y+iy+iy][x+ix+ix]==0:
                        spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка
    if board[y][x]==2:#пешка с короной
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0#определение правильности хода
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                    if board[y+iy*i][x+ix*i]==3 or board[y+iy*i][x+ix*i]==4:
                        osh+=1
                    if board[y+iy*i][x+ix*i]==1 or board[y+iy*i][x+ix*i]==2 or osh==2:
                        if osh>0:spisok.pop()#удаление хода из списка
                        break
    return spisok

def prosmotr_hodov_i2(board, spisok):#проверка наличия остальных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            if board[y][x]==1:#пешка
                for ix,iy in (-1,-1),(1,-1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if board[y+iy][x+ix]==0:
                            spisok.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                        if board[y+iy][x+ix]==3 or board[y+iy][x+ix]==4:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if board[y+iy*2][x+ix*2]==0:
                                    spisok.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка                  
            if board[y][x]==2:#пешка с короной
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0#определение правильности хода
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if board[y+iy*i][x+ix*i]==0:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                            if board[y+iy*i][x+ix*i]==3 or board[y+iy*i][x+ix*i]==4:
                                osh+=1
                            if board[y+iy*i][x+ix*i]==1 or board[y+iy*i][x+ix*i]==2 or osh==2:
                                break
    return spisok

# init_checkers_sprites()#здесь загружаем изображения пешек
# init_board()#начинаем новую игру
# render_board(-1, -1, -1, -1)#рисуем игровое поле
# doska.bind("<Motion>", mouse_pos_frame)#движение мышки по полю
# doska.bind("<Button-1>", mouse_click)#нажатие левой кнопки

# mainloop()
