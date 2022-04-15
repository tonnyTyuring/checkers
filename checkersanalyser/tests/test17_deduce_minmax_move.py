from checkersanalyser.common import Side
from checkersanalyser.movemaker import deduce_best_min_max_move


def test():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0],  # 0
        [0, 0, 0, 0, 0, 0, 0, 0],  # 1
        [0, 0, 0, 0, 0, 0, 0, 0],  # 2
        [0, 0, 0, 0, 0, 0, 0, 0],  # 3
        [3, 0, 1, 0, 0, 0, 0, 0],  # 4
        [0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    res2 = deduce_best_min_max_move(board, Side.BLACKES)
    print(repr(res2))
    assert res2 is None
