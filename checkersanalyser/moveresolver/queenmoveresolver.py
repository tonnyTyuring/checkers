from checkersanalyser.common import mul, add, VALID_PLACES
from checkersanalyser.model.move import Move
from checkersanalyser.model.piece import Piece


def _explore_direction(moves: list[tuple[int, int]], d: tuple[int, int], p: Piece):
    board = p.board
    for i in range(1, 9):
        to = add(p.pos, mul(d, i))
        if to not in VALID_PLACES:
            return
        if board[to] == 0:
            moves.append(to)
        lookahead = add(to, d)
        if p.side.is_enemy(board[to]) and lookahead in VALID_PLACES and board[lookahead] == 0:
            continue
        if board[to] != 0:
            return


def get_queen_moves(p: Piece) -> list[Move]:
    directions = [(- 1, - 1), (- 1, 1), (1, - 1), (1, 1)]
    moves = []
    for d in directions:
        _explore_direction(moves, d, p)
    return [Move(p.pos, m, p.board) for m in moves if m in VALID_PLACES and p.board[m] == 0]
