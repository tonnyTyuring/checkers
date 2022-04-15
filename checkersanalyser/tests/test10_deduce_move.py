from checkersanalyser.moveanalyser import MoveAnalyser, Side
from pyrsistent import v, pvector

from checkersanalyser.movemaker import deduce_best_move


def test():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0],  # 0
        [0, 3, 0, 0, 0, 0, 0, 0],  # 1
        [0, 0, 0, 0, 3, 0, 0, 0],  # 2
        [0, 0, 0, 0, 0, 0, 0, 0],  # 3
        [0, 0, 1, 0, 0, 0, 0, 0],  # 4
        [0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    res = deduce_best_move(board, Side.WHITES)
    print(repr(res))
    assert repr(res) == "{(4, 2) -> (6, 4)}"
