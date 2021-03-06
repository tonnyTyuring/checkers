from checkersanalyser.model.board import Board
from checkersanalyser.model.sides import BLACKES
from checkersanalyser.predrag.movemaker import get_best_move


def test():
    board = [
        [0, 0, 4, 0, 0, 0, 0, 0],  # 0
        [0, 0, 0, 0, 0, 0, 0, 0],  # 1
        [0, 0, 0, 0, 1, 0, 0, 0],  # 2
        [0, 0, 0, 0, 0, 0, 0, 0],  # 3
        [0, 0, 0, 0, 0, 0, 0, 0],  # 4
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    res2 = get_best_move(Board(board), BLACKES)
    print(repr(res2))
    # assert repr(res2) == "{(0, 2) -> (4, 6) -> (7, 3) -> (4, 0)}"
    assert repr(res2) == "{(0, 2) -> (3, 5)}"
