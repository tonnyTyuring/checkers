from checkersanalyser.model.board import Board
from checkersanalyser.model.sides import WHITES
from checkersanalyser.movemaker import get_best_move


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

    res2 = get_best_move(Board(board), WHITES)
    print(repr(res2))
    assert repr(res2) == "{(4, 2) -> (6, 4) -> (4, 6)}"
