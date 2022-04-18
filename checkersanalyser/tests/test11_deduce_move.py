from checkersanalyser.model.board import Board
from checkersanalyser.model.sides import WHITES
from checkersanalyser.predrag.movemaker import get_best_move
from checkersanalyser.common import timeit


@timeit("test11")
def test():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0],  # 0
        [0, 3, 0, 0, 0, 0, 0, 0],  # 1
        [0, 0, 0, 0, 3, 0, 0, 0],  # 2
        [0, 3, 0, 0, 0, 0, 0, 0],  # 3
        [0, 0, 1, 0, 0, 0, 0, 0],  # 4
        [0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    res = get_best_move(Board(board), WHITES)
    print(repr(res))
    assert repr(res) == "{(4, 2) -> (2, 0) -> (0, 2) -> (3, 5) -> (6, 2)}"
