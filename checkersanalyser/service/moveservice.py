from pyrsistent import pvector

from checkersanalyser.model.board import Board
from checkersanalyser.model.completemove import CompleteMove
from checkersanalyser.model.move import Move
from checkersanalyser.model.piece import Piece
from checkersanalyser.model.sides import Side
from checkersanalyser.service.pieceservice import get_moves_for_piece, get_eat_moves_for_piece


def _finish_move(movechain: pvector([Move])) -> list[CompleteMove]:
    m = movechain[-1]
    if not m.is_eat_move:
        return [CompleteMove(movechain)]
    p = Piece(m.to[0], m.to[1], m.piece.board.execute_move(m))
    next_moves = get_eat_moves_for_piece(p)
    if len(next_moves) == 0:
        return [CompleteMove(movechain)]
    return [fm for m in next_moves for fm in _finish_move(movechain.append(m))]


def _get_all_complete_moves_for_piece(p: Piece) -> list[CompleteMove]:
    if len(em := get_eat_moves_for_piece(p)) != 0:
        return [cm for m in em for cm in _finish_move(pvector([m]))]
    return [CompleteMove(pvector([m])) for m in get_moves_for_piece(p)]


def _obligatory_filter(moves: list[CompleteMove]) -> list[CompleteMove]:
    eat_moves = [m for m in moves if m.moves[0].is_eat_move]
    if len(eat_moves) != 0:
        return eat_moves
    return moves


def get_all_complete_moves_for_side(b: Board, side: Side) -> list[CompleteMove]:
    return _obligatory_filter([cm for p in b.get_pieces_for_side(side) for cm in _get_all_complete_moves_for_piece(p)])
