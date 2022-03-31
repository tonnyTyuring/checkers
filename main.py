import socket
from tkinter import *

import superai2
from checkersanalyser.moveanalyser import MoveAnalyser, Move, simplified_board, get_movement_vector
from checkersanalyser.moveanalyser import Side

CAMERA_IP = "192.168.0.101"
CAMERA_PORT = 2114

ROBOT_HOST = "192.168.0.103"  # IP адрес робота на ктоторый мы отсылаем сообщение
ROBOT_PORT = 3000  # Порт по которому передаётся сообщение
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаём сокет передачи и подключаемся
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Защита от проблем при запуске
s.bind((ROBOT_HOST, ROBOT_PORT))
s.listen(10)
connection, _ = s.accept()

gl_okno = Tk()  # создаём окно
gl_okno.title('Шашки')  # заголовок окна
doska = Canvas(gl_okno, width=800, height=800, bg='#FFFFFF')
doska.pack()

i1 = PhotoImage(file="res/1b.gif")
i2 = PhotoImage(file="res/1bk.gif")
i3 = PhotoImage(file="res/1h.gif")
i4 = PhotoImage(file="res/1hk.gif")
peshki = [0, i1, i2, i3, i4]


def clone_board(src: list[list[int]]) -> list[list[int]]:
    return [row.copy() for row in src]


def deduce_merged_cell(memcell: int, camcell: int) -> int:
    if memcell == camcell:
        return memcell
    if camcell != 0 and memcell != 0:
        return memcell
    return camcell


def merge_boards(from_memory: list[list[int]], from_camera: list[list[int]]) -> list[list[int]]:
    res = []
    for memrow, camerarow in zip(from_memory, from_camera):
        newrow = []
        res.append(newrow)
        for memcell, cameracell in zip(memrow, camerarow):
            newrow.append(deduce_merged_cell(memcell, cameracell))
    return res


def get_data() -> str:
    m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    m.connect((CAMERA_IP, CAMERA_PORT))
    data = m.recv(64).decode('utf8')
    m.close()
    return data


def get_board_from_camera() -> list[list[int]]:
    new_board = [[0 for _ in range(8)] for _ in range(8)]
    data = get_data()
    whites, blacks = data[:32][::-1], data[32:][::-1]
    for i in range(32):
        x = (i * 2) // 8
        y = (i * 2) % 8
        if x % 2 == 1:
            y += 1
        if blacks[i] == '1':
            new_board[7 - x][y] = 3
        if whites[i] == '1':
            new_board[7 - x][y] = 1
    return new_board


board = get_board_from_camera()


def render_board(deck: Canvas, pole: list[list[int]]):  # рисуем игровое поле
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


def move_figure(x, y, comand):
    connection.send((chr(x) + chr(y) + chr(comand)).encode('utf8'))  # Передаём информацию]


def update_view():
    new_board = merge_boards(board, get_board_from_camera())
    render_board(doska, new_board)
    gl_okno.after(1000, update_view)


def create_move() -> list[tuple[int, int]]:
    board_clone = [row.copy() for row in board]
    hod = superai2.hod_kompjutera(board_clone)
    return hod


def update_board(hod: list[tuple[int, int]], side: Side):
    print("\n", "Update memory board", "=" * 30)
    global board
    piece = board[hod[0][0]][hod[0][1]]
    pos = (hod[0][0], hod[0][1])
    for move in hod[1:]:
        move_vector = get_movement_vector(pos, move)
        eaten_place = tuple(b - a for a, b in zip(move_vector, move))
        if side.is_enemy(board[eaten_place[0]][eaten_place[1]]):
            board[eaten_place[0]][eaten_place[1]] = 0
        pos = move
    if any(map(lambda x: x[0] == side.last_enemy_line(), hod)) and piece in (1, 3):
        piece += 1
    board[hod[0][0]][hod[0][1]] = 0
    board[hod[-1][0]][hod[-1][1]] = piece


def make_move(hod):
    memory_board = clone_board(board)
    move_figure(hod[0][0], hod[0][1], 1)
    for i in range(len(hod) - 2):
        move_figure(hod[i + 1][0], hod[i + 1][1], 2)
    move_figure(hod[len(hod) - 1][0], hod[len(hod) - 1][1], 3)

    for i in memory_board:
        print(i)

    packing_figures = []
    for i in range(len(hod) - 1):
        if abs(hod[i][0] - hod[i + 1][0]) > 1:
            for k in range(1, abs(hod[i][0] - hod[i + 1][0])):
                pack_figure = (hod[i][0] + k if hod[i][0] - hod[i + 1][0] < 0 else hod[i][0] - k,
                               hod[i][1] + k if hod[i][1] - hod[i + 1][1] < 0 else hod[i][1] - k)

                print(i, k, pack_figure[0], pack_figure[1])
                print(memory_board[pack_figure[0]][pack_figure[1]])
                if memory_board[pack_figure[0]][7 - pack_figure[1]] == 1 or \
                        memory_board[pack_figure[0]][pack_figure[1]] == 2:
                    packing_figures.append(pack_figure)
                    memory_board[pack_figure[0]][7 - pack_figure[1]] = 0

    print("sending packing figures")
    for i in packing_figures:
        print(i)
        move_figure(i[0], i[1], 4)


def update_board_with_player_move(player_moves: list[Move]):
    if len(player_moves) == 0:
        print("ERROR: Failed to deduce player move")
        return
    player_move = player_moves[0]
    if len(player_moves) > 1:
        print("Fuck")
        print(player_moves)
        print("Someone program some custom logic for this")
    move = player_move.to_list()
    update_board(move, Side.WHITES)


def computer_make_move():
    print("work in progress")
    # Проверить правильность хода игрока исходя из доски с памятью дамок

    new_board = get_board_from_camera()
    if simplified_board(new_board) != simplified_board(board):
        player_moves = MoveAnalyser(board, new_board).calculate_move_for_side(Side.WHITES)
        update_board_with_player_move(player_moves)

    # обращение к гавно коду superai
    move = create_move()

    # Передать сигналы хода на роборуку (движение фигуры, собрать седенные фигуры)
    make_move(move)

    # Обновить доск с сделанным компютером ходом
    update_board(move, Side.BLACKES)


button = Button(gl_okno, width=50, height=5, text="Сделать ход", command=computer_make_move, bg='#AAAAAA')
button.pack()

update_view()
# doska.bind(button., move() )#нажатие левой кнопки

gl_okno.mainloop()
