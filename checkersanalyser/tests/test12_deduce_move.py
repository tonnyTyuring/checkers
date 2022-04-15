from checkersanalyser.common import Side
from checkersanalyser.movemaker import deduce_best_move


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

    res = deduce_best_move(board, Side.WHITES)
    print(repr(res))
