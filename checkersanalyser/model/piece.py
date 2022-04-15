from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from checkersanalyser.model.board import Board


class Piece:

    def __init__(self, i, j, board: 'Board'):
        from checkersanalyser.model.sides import deduce_side
        self.pos = (i, j)
        self.board = board
        self.value = board[i, j]
        self.side = deduce_side(self.value)
        self.is_queen = self.side.is_queen(self.value)

    def __repr__(self):
        return str((self.side, self.pos))
