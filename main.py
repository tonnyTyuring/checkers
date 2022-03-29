import socket
import time
from _socket import SHUT_RDWR
from tkinter import *
import superai2

# import RobotMoveFigure

'''connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "192.168.0.101"
PORT = 2114
#connection.connect((IP, PORT))
s = socket.socket(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, PORT))

while(True):
    for i in range(2):
        board = [['#' if i % 2 == (0 if j % 2 == 0 else 1) else ' ' for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in range(8):
                if (board[i][j] == '#'):
                    board[i][7-j] = s.recv(1).decode("utf8")
        for c in board:
            print(c)
        print("=============================")

    time.sleep(10)
    print("=============================")
    connection.close()
'''

CAMERA_IP = "192.168.0.101"
CAMERA_PORT = 2114

# board = [['#' if i % 2 == (1 if j % 2 == 0 else 0) else ' ' for i in range(8)] for j in range(8)]

# Init Board
gl_okno = Tk()  # создаём окно
gl_okno.title('Шашки')  # заголовок окна
doska = Canvas(gl_okno, width=800, height=800, bg='#FFFFFF')
doska.pack()

i1 = PhotoImage(file="res/1b.gif")
i2 = PhotoImage(file="res/1bk.gif")
i3 = PhotoImage(file="res/1h.gif")
i4 = PhotoImage(file="res/1hk.gif")
peshki = [0, i1, i2, i3, i4]

board = [[0 for i in range(8)] for j in range(8)]
memory_board = [[0 for i in range(8)] for j in range(8)]


def get_data():
    m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    m.connect((CAMERA_IP, CAMERA_PORT))
    data = m.recv(64).decode('utf8')
    m.close()
    return data


def update_board():
    global board
    board = [[0 for i in range(8)] for j in range(8)]
    data = get_data()
    whites, blacks = data[:32][::-1], data[32:][::-1]
    for i in range(32):
        x = (i * 2) // 8
        y = (i * 2) % 8
        if x % 2 == 1:
            y += 1
        if blacks[i] == '1':
            board[7 - x][y] = 3
            # board[int(data[i%8])][int(data[i//8])] = int(data[i]) if (i%8) % 2 == (0 if (i//8) % 2 == 0 else 1) else 0
        if whites[i] == '1':
            board[7 - x][y] = 1
    print(data)
    print("------------------------------------")


def render_board(deck, pole):  # рисуем игровое поле
    k = 100
    x = 0
    deck.delete('all')

    while x < 8 * k:  # рисуем доску
        y = 1 * k
        while y < 8 * k:
            deck.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k
    x = 1 * k
    while x < 8 * k:  # рисуем доску
        y = 0
        while y < 8 * k:
            deck.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k

    for y in range(8):  # рисуем стоячие пешки
        for x in range(8):
            z = pole[y][x]
            if z:
                deck.create_image(x * k, y * k, anchor=NW, image=peshki[z])


ROBOT_HOST = "192.168.0.103"  # IP адрес робота на ктоторый мы отсылаем сообщение
ROBOT_PORT = 3000  # Порт по которому передаётся сообщение
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаём сокет передачи и подключаемся
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Защита от проблем при запуске
s.bind((ROBOT_HOST, ROBOT_PORT))
s.listen(10)
connection, _ = s.accept()


def move_figure(x, y, comand):
    connection.send((chr(x) + chr(y) + chr(comand)).encode('utf8'))  # Передаём информацию]


def update():
    update_board()
    render_board(doska, board)
    gl_okno.after(1000, update)


def update_memory_board():
    # Входит значение доски перед/после ходом и память

    print("Memory board")
    for m in memory_board:
        print(m)

    print("board")
    for i in board:
        print(i)

    for x in range(8):
        for y in range(8):
            if memory_board[x][y] == 4 and board[x][y] == 3:
                memory_board[x][y] = 4
            else:
                memory_board[x][y] = board[x][y]

    for x in range(8):
        memory_board[7][x] = 4 if board[7][x] == 3 else board[7][x]

    print("Memory board after update")
    for m in memory_board:
        print(m)


def move():
    move_board = [[0 for i in range(8)] for j in range(8)]

    for x in range(8):
        for y in range(8):
            move_board[x][y] = memory_board[x][y]

    hod = superai2.hod_kompjutera(move_board)
    print("hod: ", hod)

    move_figure(hod[0][0], hod[0][1], 1)
    for i in range(len(hod) - 2):
        move_figure(hod[i + 1][0], hod[i + 1][1], 2)
    move_figure(hod[len(hod) - 1][0], hod[len(hod) - 1][1], 3)

    update_memory_board()


    if board[hod[0][0]][7-hod[0][1]] == 4:
        memory_board[hod[0][0]][7-hod[0][1]] = 0
        memory_board[hod[len(hod) - 1][0]][hod[len(hod) - 1][1]] = 4

    packing_figures = []
    for i in range(len(hod) - 1):
        if abs(hod[i][0] - hod[i + 1][0]) > 1:
            for k in range(1, abs(hod[i][0] - hod[i + 1][0])):
                pack_figure = (hod[i][0] + k if hod[i][0] - hod[i + 1][0] < 0 else hod[i][0] - k,
                               hod[i][1] + k if hod[i][1] - hod[i + 1][1] < 0 else hod[i][1] - k)

                print(k, pack_figure[0], pack_figure[1])
                print(memory_board[pack_figure[0]][pack_figure[1]])
                if memory_board[pack_figure[0]][pack_figure[1]] == 1 or \
                        memory_board[pack_figure[0]][pack_figure[1]] == 2:
                    packing_figures.append(pack_figure)

    for i in packing_figures:
        move_figure(i[0], i[1], 4)


button = Button(gl_okno, width=50, height=5, text="Сделать ход", command=move, bg='#AAAAAA')
button.pack()

update()
# doska.bind(button., move() )#нажатие левой кнопки

gl_okno.mainloop()
