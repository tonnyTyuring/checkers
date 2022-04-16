from pyrsistent import pvector

from checkersanalyser.model.sides import Side, deduce_side


def score(board: pvector(pvector([int])), target_side: Side) -> float:
    board_score = 0
    for row in board:
        for cell in row:
            if cell == 0:
                continue
            s = deduce_side(cell)
            mul = 1 if s == target_side else -1
            board_score += (1.1 * mul) if s.is_queen(cell) else (1 * mul)
    return board_score
