#Python 3.2.3 / IDLE 3.3.0
#Игра "Шашки". Автор: Волгин Ярослав
#08.08.2012-22.04.2013
import tkinter.messagebox
from tkinter import *
import random
import time
import copy

gl_okno=Tk()#создаём окно
gl_okno.title('Шашки')#заголовок окна
doska=Canvas(gl_okno, width=800,height=800,bg='#FFFFFF')
doska.pack()

n2_spisok=()#конечный список ходов компьютера
ur=2#количество предсказываемых компьютером ходов
k_rez=0#!!!
o_rez=0
figure_x=-1#клетка не задана
is_player_move=True#определение хода игрока(да)


def init_checkers_sprites():#загружаем изображения пешек
    global peshki
    i1=PhotoImage(file="res/1b.gif")
    i2=PhotoImage(file="res/1bk.gif")
    i3=PhotoImage(file="res/1h.gif")
    i4=PhotoImage(file="res/1hk.gif")
    peshki=[0,i1,i2,i3,i4]

def init_board():#начинаем новую игру
    global pole
    pole=[[0,3,0,3,0,3,0,3],
          [3,0,3,0,3,0,3,0],
          [0,3,0,3,0,3,0,3],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]]

def render_board(x_poz_1, y_poz_1, x_poz_2, y_poz_2):#рисуем игровое поле
    global peshki
    global pole
    global red_frame,green_frame
    k=100
    x=0
    doska.delete('all')
    red_frame=doska.create_rectangle(-5, -5, -5, -5, outline="red", width=5)
    green_frame=doska.create_rectangle(-5, -5, -5, -5, outline="green", width=5)

    while x<8*k:#рисуем доску
        y=1*k
        while y<8*k:
            doska.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k
    x=1*k
    while x<8*k:#рисуем доску
        y=0
        while y<8*k:
            doska.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k
    
    for y in range(8):#рисуем стоячие пешки
        for x in range(8):
            z=pole[y][x]
            if z:  
                if (x_poz_1,y_poz_1)!=(x,y):#стоячие пешки?
                    doska.create_image(x*k,y*k, anchor=NW, image=peshki[z])
    #рисуем активную пешку
    z=pole[y_poz_1][x_poz_1]
    if z:#???
        doska.create_image(x_poz_1*k,y_poz_1*k, anchor=NW, image=peshki[z],tag='ani')
    #вычисление коэф. для анимации
    kx = 1 if x_poz_1<x_poz_2 else -1
    ky = 1 if y_poz_1<y_poz_2 else -1
    for i in range(abs(x_poz_1-x_poz_2)):#анимация перемещения пешки
        for ii in range(33):
            doska.move('ani',0.03*k*kx,0.03*k*ky)
            doska.update()#обновление
            time.sleep(0.01)

def end_message(s):
    global is_player_move
    z='Игра завершена'
    if s==1:
        print(z, 'Вы победили!Нажми "Да" что бы начать заново.')
    if s==2:
        print(z, 'Вы проиграли!Нажми "Да" что бы начать заново.')
    if s==3:
        print(z, 'Ходов больше нет.Нажми "Да" что бы начать заново.')

def mouse_pos_frame(event):#выбор клетки для хода 1
    x,y=(event.x)//100,(event.y)//100#вычисляем координаты клетки
    doska.coords(green_frame, x * 100, y * 100, x * 100 + 100, y * 100 + 100)#рамка в выбранной клетке

def mouse_click(event):#выбор клетки для хода 2
    global figure_x, figure_y, figure_next_x, figre_next_y
    global is_player_move
    x,y=(event.x)//100,(event.y)//100#вычисляем координаты клетки
    if pole[y][x]==1 or pole[y][x]==2:#проверяем пешку игрока в выбранной клетке
        doska.coords(red_frame, x * 100, y * 100, x * 100 + 100, y * 100 + 100)#рамка в выбранной клетке
        figure_x, figure_y= x, y
    else:
        if figure_x!=-1:#клетка выбрана
            figure_next_x, figre_next_y= x, y
            if f_hi:#ход игрока?
                hod_igroka()
                if not(f_hi):
                    time.sleep(0.5)
                    hod_kompjutera()#передаём ход компьютеру
                    #gl_okno.after(500,hod_kompjutera(0))#!!!#передаём ход компьютеру
            figure_x=-1#клетка не выбрана
            doska.coords(red_frame, -5, -5, -5, -5)#рамка вне поля
     
def hod_kompjutera():#!!!
    global is_player_move
    global n2_spisok
    proverka_hk(1,(),[])
    if n2_spisok:#проверяем наличие доступных ходов
        kh=len(n2_spisok)#количество ходов
        th=random.randint(0,kh-1)#случайный ход
        dh=len(n2_spisok[th])#длина хода
        for h in n2_spisok:#!!!для отладки!!!
            h=h#!!!для отладки!!!
        for i in range(dh-1):
            #выполняем ход
            hod(1,n2_spisok[th][i][0],n2_spisok[th][i][1],n2_spisok[th][1+i][0],n2_spisok[th][1+i][1])
        n2_spisok=[]#очищаем список ходов
        f_hi=True#ход игрока доступен

    #определяем победителя
    s_k,s_i=skan()
    if not(s_i):
            end_message(2)
    elif not(s_k):
            end_message(1)
    elif f_hi and not(spisok_hi()):
            end_message(3)
    elif not(f_hi) and not(spisok_hk()):
            end_message(3)

def spisok_hk():#составляем список ходов компьютера
    spisok=prosmotr_hodov_eat([])#здесь проверяем обязательные ходы
    if not(spisok):
        spisok=prosmotr_hodov_move([])#здесь проверяем оставшиеся ходы
    return spisok

