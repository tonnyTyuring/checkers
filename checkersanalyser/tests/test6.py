from checkersanalyser.moveanalyser import MoveAnalyser, Side
from pyrsistent import v, pvector


def test():
    fromm = [
        [3, 0, 0, 0, 3, 0, 3, 0],  # 0
        [0, 3, 0, 3, 0, 3, 0, 3],  # 3
        [0, 0, 0, 0, 0, 0, 3, 0],  # 2
        [0, 0, 0, 3, 0, 0, 0, 0],  # 1
        [0, 0, 0, 0, 0, 0, 0, 0],  # 4
        [0, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    to = [
        [3, 0, 0, 0, 3, 0, 3, 0],  # 0
        [0, 0, 0, 0, 0, 3, 0, 3],  # 3
        [2, 0, 0, 0, 0, 0, 3, 0],  # 2
        [0, 0, 0, 0, 0, 0, 0, 0],  # 1
        [0, 0, 0, 0, 0, 0, 0, 0],  # 4
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    m = MoveAnalyser(fromm, to)
    res = m.calculate_move_for_side(Side.WHITES)
    print(res)
    expected = "[{(5, 1) -> (2, 4) -> (0, 2) -> (2, 0)}]"
    assert repr(res) == expected
