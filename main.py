import socket
from tkinter import *

from pyrsistent import freeze

import superai2
from checkersanalyser.moveanalyser import MoveAnalyser, Move, simplified_board, get_movement_vector
from checkersanalyser.moveanalyser import Side
from checkersanalyser.movemaker import deduce_best_move

CAMERA_IP = "192.168.0.101"
CAMERA_PORT = 2114

ROBOT_HOST = "0.0.0.0"  # IP адрес робота на ктоторый мы отсылаем сообщение
ROBOT_PORT = 3000  # Порт по которому передаётся сообщение
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаём сокет передачи и подключаемся
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Защита от проблем при запуске
s.bind((ROBOT_HOST, ROBOT_PORT))
s.listen(10)
connection, _ = s.accept()

gl_okno = Tk()  # создаём окно
gl_okno.title('Шашки')
# заголовок окна

lf = LabelFrame(gl_okno)
lf.pack(fill='x')
Label(lf, text="Camera Board").pack(side=LEFT)
Label(lf, text="Memory Board").pack(side=RIGHT)

doska = Canvas(gl_okno, width=800, height=800, bg='#FFFFFF')
doska.pack(side=LEFT)
mem_doska = Canvas(gl_okno, width=800, height=800, bg='#FFFFFF')
mem_doska.pack(side=RIGHT)


from PIL import Image, ImageTk
image_scale = (100, 100)
i1 = ImageTk.PhotoImage(Image.open("res/1b.gif").resize(image_scale))
i2 = ImageTk.PhotoImage(Image.open("res/1bk.gif").resize(image_scale))
i3 = ImageTk.PhotoImage(Image.open("res/1h.gif").resize(image_scale))
i4 = ImageTk.PhotoImage(Image.open("res/1hk.gif").resize(image_scale))
peshki = [0, i1, i2, i3, i4]


def fuck_move(move: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return unfuck_move(move)


def unfuck_move(move: list[tuple[int, int]]) -> list[tuple[int, int]]:
    unfucked_move = []
    for m in move:
        unfucked_move.append((m[0], 7 - m[1]))
    return unfucked_move


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
    # hod = superai2.hod_kompjutera(board_clone)
    return deduce_best_move(board_clone, Side.BLACKES).to_list()


def update_board(hod: list[tuple[int, int]], side: Side):
    print("\n", "Update memory board", "=" * 30)
    global board
    render_board(mem_doska, board)
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
    render_board(mem_doska, board)


def make_move(move, side: Side):
    hod = fuck_move(move)
    memory_board = clone_board(board)
    move_figure(hod[0][0], hod[0][1], 1)
    for i in range(len(hod) - 2):
        move_figure(hod[i + 1][0], hod[i + 1][1], 2)
    move_figure(hod[len(hod) - 1][0], hod[len(hod) - 1][1], 3)

    for i in memory_board:
        print(i)

    packing_figures = []
    pos = (move[0][0], move[0][1])
    for m in move[1:]:
        move_vector = get_movement_vector(pos, m)
        eaten_place = tuple(b - a for a, b in zip(move_vector, m))
        if side.is_enemy(board[eaten_place[0]][eaten_place[1]]):
            packing_figures.append((eaten_place[0], eaten_place[1]))
        pos = m
    packing_figures = fuck_move(packing_figures)

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
    if simplified_board(freeze(new_board)) != simplified_board(freeze(board)):
        player_moves = MoveAnalyser(board, new_board).calculate_move_for_side(Side.WHITES)
        update_board_with_player_move(player_moves)

    # обращение к гавно коду superai
    move = create_move()

    # Передать сигналы хода на роборуку (движение фигуры, собрать седенные фигуры)
    make_move(move, Side.BLACKES)

    # Обновить доск с сделанным компютером ходом
    update_board(move, Side.BLACKES)


button = Button(gl_okno, width=30, height=5, text="Сделать ход", command=computer_make_move, bg='#AAAAAA')
button.pack(side=BOTTOM)

render_board(mem_doska, board)
update_view()
# doska.bind(button., move() )#нажатие левой кнопки

gl_okno.mainloop()
