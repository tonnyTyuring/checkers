import enum
from copy import deepcopy
from typing import Optional

from pyrsistent import v, pvector, freeze

from checkersanalyser.common import simplified_board, Side, Piece, get_movement_vector, has_friend, is_out_of_bounds, Move, has_enemy, \
    add, is_free_for_occupation


def logged(func):
    def logged_func(*args, **kwargs):
        self = args[0]
        print(f"INPUT:from: {self._meta['from']}")
        print(f"INPUT:to: {self._meta['to']}")
        print(f"INPUT:args: {args[1:]} {kwargs}")
        res = func(*args, **kwargs)
        print(f"OUTPUT: {res}")
        return res

    return logged_func


def get_potential_moves(p: Piece, board: pvector(pvector([int]))) -> list[tuple[int, int]]:
    i = p.pos[0]
    j = p.pos[1]
    directions = [(i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1)]
    if not p.is_queen:
        return directions
    queen_moves = []
    for direction in directions:
        movement_vector = get_movement_vector(p.pos, direction)
        move = add(p.pos, movement_vector)
        while not is_out_of_bounds(move) and board[move[0]][move[1]] == 0:
            queen_moves.append(move)
            move = add(move, movement_vector)
        queen_moves.append(move)
    return queen_moves


class MoveAnalyser:
    def __init__(self, fromm: list[list[int]], to: list[list[int]]):
        self._meta = {"from": fromm, "to": to}
        self.fromm = freeze(fromm)
        self.to = simplified_board(freeze(to))

    def _get_pieces_for_side(self, side: Side) -> list[Piece]:
        pieces = []
        for i in range(len(self.fromm)):
            for j in range(len(self.fromm)):
                if self.fromm[i][j] in side.value:
                    is_queen = self.fromm[i][j] == side.value[1]
                    pieces.append(Piece(i, j, side, is_queen))
        return pieces

    def _make_move(self, board: pvector(pvector([int])), valid_player_moves: list[Move], move: Move):
        p = board[move.fr[0]][move.fr[1]]
        board = board.set(move.fr[0], board[move.fr[0]].set(move.fr[1], 0))  # set initial place to 0
        board = board.set(move.to[0], board[move.to[0]].set(move.to[1], p))  # set target place
        if move.is_eat_move:
            move_vector = get_movement_vector(move.fr, move.to)
            eaten_piece = tuple(b - a for a, b in zip(move_vector, move.to))
            board = board.set(eaten_piece[0], board[eaten_piece[0]].set(eaten_piece[1], 0))  # set eaten place to 0

        if simplified_board(board) == self.to:
            # if board == self.to:
            valid_player_moves.append(move)
        if not move.is_eat_move:
            return
        new_piece = deepcopy(move.piece)
        if move.to[0] == move.piece.side.last_enemy_line():
            new_piece.is_queen = True
        new_piece.pos = move.to
        for next_move in filter(lambda m: m.is_eat_move, self._get_moves_for_piece(board, new_piece)):
            next_move.prev_move = move
            self._make_move(board, valid_player_moves, next_move)

    @staticmethod
    def _create_move(board: pvector(pvector([int])), fr: tuple[int, int], to: tuple[int, int], p: Piece) -> Optional[
        Move]:
        is_eat_move = False
        if is_out_of_bounds(to) or has_friend(board[to[0]][to[1]], p.side):
            return None
        cell = board[to[0]][to[1]]
        if not p.is_queen and p.side.is_back_move(fr, to) and not has_enemy(cell, p.side):
            return None
        if has_enemy(cell, p.side):
            move_vector = get_movement_vector(fr, to)
            to = add(move_vector, to)
            is_eat_move = True
        if not is_free_for_occupation(to, board):
            return None
        return Move(fr, to, is_eat_move, p)

    def _get_moves_for_piece(self, board: pvector(pvector([int])), p: Piece) -> list[Move]:
        return [m for pm in get_potential_moves(p, board) if (m := self._create_move(board, p.pos, pm, p)) is not None]

    @logged
    def calculate_move_for_side(self, side: Side) -> list[Move]:
        moves: list[Move] = [m for p in self._get_pieces_for_side(side) for m in
                             self._get_moves_for_piece(self.fromm, p)]
        valid_player_moves: list[Move] = []
        for move in filter(lambda m: m.is_eat_move, moves):
            self._make_move(self.fromm, valid_player_moves, move)
        if len(valid_player_moves) != 0:
            return valid_player_moves
        for move in filter(lambda m: not m.is_eat_move, moves):
            self._make_move(self.fromm, valid_player_moves, move)
        return valid_player_moves
