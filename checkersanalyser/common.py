import enum

from pyrsistent import pvector, freeze

VALID_PLACES = [(x, y) for y in range(8) for x in range(8)]


def is_out_of_bounds(pos: tuple[int, int]) -> bool:
    return pos not in VALID_PLACES


def is_free_for_occupation(pos: tuple[int, int], board: pvector(pvector([int]))) -> bool:
    if is_out_of_bounds(pos):
        return False
    return board[pos[0]][pos[1]] == 0


def norm(el: int) -> int:
    if el == 0:
        return 0
    if el > 0:
        return 1
    return -1


def add(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return t1[0] + t2[0], t1[1] + t2[1]


class Side(enum.Enum):
    WHITES = (1, 2)
    BLACKES = (3, 4)

    @staticmethod
    def deduce_side(v: int):
        return Side.BLACKES if v in Side.BLACKES.value else Side.WHITES

    def to_pawn(self, v: int) -> int:
        if self == Side.WHITES and v in Side.WHITES.value:
            return Side.WHITES.value[0]
        if self == Side.BLACKES and v in Side.BLACKES.value:
            return Side.BLACKES.value[0]
        return v

    def to_queen(self, v: int) -> int:
        if self == Side.WHITES and v in Side.WHITES.value:
            return Side.WHITES.value[1]
        if self == Side.BLACKES and v in Side.BLACKES.value:
            return Side.BLACKES.value[1]
        return v

    def opposite_side(self):
        return Side.WHITES if self == Side.BLACKES else Side.BLACKES

    def last_enemy_line(self):
        if self == Side.BLACKES:
            return 7
        else:
            return 0

    def is_back_move(self, fr: tuple[int, int], to: tuple[int, int]):
        distance_to_enemy_line_before = abs(self.last_enemy_line() - fr[0])
        distance_to_enemy_line_after = abs(self.last_enemy_line() - to[0])
        return distance_to_enemy_line_after > distance_to_enemy_line_before

    def is_enemy(self, v: int) -> bool:
        return v in self.opposite_side().value

    def __str__(self):
        if self == Side.WHITES:
            return "Whites"
        return "Blacks"


def has_enemy(board_value: int, side: Side) -> bool:
    return board_value in side.opposite_side().value


def has_friend(board_value: int, side: Side) -> bool:
    return board_value in side.value


class Piece:

    def __init__(self, i, j, side: Side, is_queen):
        self.pos = (i, j)
        self.side = side
        self.is_queen = is_queen


def _get_pieces_for_side(board, side: Side) -> list[Piece]:
    pieces = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] in side.value:
                is_queen = board[i][j] == side.value[1]
                pieces.append(Piece(i, j, side, is_queen))
    return pieces


class Move:

    def __init__(self, fr: tuple[int, int], to: tuple[int, int], is_eat_move: bool, piece: Piece):
        self.fr = fr
        self.to = to
        self.is_eat_move = is_eat_move
        self.piece = piece
        self.prev_move = None
        self.children = None
        self.board = None
        self.is_final = None
        self.manual_score = None

    def __str__(self):
        return f"{self.fr} -> {self.to}"

    def __repr__(self):
        moves = get_move_chain(self)
        moves.reverse()
        res = str(moves[0].fr)
        for m in moves:
            res += " -> " + str(m.to)
        return "{" + res + "}"

    def to_list(self) -> list[tuple[int, int]]:
        moves = get_move_chain(self)
        moves.reverse()
        res = [moves[0].fr]
        for m in moves:
            res.append(m.to)
        return res

    def get_side(self) -> Side:
        return self.piece.side

    def get_best_score(self, target_side: Side) -> int:
        if self.children is None:
            return self.score(target_side)
        child_scores = [i.get_best_score(target_side) for i in self.children]
        if self.get_side() == target_side:
            return min(child_scores)
        else:
            return max(child_scores)

    def score(self, target_side):
        if self.manual_score is not None:
            return self.manual_score
        s1 = len(_get_pieces_for_side(self.board, target_side))
        s2 = len(_get_pieces_for_side(self.board, target_side.opposite_side()))
        return s1 - s2


def get_move_chain(m: Move, chain=None) -> list[Move]:
    if chain is None:
        chain = []
    chain.append(m)
    if m.prev_move is None:
        return chain
    return get_move_chain(m.prev_move, chain)


def get_movement_vector(pos1: tuple[int, int], pos2: tuple[int, int]) -> tuple[int, int]:
    return norm(pos2[0] - pos1[0]), norm(pos2[1] - pos1[1])


def simplify_cell(v: int):
    if v == 0:
        return v
    return Side.deduce_side(v).to_pawn(v)


def simplified_board(board: pvector(pvector([int]))):
    sboard = []
    for row in board:
        sboard.append([simplify_cell(i) for i in row.tolist()])
    return freeze(sboard)


def flatlist(obj):
    if not isinstance(obj, list):
        return [obj]
    ret = []
    for i in obj:
        [ret.append(j) for j in flatlist(i)]
    return ret


def set_board(board: pvector(pvector([int])), i: tuple[int, int], v: int):
    return board.set(i[0], board[i[0]].set(i[1], v))
