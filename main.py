import functools
import platform
import socket
import threading
import time
from functools import cached_property
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


def synchronized(wrapped):
    lock = threading.Lock()

    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        with lock:
            return wrapped(*args, **kwargs)

    return _wrap


def error_msg():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(440, 500)
    messagebox.showerror("Move Prediction Error", "Failed to deduce player Move")


def predict_player_move(board) -> Optional[list[CompleteMove]]:
    print("Predicting player move")
    attempts = 10
    while attempts > 0:
        new_board = get_board_from_camera()
        player_moves = MoveAnalyser(board, new_board).calculate_move_for_side(WHITES)
        if len(player_moves) == 0:
            attempts -= 1
            time.sleep(0.1)
            continue
        return player_moves
    print("ERROR: Failed to deduce player move")
    return None


class RobotClient:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаём сокет передачи и подключаемся
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Защита от проблем при запуске
        self.s.bind((ROBOT_HOST, ROBOT_PORT))
        self.s.listen(10)

    def make_move(self, complete_move: CompleteMove):
        self.move_figure(*complete_move.moves[0].fr, 1)
        [self.move_figure(*m.fr, 2) for m in complete_move.moves[1:]]
        self.move_figure(*complete_move.moves[-1].to, 3)
        [self.move_figure(*m.get_eaten_cell(), 4) for m in complete_move.moves if m.get_eaten_cell() is not None]

    @cached_property
    def get_connection(self):
        connection, _ = self.s.accept()
        return connection

    def move_figure(self, x, y, command):
        y = 7 - y
        self.get_connection.send((chr(x) + chr(y) + chr(command)).encode('utf8'))


def get_images(dim: int) -> list[ImageTk]:
    image_scale = (dim, dim)
    i1 = ImageTk.PhotoImage(Image.open("res/1b.gif").resize(image_scale))
    i2 = ImageTk.PhotoImage(Image.open("res/1bk.gif").resize(image_scale))
    i3 = ImageTk.PhotoImage(Image.open("res/1h.gif").resize(image_scale))
    i4 = ImageTk.PhotoImage(Image.open("res/1hk.gif").resize(image_scale))
    return [0, i1, i2, i3, i4]


def create_move(board) -> Optional[CompleteMove]:
    print("Starting to deduce AI move")
    board_clone = Board(board)
    # if (board_clone, BLACKES) in worker.mem:
    #     move = worker.mem[(board_clone, BLACKES)]
    #     worker.stop()
    #     return move
    # worker.stop()
    return get_best_move(board_clone, BLACKES, randomized=True)


@synchronized
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


class CheckersGameWindow:

    def __init__(self, dim=80):
        self.gl_okno = Tk()  # создаём окно
        self.gl_okno.title('Шашки')
        self.dim = dim
        self.images = get_images(self.dim)
        self.lf = LabelFrame(self.gl_okno)
        self.lf.pack(fill='x')
        Label(self.lf, text="Camera Board").pack(side=LEFT)
        Label(self.lf, text="Memory Board").pack(side=RIGHT)
        self.camera_board_canvas = Canvas(self.gl_okno, width=dim * 8, height=dim * 8, bg='#FFFFFF')
        self.camera_board_canvas.pack(side=LEFT)
        self.memory_board_canvas = Canvas(self.gl_okno, width=dim * 8, height=dim * 8, bg='#FFFFFF')
        self.memory_board_canvas.pack(side=RIGHT)

        self.button1 = Button(self.gl_okno, width=30, height=5, text="Сделать ход", bg='#AAAAAA')
        self.button1.pack(side=BOTTOM)
        self.button2 = Button(self.gl_okno, width=30, height=5, text="Refresh Memory Board", bg='#AAAAAA')
        self.button2.pack(side=BOTTOM)

    def render_camera_board(self):
        camera_board = get_board_from_camera()
        self._render_board(self.camera_board_canvas, camera_board)

    def render_memory_board(self, memory_board):
        self._render_board(self.memory_board_canvas, memory_board)

    def _render_board(self, canvas: Canvas, board: list[list[int]]):  # рисуем игровое поле
        dim = self.dim
        canvas.delete('all')
        v1xs = [i * dim * 2 + dim for i in range(4)]
        v2xs = [i * dim * 2 for i in range(4)]
        for ri in range(8):
            xs = v1xs if ri % 2 == 0 else v2xs
            [canvas.create_rectangle(i, ri * dim, i + dim, ri * dim + dim, fill="black") for i in xs]

        for i in range(64):
            x = i // 8
            y = i % 8
            z = board[y][x]
            if z:
                canvas.create_image(x * dim, y * dim, anchor=NW, image=self.images[z])

    def update_view(self):
        self.render_camera_board()
        self.gl_okno.after(1000, self.update_view)


