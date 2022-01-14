import logging


logg = logging.getLogger('solver.c.model')


class Board:
    COLUMNS = 30
    ROWS = 16

    def __init__(self, left, top) -> None:
        self.columns = self.COLUMNS
        self.rows = self.ROWS
        self._init_fields(left, top)
        self._bind_neighbours()

    def _init_fields(self, left, top):
        self.fields = []
        logg.debug(f"init fields parameters vals: left: {left}, top: {top}")

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

    def print_board(self):
        board = ''
        for row in self.fields:
            for field in row:
                board += field.state + ' '
            board += '\n'

        print(board)

    def _bind_neighbours(self):
        for row in self.fields:
            for field in row:
                x = field.col
                y = field.row
                neighbours = []
                for r in range(y - 1 if y > 0 else y, y + 2 if y < len(self.fields) - 1 else y + 1):
                    for c in range(x - 1 if x > 0 else x, x + 2 if x < len(self.fields[0]) - 1 else x + 1):
                        neighbours.append(self.fields[r][c])
                field.neighbours = set(neighbours)
                field.neighbours.remove(self.fields[y][x])


class Field:

    # STATES:
    # 'c' = covered
    # 'e' = empty
    # 'm' = mine
    # '1-8' = value

    def __init__(self, col: int, row: int, x: int, y: int) -> None:
        self.col = col
        self.row = row
        self.x = x
        self.y = y
        self.state = 'c'
        self.neighbours = []
        self.region = self._get_region()

    def __repr__(self):
        return f'Field Col:{self.col}, Row:{self.row}'

    def _get_region(self):
        x = self.x - 20
        y = self.y - 20
        width = 40
        length = 40
        return (x, y, width, length)
