from checkersanalyser.common import get_movement_vector, add
from checkersanalyser.model.piece import Piece

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from checkersanalyser.model.board import Board


class Move:

    def __init__(self, fr: tuple[int, int], to: tuple[int, int], board: 'Board'):
        self.fr = fr
        self.to = to
        self.piece = Piece(fr[0], fr[1], board)
        self.is_eat_move = any([self.piece.side.has_enemy(c, board) for c in self.get_involved_cells()])

    def __str__(self):
        return f"{self.fr} -> {self.to}"

    def __repr__(self):
        return str(self)

    def get_involved_cells(self) -> list[tuple[int, int]]:
        vec = get_movement_vector(self.fr, self.to)
        cell = self.fr
        cells = []
        while cell != self.to:
            cells.append(cell)
            cell = add(cell, vec)
        cells = cells[1:]  # remove first cell (fr cell)
        return cells
