from __future__ import annotations

from checkersanalyser.model.board import Board
from checkersanalyser.model.sides import Side
from checkersanalyser.service.moveservice import get_all_complete_moves_for_side


class Node:

    def __init__(self, board: Board, side: Side):
        self.board = board
        self.side = side
        self.children = None

    def get_children(self) -> list[Node]:
        return self._children()

    def is_terminal(self) -> bool:
        return len(self._children()) == 0

    def _children(self):
        if self.children is not None:
            return self.children
        cmoves = get_all_complete_moves_for_side(self.board, self.side)
        self.children = [Node(self.board.execute_complete_move(c), self.side.opposite_side()) for c in cmoves]
        return self.children
