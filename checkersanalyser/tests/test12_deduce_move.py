from checkersanalyser.model.board import Board
from checkersanalyser.model.sides import WHITES
from checkersanalyser.movemaker import get_best_move, COUNTER


def test():
    board = [
        [3, 0, 3, 0, 3, 0, 3, 0],  # 0
        [0, 3, 0, 3, 0, 3, 0, 3],  # 1
        [3, 0, 3, 0, 3, 0, 3, 0],  # 2
        [0, 0, 0, 0, 0, 0, 0, 0],  # 3
        [0, 0, 0, 0, 0, 0, 0, 0],  # 4
        [0, 1, 0, 1, 0, 1, 0, 1],  # 5
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]
    ]

    res = get_best_move(Board(board), WHITES)
    print(repr(res))
