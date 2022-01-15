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

        self.reader.read_whole_board(self.model.fields)
        logg.info("Board updated")
        self._start_game()
        logg.info("Game started")
        self.solve()

    def solve(self):
        logg.info("Starting solving")
        i_know_what_to_do = True
        while i_know_what_to_do:
            logg.info("Started solving loop")
            potential_mines = self.model.mark_potential_mines()
            self.reader.mark_mines(potential_mines)
            fields_to_uncover = self.model.get_fields_with_cov_neighbours()
            self.reader.uncover(fields_to_uncover)
            i_know_what_to_do = self._update_board(fields_to_uncover)
        logg.warning("I don't know what to do")

    def mine_left(self):
        pass

    def get_game_region(self):
        pass

    def _start_game(self):
        logg.debug("Starting game")
        for row in self.model.fields:
            for field in row:
                if field.state != '*':
                    return

        row = random.randrange(0, self.model.rows)
        col = random.randrange(0, self.model.columns)
        field = self.model.fields[row][col]
        self.reader.discover_field(field)
        logg.debug(f"started game in {row} row, {col} col")
        logg.debug(f"started game in {field.x} x, {field.y} y")

    def _update_board(self, fields_clicked):
        logg.info("Reading Board")
        changes_flag = self.reader.update_board(fields_clicked)
        self.model.print_board()
        return changes_flag
