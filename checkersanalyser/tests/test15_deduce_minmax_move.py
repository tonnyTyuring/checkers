from checkersanalyser.common import Side
from checkersanalyser.movemaker import deduce_best_min_max_move

from checkersanalyser.movemaker import deduce_best_complete_move


def test():
    board = [
        [0, 0, 3, 0, 0, 0, 0, 0],  # 0
        [0, 0, 0, 0, 0, 0, 0, 0],  # 1
        [0, 0, 0, 0, 3, 0, 0, 0],  # 2
        [0, 3, 0, 0, 0, 0, 0, 0],  # 3
        [0, 0, 1, 0, 0, 0, 0, 0],  # 4
        [0, 0, 0, 3, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    res1 = deduce_best_complete_move(board, Side.WHITES)
    print(repr(res1))
    assert repr(res1) == "{(4, 2) -> (2, 0)}"

    res2 = deduce_best_min_max_move(board, Side.WHITES)
    print(repr(res2))
    assert repr(res2) == "{(4, 2) -> (6, 4) -> (4, 6)}"
