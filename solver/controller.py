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

        self._update_board()
        self._start_game()
        self.solve()

    def solve(self):
        i_know_what_to_do = True
        while i_know_what_to_do:
            pass
            i_know_what_to_do = False

    def mine_left(self):
        pass

    def get_game_region(self):
        pass

    def _start_game(self):
        for row in self.model.fields:
            for field in row:
                if field != 'c':
                    return

        row = random.randrange(0, self.model.rows)
        col = random.randrange(0, self.model.columns)
        field = self.model.fields[row][col]
        self.reader.discover_field(field)
        logg.debug(f"started game in {row} row, {col} col")
        logg.debug(f"started game in {field.x} x, {field.y} y")

    def _update_board(self):
        self.reader.update_fields(self.model.fields)
        self.model.print_board()
