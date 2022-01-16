import random

from solver.reader import Reader
from solver.model import Board
import logging

logg = logging.getLogger('solver.c')

# Start in [0][0] Field
DEBUG_MODE = False


class Controller:

    def __init__(self, board_clear=False):
        self.reader = Reader()
        if self.reader.region is not None:

            self.model = Board(self.reader.left, self.reader.top)
            logg.info('app initialized successfully')
            logg.debug(f"board top left corner: X:{self.reader.left} Y:{self.reader.top}")
        else:
            logg.error('Board not found')
            return

        if not board_clear and not DEBUG_MODE:
            self.reader.read_whole_board(self.model.fields)
        self._start_game()
        logg.info("Game started")
        self.solve()

    def solve(self):
        logg.info("Starting solving")
        i_know_what_to_do = True
        while i_know_what_to_do:
            logg.info("Started solving loop")
            fields_to_uncover = set()

            potential_mines, potential_numbers, neighbours_of_mines \
                = self.model.get_potential()
            self.reader.mark_multiple_field_as_mines(potential_mines)
            fields_to_uncover |= neighbours_of_mines
            logg.debug(f"Neighbours of mines: {neighbours_of_mines}")
            logg.debug(f"Potential numbers: {potential_numbers}")
            fields_to_uncover |= potential_numbers
            fields_to_uncover |= self.model.get_complete_fields_w_cov_neighbours()
            self.reader.uncover_around_multiple_fields(fields_to_uncover)

            logg.info("Going to update Board")
            changes = self.reader.update_board(fields_to_uncover)
            if not changes and not self.model.get_complete_fields_w_cov_neighbours():
                i_know_what_to_do = False
            self.model.print_board()
            # if self.reader.do_we_lost():
            #     i_know_what_to_do = False
            #     logg.error("WE LOST!")
        logg.warning("I don't know what to do")

    def _start_game(self):
        logg.debug("Starting game")
        for row in self.model.fields:
            for field in row:
                if field.state != '*':
                    logg.info("Game already started")
                    return

        starting_field = self._pick_start_field()
        self.reader.uncover_field(starting_field)
        self.reader.update_board({starting_field})
        logg.debug(f"Started new game at {starting_field}")

    def _pick_start_field(self):
        if not DEBUG_MODE:
            row = random.randrange(0, self.model.rows)
            col = random.randrange(0, self.model.columns)
        else:
            row = 0
            col = 0
        random_field = self.model.fields[row][col]
        return random_field
