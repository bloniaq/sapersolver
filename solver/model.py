import logging


logg = logging.getLogger('solver.c.model')


class Board:
    COLUMNS = 30
    ROWS = 16

    def __init__(self, top, left) -> None:
        self.columns = self.COLUMNS
        self.rows = self.ROWS
        self._init_fields(top, left)

    def _init_fields(self, top, left):
        self.fields = []

        x = first_row_x = left + 23
        y = top + 23

        for row in range(self.rows):
            row_list = []
            for col in range(self.columns):
                field = Field(col, row, x, y)
                row_list.append(field)
                x += 51
            x = first_row_x
            y += 51
            self.fields.append(row_list)

    # def get_field(self):
    #     pass


class Field:

    def __init__(self, col: int, row: int, x: int, y: int) -> None:
        self.col = col
        self.row = row
        self._x = x
        self._y = y
        self.state = 'covered'
        self.neighbours = []
