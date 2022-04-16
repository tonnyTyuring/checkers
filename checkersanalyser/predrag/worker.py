import time
from threading import Thread

from checkersanalyser.model.board import Board
from checkersanalyser.model.sides import Side
from checkersanalyser.moveresolver.completemoveresolver import get_all_valid_moves_for_side

STOP = [False]


class PredragWorker:

    def __init__(self):
        self.mem = {}
        self.th = None

    def start(self, b: Board, ai_side: Side):
        STOP[0] = False
        self.th = Thread(target=lambda: self._start(b, ai_side))
        self.th.start()

    def stop(self):
        STOP[0] = True
        self.th.join()
        STOP[0] = False

    def _start(self, b: Board, ai_side: Side):
        self.work(b, ai_side)
        while not STOP[0]:
            time.sleep(0.1)
        self.mem = {}

    def work(self, b: Board, ai_side: Side):
        from checkersanalyser.predrag.movemaker import get_best_move
        boards = [b.execute_complete_move(pm) for pm in get_all_valid_moves_for_side(b, ai_side.opposite_side())]
        boards = [b] + boards
        for board in boards:
            if STOP[0]:
                return
            m = get_best_move(board, ai_side)
            self.mem[(board, ai_side)] = m
