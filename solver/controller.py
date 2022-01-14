import random

from solver.reader import Reader
from solver.model import Board
import logging


logg = logging.getLogger('solver.c')


class Controller:

    def __init__(self):
        self.reader = Reader()
        if self.reader.region is not None:

            self.model = Board(self.reader.left, self.reader.top)
            logg.info('app initialized successfully')
            logg.debug(f"board top left corner: X:{self.reader.left} Y:{self.reader.top}")
        else:
            logg.error('Board not found')
            return

        self._start_game()
        self._update_board()

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

    def _start_game(self):
        row = random.randrange(0, self.model.rows)
        col = random.randrange(0, self.model.columns)
        field = self.model.fields[row][col]
        self.reader.discover_field(field)
        logg.debug(f"started game in {row} row, {col} col")
        logg.debug(f"started game in {field.x} x, {field.y} y")

    def _update_board(self):
        self.reader.update_fields(self.model.fields)
