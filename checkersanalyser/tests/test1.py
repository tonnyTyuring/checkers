from checkersanalyser.moveanalyser import MoveAnalyser, Side
from pyrsistent import v, pvector


def test():
    fromm = [
        [3, 0, 3, 0, 3, 0, 3, 0],  # 0
        [0, 3, 0, 3, 0, 3, 0, 3],  # 1
        [3, 0, 3, 0, 3, 0, 3, 0],  # 2
        [0, 0, 0, 0, 0, 0, 0, 0],  # 3
        [0, 0, 0, 0, 0, 0, 0, 0],  # 4
        [0, 1, 0, 1, 0, 1, 0, 1],  # 5
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]
    ]

    to = [
        [3, 0, 3, 0, 3, 0, 3, 0],  # 0
        [0, 3, 0, 3, 0, 3, 0, 3],  # 1
        [3, 0, 3, 0, 3, 0, 3, 0],  # 2
        [0, 0, 0, 0, 0, 0, 0, 0],  # 3
        [0, 0, 1, 0, 0, 0, 0, 0],  # 4
        [0, 0, 0, 1, 0, 1, 0, 1],  # 5
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]
    ]

    m = MoveAnalyser(fromm, to)

    res = m.calculate_move_for_side(Side.WHITES)
    print(m.calculate_move_for_side(Side.WHITES))
    assert repr(res) == "[{(5, 1) -> (4, 2)}]"
