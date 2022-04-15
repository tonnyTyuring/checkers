from __future__ import annotations

from pyrsistent import pvector

from checkersanalyser.common import simplified_board, Side
from checkersanalyser.model.completemove import CompleteMove
from checkersanalyser.model.move import Move
from checkersanalyser.model.piece import Piece
from checkersanalyser.service.pieceservice import VALID_PLACES


class Board:

    def __init__(self, b: pvector(pvector([int]))):
        self.pboard = b

    def set(self, pos: tuple[int, int], v: int) -> Board:
        return Board(self.pboard.set(pos[0], self.pboard[pos[0]].set(pos[1], v)))

    def __getitem__(self, pos: tuple[int, int]) -> int:
        if pos not in VALID_PLACES:
            return -1
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
        for c in m.get_involved_cells():
            if side.is_enemy(new_board[c]):
                new_board = new_board.set(c, 0)
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

    def print(self):
        print('\n\n')
        for row in self.pboard:
            print(row.tolist())
