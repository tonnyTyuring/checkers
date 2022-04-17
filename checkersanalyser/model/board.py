from __future__ import annotations

from pyrsistent import pvector, freeze

from checkersanalyser.common import simplified_board, VALID_PLACES
from checkersanalyser.model.completemove import CompleteMove
from checkersanalyser.model.move import Move
from checkersanalyser.model.piece import Piece
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from checkersanalyser.model.sides import Side


class Board:

    def __init__(self, b: pvector(pvector([int])) | list[list[int]]):
        if isinstance(b, list):
            b = freeze(b)
        self.pboard = b

    def set(self, pos: tuple[int, int], v: int) -> Board:
        return Board(self.pboard.set(pos[0], self.pboard[pos[0]].set(pos[1], v)))

    def __getitem__(self, pos: tuple[int, int]) -> int:
        return self.pboard[pos[0]][pos[1]]

    def __eq__(self, other: object):
        if not isinstance(other, Board):
            return NotImplemented
        return self.pboard == other.pboard

    def execute_move(self, m: Move) -> Board:
        side = m.piece.side
        v = self[m.fr]
        if m.to[0] == side.upgrade_line():
            v = side.queen_value
        new_board = self.set(m.to, v)
        new_board = new_board.set(m.fr, 0)
        if (ec := m.get_eaten_cell()) is not None:
            new_board = new_board.set(ec, 0)
        return new_board

    def execute_complete_move(self, m: CompleteMove) -> Board:
        new_board = self.execute_move(m.moves[0])
        for m in m.moves[1:]:
            new_board = new_board.execute_move(m)
        return new_board

    def get_pieces(self) -> list[Piece]:
        cells = []
        for i in range(len(self.pboard)):
            for j in range(len(self.pboard[i])):
                if self[i, j] != 0:
                    cells.append(Piece(i, j, self))
        return cells

    def get_pieces_for_side(self, side: 'Side') -> list[Piece]:
        return [p for p in self.get_pieces() if p.side == side]

    def simplified(self) -> Board:
        return Board(simplified_board(self.pboard))

    def __repr__(self):
        return str(self.pboard.tolist())

    def tolist(self):
        return [row.tolist() for row in self.pboard]

    def print(self):
        print('\n\n')
        for row in self.pboard:
            print(row.tolist())

    def __hash__(self):
        return hash(self.pboard)