class CheckersGame:

    def __init__(self, window: CheckersGameWindow):
        self.board = get_board_from_camera()
        self.window = window
        self.window.button1.configure(command=self.computer_make_move)
        self.window.button2.configure(command=self.refresh_memory_board)
        self.window.memory_board_canvas.bind("<Button-1>", self.mem_board_click_handle)
        self.robot_client = RobotClient()

    def mem_board_click_handle(self, event):
        dim = self.window.dim
        board = self.board
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

        self.window.render_memory_board(board)

    def update_board(self, move: CompleteMove):
        print(f"Updating memory board with {move}")
        self.window.render_memory_board(self.board)
        self.board = Board(self.board).execute_complete_move(move).tolist()
        self.window.render_memory_board(self.board)

    def update_board_with_player_move(self, player_moves: list[CompleteMove]):
        player_move = player_moves[0]
        if len(player_moves) > 1:
            print("Fuck")
            print(player_moves)
            print("Someone program some custom logic for this")
        print(f"Updating board with player move: {player_move}")
        self.update_board(player_move)

    def refresh_memory_board(self):
        self.board = get_board_from_camera()
        self.board[WHITES.upgrade_line()] = [WHITES.to_queen(c) for c in self.board[WHITES.upgrade_line()]]
        self.board[BLACKES.upgrade_line()] = [BLACKES.to_queen(c) for c in self.board[BLACKES.upgrade_line()]]
        self.window.render_memory_board(self.board)

    def computer_make_move(self):
        side = _get_winning_side(Board(self.board))
        if side is not None:
            messagebox.showinfo("WINNER", f"Winner is {side}")
            return
        # Проверить правильность хода игрока исходя из доски с памятью дамок
        s_board = simplified_board(freeze(self.board))
        if s_board == get_board_from_camera():
            self.do_robot_move()
            return

        player_moves = predict_player_move(self.board)
        if player_moves is None:
            error_msg()
            return
        self.update_board_with_player_move(player_moves)
        self.do_robot_move()

    def do_robot_move(self):
        move = create_move(self.board)
        if move is None:
            messagebox.showinfo("WINNER", f"Winner is {WHITES}")
            return

        # Передать сигналы хода на роборуку (движение фигуры, собрать седенные фигуры)
        self.robot_client.make_move(move)

        # Обновить доск с сделанным компютером ходом
        self.update_board(move)

    def recv_from_robot(self):
        while True:
            try:
                msg = self.robot_client.get_connection.recv(4).decode("utf-8")
                if msg == "MOVE":
                    self.window.button1['state'] = DISABLED
                    self.computer_make_move()
            except RuntimeError:
                pass
            finally:
                self.window.button1['state'] = NORMAL
            time.sleep(1)

    def start(self):
        threading.Thread(target=self.recv_from_robot).start()
        self.window.update_view()
        self.window.render_memory_board(self.board)
        self.window.gl_okno.mainloop()


if __name__ == "__main__":
    game = CheckersGame(CheckersGameWindow())
    game.start()
