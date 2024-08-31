class Move:
    def __init__(self, xfrom, yfrom, xto, yto):
        self.xfrom = xfrom
        self.yfrom = yfrom
        self.xto = xto
        self.yto = yto

    def to_string(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        flipped_yfrom = 7 - self.yfrom
        flipped_yto = 7 - self.yto
        return f"{letters[self.xfrom]}{flipped_yfrom + 1} -> {letters[self.xto]}{flipped_yto + 1}"

    def equals(self, other_move):
        return self.xfrom == other_move.xfrom and self.yfrom == other_move.yfrom and self.xto == other_move.xto and self.yto == other_move.yto
