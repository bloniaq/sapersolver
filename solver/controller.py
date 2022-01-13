from solver.reader import Reader
from solver.model import Board
import logging


logg = logging.getLogger('solver.c')


class Controller:

    def __init__(self):
        reader = Reader()
        if reader.region is not None:

            self.model = Board(reader.left, reader.top)
            logg.info('app initialized successfully')
            logg.debug(f"board top left corner: X:{reader.left} Y:{reader.top}")
        else:
            logg.error('Board not found')

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
