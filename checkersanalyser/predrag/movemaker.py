from __future__ import annotations

import operator
import random

from math import inf
from checkersanalyser.model.board import Board
from checkersanalyser.model.completemove import CompleteMove
from checkersanalyser.model.node import Node
from checkersanalyser.model.sides import Side
from checkersanalyser.moveresolver.completemoveresolver import get_all_valid_moves_for_side
from checkersanalyser.predrag.scorecounter import score
from checkersanalyser.predrag.worker import STOP
from pathos.multiprocessing import ProcessPool, cpu_count

from checkersanalyser.common import timeit


class MoveMaker:

    def __init__(self, target_side: Side, depth: int, parallelized: bool, randomized: bool):
        self.target_side = target_side
        self.depth = depth
        self.parallelized = parallelized
        self.randomized = randomized

    def _under_threat(self, board: Board) -> bool:
        enemy_moves = get_all_valid_moves_for_side(board, self.target_side.opposite_side())
        return any([i.moves[0].is_eat_move for i in enemy_moves])

    def _alphabeta(self, node: Node, depth: int, alpha: int | inf, beta: int | inf) -> float:
        if STOP[0]:
            return inf
        if node.is_terminal():
            return score(node.board.pboard, self.target_side)
        if depth <= 0 and not self._under_threat(node.board):
            return score(node.board.pboard, self.target_side)
        maximizing_player = self.target_side == node.side
        if maximizing_player:
            value = -inf
            for ch in node.get_children():
                value = max(value, self._alphabeta(ch, depth - 1, alpha, beta))
                if value >= beta:
                    break
                alpha = max(alpha, value)
            return value
        else:
            value = inf
            for ch in node.get_children():
                value = min(value, self._alphabeta(ch, depth - 1, alpha, beta))
                if value <= alpha:
                    break
                beta = min(beta, value)
            return value

    def get_best_move(self, board: Board) -> CompleteMove | None:
        cmoves = get_all_valid_moves_for_side(board, self.target_side)
        if len(cmoves) == 0:
            return None
        nodes = [Node(board.execute_complete_move(cm), self.target_side.opposite_side()) for cm in cmoves]
        max_indexes = self._max_score_indexes(nodes)
        best_moves = operator.itemgetter(*max_indexes)(cmoves) if len(max_indexes) > 1 else [cmoves[max_indexes[0]]]
        longest_move_num = max([len(cm.moves) for cm in best_moves])
        best_longest_moves = [cm for cm in best_moves if len(cm.moves) == longest_move_num]
        if self.randomized:
            return random.choice(best_longest_moves)
        else:
            return best_longest_moves[0]

    def _max_score_indexes(self, nodes):
        if self.parallelized:
            """
            ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
            ⠄⠄⠄⠄⠄⣀⠠⣴⣶⣾⣿⣶⣄⡀⣀⣠⣤⣄⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
            ⠄⠄⠄⢰⣿⣿⣿⣿⣿⣯⣭⡛⠿⡇⢚⣽⣿⣟⡻⡆⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
            ⠄⣠⣾⣸⣿⣿⣒⡹⠟⢛⣉⠐⢖⢃⣵⡖⠂⠒⠲⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
            ⣰⣿⣿⣿⣿⣿⡇⡐⣫⣿⣿⣷⡿⣠⡻⢿⣾⣯⣶⡤⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
            ⣿⣿⣿⣿⣥⡿⢃⠛⣲⢉⣩⣭⠬⠭⠭⠥⠬⠭⠽⠜⠆⣦⠄⠄⠄⠄⠄⠄⠄⠄
            ⣿⣿⣿⣿⣿⡇⣿⠄⡇⣴⣰⢰⡇⣿⠘⣧⢹⡆⠇⠃⢸⣸⡇⠄⠄⠄⡜⣷⡰⡄
            ⣿⣿⣿⣿⣿⡇⢻⣀⣇⡉⡍⡄⣶⢰⡆⢰⢰⡆⣄⡄⡴⣿⠇⢰⣦⠄⣿⣸⣧⡿
            ⢿⣿⣿⣿⣿⣿⣶⣍⣻⣿⣟⣃⡛⣘⢃⢻⢘⢃⣌⣼⣿⠃⠄⡀⣿⣷⣿⣿⠟⠁
            ⣔⡺⠯⣝⣛⡻⠿⠿⣿⣿⡻⣔⢷⣯⣿⣘⣿⢘⡌⣿⠏⢰⣾⣿⣿⡿⠉⠁⠄⠄
            ⣿⣿⣿⣶⣭⣭⣙⣛⣒⣒⣒⣛⠿⢿⣿⣿⣿⠿⠋⠁⠄⠘⣿⣿⣿⡇⠄⠄⠄⠄
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢸⣿⣿⣿⢰⣿⣆⠄⠄⠄⢿⣿⣿⣷⠄⠄⠄⠄
            ⣿⣿⣿⣿⣍⢻⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⢸⣿⣿⣷⣄⠄⢸⣿⣿⣿⡀⠄⠄⠄
            ⡜⢿⣿⣿⣿⣷⣜⢿⣿⣿⣿⢱⣿⣿⣿⡧⠻⣿⣿⣿⣿⡟⣼⣿⣿⣿⡇⠄⠄⠄
            ⣿⣎⢿⣿⣿⣿⣿⣷⣌⢻⡿⣿⣿⣿⡿⢡⣷⡈⠻⣿⡟⣴⣿⣿⣿⣿⠄⠄⠄⠄
            I love GIL"""
            with ProcessPool(nodes=cpu_count()) as p:
                scores = p.map(lambda x: self._alphabeta(x, self.depth, -inf, inf), nodes)
        else:
            scores = [self._alphabeta(n, self.depth, -inf, inf) for n in nodes]
        max_score = max(scores)
        max_indexes = [i for i, v in enumerate(scores) if v == max_score]
        return max_indexes


@timeit("Move deduction")
def get_best_move(board: Board, target_side: Side, randomized=False) -> CompleteMove | None:
    depth = 5
    mm = MoveMaker(target_side, depth=depth, parallelized=True, randomized=randomized)
    return mm.get_best_move(board)
