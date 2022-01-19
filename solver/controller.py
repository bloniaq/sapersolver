import random

from solver.reader import Reader
from solver.model import Board
import logging

log = logging.getLogger('solver.c')

# Start in [0][0] Field
DEBUG_MODE = False


class Controller:

    def __init__(self, board_clear=False):
        self.reader = Reader()
        if self.reader.region is not None:

            self.model = Board(self.reader.left, self.reader.top)
            log.info('app initialized successfully')
            log.debug(f"board top left corner: X:{self.reader.left} Y:{self.reader.top}")
        else:
            log.error('Board not found')
            return

        if not board_clear and not DEBUG_MODE:
            self.reader.read_whole_board(self.model.fields)
        self._start_game()
        log.info("Game started")
        self.solve()

    def solve(self):
        log.info("Starting solving")
        i_know_what_to_do = True
        while i_know_what_to_do:
            log.info("Started solving loop")

            mines_to_mark, fields_to_uncover = self.model.get_potentials()

            self.reader.mark_multiple_field_as_mines(mines_to_mark)
            self.reader.uncover_multiple_fields(fields_to_uncover)

            log.debug("Going to update Board")
            changes = self.reader.update_board(fields_to_uncover)

            if not changes:
                i_know_what_to_do = False
            print(self.model.get_board_string())
        log.warning("I don't know what to do")

    def _start_game(self):
        log.info("Starting game")
        for row in self.model.fields:
            for field in row:
                if field.state != '*':
                    log.warning("Game already started")
                    return

        starting_field = self._pick_start_field()
        self.reader.uncover_field(starting_field)
        log.info(f"Started new game at {starting_field}")
        self.reader.update_board({starting_field})

    def _pick_start_field(self):
        if not DEBUG_MODE:
            row = random.randrange(0, self.model.rows)
            col = random.randrange(0, self.model.columns)
        else:
            row = 0
            col = 0
        random_field = self.model.fields[row][col]
        return random_field
