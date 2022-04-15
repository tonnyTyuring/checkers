from pyrsistent import pvector


class CompleteMove:

    def __init__(self, moves: pvector(['Move'])):
        self.moves = moves
        self.side = self.moves[0].piece.side

    def to_list(self) -> list[tuple[int, int]]:
        moves = self.moves
        moves.reverse()
        res = [moves[0].fr]
        for m in moves:
            res.append(m.to)
        return res

    def __repr__(self):
        moves = self.moves
        res = str(moves[0].fr)
        for m in moves:
            res += " -> " + str(m.to)
        return "{" + res + "}"
