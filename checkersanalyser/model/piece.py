from typing import TYPE_CHECKING
from checkersanalyser.model.sides import deduce_side

class Piece:

    def __init__(self, i, j, board):
        self.pos = (i, j)
        self.board = board
        self.value = board[i, j]
        self.side = deduce_side(self.value)
        self.is_queen = self.side.is_queen(self.value)

    def __repr__(self):
        return str((self.side, self.pos))
