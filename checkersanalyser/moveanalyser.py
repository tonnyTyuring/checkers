from pyrsistent import freeze
from checkersanalyser.model.board import Board
from checkersanalyser.model.completemove import CompleteMove
from checkersanalyser.model.sides import Side
from checkersanalyser.moveresolver.completemoveresolver import get_all_valid_moves_for_side


def logged(func):
    def logged_func(*args, **kwargs):
        self = args[0]
        print(f"INPUT:from: {self._meta['from']}")
        print(f"INPUT:to: {self._meta['to']}")
        print(f"INPUT:args: {args[1:]} {kwargs}")
        res = func(*args, **kwargs)
        print(f"OUTPUT: {res}")
        return res

    return logged_func


class MoveAnalyser:

    def __init__(self, fromm: list[list[int]], to: list[list[int]]):
        self._meta = {"from": fromm, "to": to}
        self.fromm = Board(freeze(fromm))
        self.to = Board(freeze(to)).simplified()

    @logged
    def calculate_move_for_side(self, side: Side) -> list[CompleteMove]:
        cmoves = get_all_valid_moves_for_side(self.fromm, side)
        valid_moves = []
        for cmove in cmoves:
            result_board = self.fromm.execute_complete_move(cmove)
            if result_board.simplified() == self.to:
                valid_moves.append(cmove)
        return valid_moves
