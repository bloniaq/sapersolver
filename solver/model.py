import logging


logg = logging.getLogger('solver.c.model')


class Board:
    COLUMNS = 30
    ROWS = 16

    def __init__(self, top, left) -> None:
        self.columns = self.COLUMNS
        self.rows = self.ROWS


class Field:

    def __init__(self, col: int, row: int, x: int, y: int) -> None:
        self.col = col
        self.row = row
        self.x = x
        self.y = y
        self.state = 'covered'
