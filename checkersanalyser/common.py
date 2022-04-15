from pyrsistent import pvector, freeze

VALID_PLACES = [(x, y) for y in range(8) for x in range(8)]


def norm(el: int) -> int:
    if el == 0:
        return 0
    if el > 0:
        return 1
    return -1


def add(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return t1[0] + t2[0], t1[1] + t2[1]


def mul(t1: tuple[int, int], i: int) -> tuple[int, int]:
    return t1[0] * i, t1[1] * i


def get_movement_vector(pos1: tuple[int, int], pos2: tuple[int, int]) -> tuple[int, int]:
    return norm(pos2[0] - pos1[0]), norm(pos2[1] - pos1[1])


def simplify_cell(v: int):
    if v == 0:
        return v
    from checkersanalyser.model.sides import deduce_side
    return deduce_side(v).to_pawn(v)


def simplified_board(board: pvector(pvector([int]))) -> pvector(pvector([int])):
    sboard = []
    for row in board:
        sboard.append([simplify_cell(i) for i in row.tolist()])
    return freeze(sboard)


