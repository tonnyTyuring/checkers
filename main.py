import platform
import socket
import threading
import time
from tkinter import *
from typing import Optional

from pyrsistent import freeze

from tkinter import messagebox

from PIL import Image, ImageTk

from checkersanalyser.common import simplified_board, _get_winning_side
from checkersanalyser.model.board import Board
from checkersanalyser.model.completemove import CompleteMove
from checkersanalyser.model.sides import BLACKES, WHITES
from checkersanalyser.moveanalyser import MoveAnalyser
from checkersanalyser.predrag.movemaker import get_best_move

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

dim = 80


def callback(event):
    global board
    print("clicked at", event.x, event.y, event.x // dim, event.y // dim)
    square = board[event.y // dim][event.x // dim]
    if square == 1:
        board[event.y // dim][event.x // dim] = 2
    elif square == 2:
        board[event.y // dim][event.x // dim] = 1
    elif square == 3:
        board[event.y // dim][event.x // dim] = 4
    elif square == 4:
        board[event.y // dim][event.x // dim] = 3

    render_board(mem_doska, board)


doska = Canvas(gl_okno, width=dim * 8, height=dim * 8, bg='#FFFFFF')
doska.pack(side=LEFT)
mem_doska = Canvas(gl_okno, width=dim * 8, height=dim * 8, bg='#FFFFFF')
mem_doska.bind("<Button-1>", callback)
mem_doska.pack(side=RIGHT)

image_scale = (dim, dim)
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
    # if memcell == camcell:
    #     return memcell
    # if camcell != 0 and memcell != 0:
    #     return memcell
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
    deck.delete('all')
    v1xs = [i * dim * 2 + dim for i in range(4)]
    v2xs = [i * dim * 2 for i in range(4)]
    for ri in range(8):
        xs = v1xs if ri % 2 == 0 else v2xs
        [deck.create_rectangle(i, ri * dim, i + dim, ri * dim + dim, fill="black") for i in xs]

    for i in range(64):
        x = i // 8
        y = i % 8
        z = pole[y][x]
        if z:
            deck.create_image(x * dim, y * dim, anchor=NW, image=peshki[z])


def move_figure(x, y, comand):
    y = 7 - y
    connection.send((chr(x) + chr(y) + chr(comand)).encode('utf8'))  # Передаём информацию]


def update_view():
    new_board = merge_boards(board, get_board_from_camera())
    render_board(doska, new_board)
    gl_okno.after(1000, update_view)


def create_move() -> Optional[CompleteMove]:
    board_clone = [row.copy() for row in board]
    return get_best_move(Board(board_clone), BLACKES)


def update_board(move: CompleteMove):
    print("\n", "Update memory board", "=" * 30)
    global board
    render_board(mem_doska, board)
    board = Board(board).execute_complete_move(move).tolist()
    render_board(mem_doska, board)


def make_move(complete_move: CompleteMove):
    move_figure(*complete_move.moves[0].fr, 1)
    [move_figure(*m.fr, 2) for m in complete_move.moves[1:]]
    move_figure(*complete_move.moves[-1].to, 3)
    [move_figure(*m.get_eaten_cell(), 4) for m in complete_move.moves if m.get_eaten_cell() is not None]


def update_board_with_player_move(player_moves: list[CompleteMove]):
    player_move = player_moves[0]
    if len(player_moves) > 1:
        print("Fuck")
        print(player_moves)
        print("Someone program some custom logic for this")
    update_board(player_move)


def predict_player_move() -> bool:
    global board
    attempts = 10
    s_board = simplified_board(freeze(board))
    while attempts > 0:
        new_board = get_board_from_camera()
        if s_board == new_board:
            return True
        player_moves = MoveAnalyser(board, new_board).calculate_move_for_side(WHITES)
        if len(player_moves) == 0:
            attempts -= 1
            continue
        update_board_with_player_move(player_moves)
        return True
    print("ERROR: Failed to deduce player move")
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(440, 500)
    return messagebox.askyesno("ERROR", f"Failed to deduce player Move\nContinue with computer move?")


def computer_make_move():
    side = _get_winning_side(Board(board))
    if side is not None:
        messagebox.showinfo("WINNER", f"Winner is {side}")
        return
    print("work in progress")
    # Проверить правильность хода игрока исходя из доски с памятью дамок

    success = predict_player_move()
    if not success:
        return

    # обращение к гавно коду superai
    move = create_move()
    if move is None:
        messagebox.showinfo("WINNER", f"Winner is {WHITES}")
        return

    # Передать сигналы хода на роборуку (движение фигуры, собрать седенные фигуры)
    make_move(move)

    # Обновить доск с сделанным компютером ходом
    update_board(move)


def refresh_memory():
    global board
    board = get_board_from_camera()
    board[WHITES.upgrade_line()] = [WHITES.to_queen(c) for c in board[WHITES.upgrade_line()]]
    board[BLACKES.upgrade_line()] = [BLACKES.to_queen(c) for c in board[BLACKES.upgrade_line()]]
    render_board(mem_doska, board)


button1 = Button(gl_okno, width=30, height=5, text="Сделать ход", command=computer_make_move, bg='#AAAAAA')
button1.pack(side=BOTTOM)
button2 = Button(gl_okno, width=30, height=5, text="Refresh Memory Board", command=refresh_memory, bg='#AAAAAA')
button2.pack(side=BOTTOM)

render_board(mem_doska, board)
update_view()


# doska.bind(button., move() )#нажатие левой кнопки

def recv_from_robot():
    while True:
        try:
            msg = connection.recv(4).decode("utf-8")
            if msg == "MOVE":
                button1['state'] = DISABLED
                computer_make_move()
        except RuntimeError:
            pass
        finally:
            button1['state'] = NORMAL
        time.sleep(1)


threading.Thread(target=recv_from_robot).start()
gl_okno.mainloop()
