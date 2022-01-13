from solver.reader import Reader
from solver.model import Board
import logging as lg

lg.basicConfig(level=lg.INFO)


class Solver:

    def __init__(self):
        reader = Reader()
        if reader.region is not None:
            self.model = Board(reader.left, reader.top)
            lg.info('app initialized successfully')
            lg.info(f"board top left corner: X:{reader.left} Y:{reader.top}")
        else:
            lg.error('Board not found')

    def solve(self):
        if self.get_game_region():
            game = True
            win = False
        else:
            return False
        while game:
            # solving
            if self.mine_left() == 0:
                win = True
            game = False
        return win

    def mine_left(self):
        pass

    def get_game_region(self):
        pass
