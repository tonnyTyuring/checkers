from checkersanalyser.model.sides import WHITES
from checkersanalyser.moveanalyser import MoveAnalyser
from pyrsistent import v, pvector


def test():
    fromm = [
        [3, 0, 0, 0, 3, 0, 3, 0],  # 0
        [0, 3, 0, 3, 0, 3, 0, 3],  # 1
        [0, 0, 0, 0, 3, 0, 3, 0],  # 2
        [0, 3, 0, 0, 0, 0, 0, 0],  # 3
        [0, 0, 1, 0, 0, 0, 0, 0],  # 4
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    to = [
        [3, 0, 1, 0, 3, 0, 3, 0],
        [0, 0, 0, 3, 0, 3, 0, 3],
        [0, 0, 0, 0, 3, 0, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    m = MoveAnalyser(fromm, to)
    res = m.calculate_move_for_side(WHITES)
    print(res)
    assert repr(res) == "[{(4, 2) -> (2, 0) -> (0, 2)}]"