def proverka_hk(tur,n_spisok,spisok):#!!!
    global pole
    global n2_spisok
    global l_rez,k_rez,o_rez
    if not(spisok):#если список ходов пустой...
        spisok=spisok_hk()#заполняем

    if spisok:
        k_pole=copy.deepcopy(pole)#копируем поле
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:#проходим все ходы по списку
            t_spisok=hod(0,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_spisok:#если существует ещё ход
                proverka_hk(tur,(n_spisok+((poz1_x,poz1_y),)),t_spisok)
            else:
                proverka_hi(tur,[])
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
        s_k,s_i=skan()#подсчёт результата хода
        o_rez+=(s_k-s_i)
        k_rez+=1

def spisok_hi():#составляем список ходов игрока
    spisok=prosmotr_hodov_i1([])#здесь проверяем обязательные ходы
    if not(spisok):
        spisok=prosmotr_hodov_i2([])#здесь проверяем оставшиеся ходы
    return spisok
    
def proverka_hi(tur,spisok):
    global pole,k_rez,o_rez
    global ur
    if not(spisok):
        spisok=spisok_hi()

    if spisok:#проверяем наличие доступных ходов
        k_pole=copy.deepcopy(pole)#копируем поле
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:                    
            t_spisok=hod(0,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_spisok:#если существует ещё ход
                proverka_hi(tur,t_spisok)
            else:
                if tur<ur:
                    proverka_hk(tur+1,(),[])
                else:
                    s_k,s_i=skan()#подсчёт результата хода
                    o_rez+=(s_k-s_i)
                    k_rez+=1

            pole=copy.deepcopy(k_pole)#возвращаем поле
    else:#доступных ходов нет
        s_k,s_i=skan()#подсчёт результата хода
        o_rez+=(s_k-s_i)
        k_rez+=1

def skan():#подсчёт пешек на поле
    global pole
    s_i=0
    s_k=0
    for i in range(8):
        for ii in pole[i]:
            if ii==1:s_i+=1
            if ii==2:s_i+=3
            if ii==3:s_k+=1
            if ii==4:s_k+=3
    return s_k,s_i

def hod_igroka():
    global figure_x,figure_y,figure_next_x,figre_next_y
    global is_player_move
    f_hi=False#считаем ход игрока выполненным
    spisok=spisok_hi()
    if spisok:
        if ((figure_x, figure_y), (figure_next_x, figre_next_y)) in spisok:#проверяем ход на соответствие правилам игры
            t_spisok=hod(1, figure_x, figure_y, figure_next_x, figre_next_y)#если всё хорошо, делаем ход
            if t_spisok:#если есть ещё ход той же пешкой
                f_hi=True#считаем ход игрока невыполненным
        else:
            f_hi=True#считаем ход игрока невыполненным
    doska.update()#!!!обновление

def hod(f,poz1_x,poz1_y,poz2_x,poz2_y):
    global pole
    if f:render_board(poz1_x, poz1_y, poz2_x, poz2_y)#рисуем игровое поле
    #превращение
    if poz2_y==0 and pole[poz1_y][poz1_x]==1:
        pole[poz1_y][poz1_x]=2
    #превращение
    if poz2_y==7 and pole[poz1_y][poz1_x]==3:
        pole[poz1_y][poz1_x]=4
    #делаем ход           
    pole[poz2_y][poz2_x]=pole[poz1_y][poz1_x]
    pole[poz1_y][poz1_x]=0

    #рубим пешку игрока
    kx=ky=1
    if poz1_x<poz2_x:kx=-1
    if poz1_y<poz2_y:ky=-1
    x_poz,y_poz=poz2_x,poz2_y
    while (poz1_x!=x_poz) or (poz1_y!=y_poz):
        x_poz+=kx
        y_poz+=ky
        if pole[y_poz][x_poz]!=0:
            pole[y_poz][x_poz]=0
            if f:render_board(-1, -1, -1, -1)#рисуем игровое поле
            #проверяем ход той же пешкой...
            if pole[poz2_y][poz2_x]==3 or pole[poz2_y][poz2_x]==4:#...компьютера
                return prosmotr_hodov_k1p([],poz2_x,poz2_y)#возвращаем список доступных ходов
            elif pole[poz2_y][poz2_x]==1 or pole[poz2_y][poz2_x]==2:#...игрока
                return prosmotr_hodov_i1p([],poz2_x,poz2_y)#возвращаем список доступных ходов
    if f:render_board(poz1_x, poz1_y, poz2_x, poz2_y)#рисуем игровое поле

def prosmotr_hodov_eat(spisok):#проверка наличия обязательных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            spisok=prosmotr_hodov_k1p(spisok,x,y)
    return spisok

def prosmotr_hodov_k1p(spisok,x,y):
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

def prosmotr_hodov_move(spisok):#проверка наличия остальных ходов
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

def prosmotr_hodov_i1(spisok):#проверка наличия обязательных ходов
    spisok=[]#список ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            spisok=prosmotr_hodov_i1p(spisok,x,y)
    return spisok

def prosmotr_hodov_i1p(spisok,x,y):
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

def prosmotr_hodov_i2(spisok):#проверка наличия остальных ходов
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

init_checkers_sprites()#здесь загружаем изображения пешек
init_board()#начинаем новую игру
render_board(-1, -1, -1, -1)#рисуем игровое поле
doska.bind("<Motion>", mouse_pos_frame)#движение мышки по полю
doska.bind("<Button-1>", mouse_click)#нажатие левой кнопки


mainloop()
