from __future__ import annotations

import operator

from pyrsistent import pvector

from math import inf
from checkersanalyser.model.board import Board
from checkersanalyser.model.completemove import CompleteMove
from checkersanalyser.model.node import Node
from checkersanalyser.model.sides import Side, deduce_side
from checkersanalyser.service.moveservice import get_all_complete_moves_for_side


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


def _alphabeta(node: Node, depth: int, alpha: int | inf, beta: int | inf, target_side: Side) -> float:
    if depth == 0 or node.is_terminal():
        return score(node.board.pboard, target_side)
    maximizing_player = target_side == node.side
    if maximizing_player:
        value = -inf
        for ch in node.get_children():
            value = max(value, _alphabeta(ch, depth - 1, alpha, beta, target_side))
            if value >= beta:
                break
            alpha = max(alpha, value)
        return value
    else:
        value = inf
        for ch in node.get_children():
            value = min(value, _alphabeta(ch, depth - 1, alpha, beta, target_side))
            if value <= alpha:
                break
            beta = min(beta, value)
        return value


def get_best_move(board: Board, target_side: Side) -> CompleteMove | None:
    cmoves = get_all_complete_moves_for_side(board, target_side)
    if len(cmoves) == 0:
        return None
    nodes = [Node(board.execute_complete_move(cm), target_side.opposite_side()) for cm in cmoves]
    scores = [_alphabeta(n, 5, -inf, inf, target_side) for n in nodes]
    i, _ = max(enumerate(scores), key=operator.itemgetter(1))
    return cmoves[i]
