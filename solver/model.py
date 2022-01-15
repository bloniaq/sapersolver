import logging


logg = logging.getLogger('solver.c.model')


class Board:
    COLUMNS = 30
    ROWS = 16

    def __init__(self, left, top) -> None:
        self.getneighbours = None
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
                field.neighbours.discard(self.fields[y][x])

    def get_complete_fields_w_cov_neighbours(self):
        fields_to_click = set()
        for row in self.fields:
            for field in row:
                if field.iscomplete() and field.getcoveredneighbours():
                    fields_to_click.add(field)
        logg.info(f"complete_fields_w_cov_neighbours: {fields_to_click}")
        return fields_to_click

    def get_neighbours(self, fields: set):
        neighbours = set()
        for field in fields:
            neighbours.union(field.neighbours)
        return neighbours

    def pick_number_neighbours(self, fields: set):
        number_neighbours = set()
        for field in fields:
            for neighbour in field.neighbours:
                if neighbour.isnumber():
                    number_neighbours.add(neighbour)
        return number_neighbours

    def get_potential_mines(self):
        potential_mines = set()
        for row in self.fields:
            for field in row:
                if field.isnumber():
                    potential_mines |= field.point_mines_around()
        logg.info(f"All potential mines for now: {potential_mines}")
        their_complete_number_nbrs = set()
        for mine in potential_mines:
            for n in mine.neighbours:
                if n.isnumber() and n.iscomplete():
                    their_complete_number_nbrs.add(n)
        logg.info(f"Neighbour numbers of mines: {their_complete_number_nbrs}")
        return potential_mines, their_complete_number_nbrs


class Field:

    # STATES:
    # '*' = covered
    # 'e' = empty
    # 'm' = mine
    # '1-8' = value

    def __init__(self, col: int, row: int, x: int, y: int) -> None:
        self.col = col
        self.row = row
        self.x = x
        self.y = y
        self.state = '*'
        self.neighbours = []
        self.region = self._get_region()

    def __repr__(self):
        return f'Field {self.state.upper()} Col:{self.col}, Row:{self.row}'

    def _get_region(self):
        x = self.x - 20
        y = self.y - 20
        width = 40
        length = 40
        return (x, y, width, length)

    def isnumber(self):
        if self.state > '0' and self.state < '9':
            return True
        else:
            return False

    def iscomplete(self):
        if not self.isnumber():
            return False
        mine_neighbours = 0
        for n in self.neighbours:
            if n.state in ('m', 'pm'):
                mine_neighbours += 1
        if mine_neighbours == int(self.state):
            return True
        else:
            return False

    def getcoveredneighbours(self):
        covered_neighbours = set()
        for n in self.neighbours:
            if n.state == '*':
                covered_neighbours.add(n)
        return covered_neighbours

    def getmineneighbours(self):
        mine_neighbours = set()
        for n in self.neighbours:
            if n.state in ('m', 'pm'):
                mine_neighbours.add(n)
        return mine_neighbours

    ###
    # POINTING MINES
    ###

    def point_mines_around(self):
        potential_mines = set()
        # methods = (
        #     self._check_if_state_equals_cov_neighbours
        # )
        # for method in methods:
        #     method()

        potential_mines = self._check_if_state_equals_cov_neighbours(
            potential_mines)
        logg.debug(f"{self} pointed {potential_mines} as mines")
        return potential_mines

    def _check_if_state_equals_cov_neighbours(self, potential_mines):
        covered_neighbours = self.getcoveredneighbours()
        mine_neighbours = self.getmineneighbours()
        if len(covered_neighbours) == int(self.state) - len(mine_neighbours):
            for n in covered_neighbours:
                potential_mines.add(n)
                n.state = 'pm'
        return potential_mines