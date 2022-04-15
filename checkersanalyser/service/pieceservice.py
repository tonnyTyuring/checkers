from typing import Optional

from checkersanalyser.common import get_movement_vector, add, norm, VALID_PLACES
from checkersanalyser.model.move import Move
from checkersanalyser.model.piece import Piece
from checkersanalyser.service.queenservice import get_queen_moves


def _get_next_cell(fr: tuple[int, int], to: tuple[int, int]) -> tuple[int, int]:
    vec = get_movement_vector(fr, to)
    return add(to, vec)


def _is_back_move(p: Piece, fr: tuple[int, int], to: tuple[int, int]):
    direction = norm(to[0] - fr[0])  # 1 or -1 (up or down)
    return direction != p.side.target_direction


def _get_valid_move(p: Piece, fr: tuple[int, int], to: tuple[int, int]) -> Optional[tuple[int, int]]:
    if not p.side.has_enemy(to, p.board) and _is_back_move(p, fr, to):
        return None
    if p.side.has_enemy(to, p.board):
        to = _get_next_cell(p.pos, to)
    if to not in VALID_PLACES:
        return None
    if p.board[to] != 0:
        return None
    return to


def _get_pawn_moves(p: Piece) -> list[Move]:
    i = p.pos[0]
    j = p.pos[1]
    moves = [(i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1)]
    moves = [m for m in moves if m in VALID_PLACES]
    moves = [tm for m in moves if (tm := _get_valid_move(p, p.pos, m)) is not None]
    return [Move(p.pos, m, p.board) for m in moves]


def _obligatory_filter(moves: list[Move]):
    eat_moves = [m for m in moves if m.is_eat_move]
    if len(eat_moves) != 0:
        return eat_moves
    return moves


def get_eat_moves_for_piece(p: Piece) -> list[Move]:
    if not p.is_queen:
        return [m for m in _get_pawn_moves(p) if m.is_eat_move]
    return [m for m in get_queen_moves(p) if m.is_eat_move]


def get_moves_for_piece(p: Piece) -> list[Move]:
    if not p.is_queen:
        return _obligatory_filter(_get_pawn_moves(p))
    return _obligatory_filter(get_queen_moves(p))
