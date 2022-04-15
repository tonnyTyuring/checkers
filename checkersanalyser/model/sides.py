from __future__ import annotations

from typing import Optional

from checkersanalyser.model.board import Board


class Side:
    _UPGRADE_LINE = {1: 7, -1: 0}  # Maps direction to line on which piece upgrades to queen

    def __init__(self, pv, qv, td, name):
        self.opposite = None
        self.queen_value = qv
        self.pawn_value = pv
        self.target_direction = td  # 1 - forward, -1 - backward
        self.side_name = name

    def __contains__(self, key: int) -> bool:
        return key in (self.pawn_value, self.queen_value)

    def is_pawn(self, v: int) -> bool:
        return v == self.pawn_value

    def is_queen(self, v: int) -> bool:
        return v == self.queen_value

    def to_pawn(self, v: int) -> int:
        if v == self.queen_value:
            return self.pawn_value
        return v

    def to_queen(self, v: int) -> int:
        if v == self.pawn_value:
            return self.queen_value
        return v

    def opposite_side(self) -> Side:
        return self.opposite

    def has_enemy(self, pos: tuple[int, int], board: Board) -> bool:
        return board[pos] in self.opposite

    def is_enemy(self, v: int) -> bool:
        return v in self.opposite

    def upgrade_line(self):
        return self._UPGRADE_LINE[self.target_direction]

    def __str__(self):
        return self.side_name

    def __repr__(self):
        return self.side_name


WHITES = Side(1, 2, -1, "Whites")
BLACKES = Side(3, 4, 1, "Blackes")
WHITES.opposite = BLACKES
BLACKES.opposite = WHITES


def deduce_side(v: int) -> Optional[Side]:
    if v in WHITES:
        return WHITES
    if v in BLACKES:
        return BLACKES
    return None
