import logging


logg = logging.getLogger('solver.c.model')


class Board:
    ROWS = 16
    COLUMNS = 30

    def __init__(self, left, top, rows=ROWS, columns=COLUMNS, pref_state=None) -> None:
        self.getneighbours = None
        self.columns = columns
        self.rows = rows
        self._init_fields(left, top, pref_state)
        self._bind_neighbours()

    def _init_fields(self, left, top, preferred_state=None):
        self.fields = []
        logg.debug(f"init fields parameters vals: left: {left}, top: {top}")

        # adjustment to center of minesweeper field button
        x = first_row_x = left + 23
        y = top + 23

        for row in range(self.rows):
            row_list = []
            for col in range(self.columns):
                if preferred_state is None:
                    field = Field(row, col, x, y)
                else:
                    field = Field(row, col, x, y, preferred_state)
                row_list.append(field)
                # 51 is width of button in pixels
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
                if field.iscomplete() and field.get_nbours('*'):
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

    def get_potentials(self):
        potential_mines = set()
        potential_numbers = set()
        for row in self.fields:
            for field in row:
                if field.isnumber():
                    pointed_mines, pointed_numbers = field.figure_out()
                    potential_mines |= pointed_mines
                    potential_numbers |= pointed_numbers
        logg.info(f"All potential mines for now: {potential_mines}")
        their_complete_number_nbrs = set()
        for mine in potential_mines:
            for n in mine.neighbours:
                if n.isnumber() and n.iscomplete():
                    their_complete_number_nbrs.add(n)
        logg.info(f"Neighbour numbers of mines: {their_complete_number_nbrs}")
        return potential_mines, potential_numbers, their_complete_number_nbrs


class Field:

    # STATES:
    # '*' = covered
    # '_' = empty
    # 'm' = mine
    # '1-8' = value

    def __init__(self, row: int, col: int, x: int, y: int, state='*') -> None:
        self.col = col
        self.row = row
        self.x = x
        self.y = y
        self.state = state
        self.neighbours = set()
        self.region = self._get_region()

    def __repr__(self):
        return f'Field S:{self.state.upper()} C:{self.col}, R:{self.row}'

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

    def get_nbours(self, *args):
        neighbours = set()
        args = list(args)
        if not args:
            args = ['*', '_', 'm', 'n']
        if 'n' in args:
            args.remove('n')
            for n in range(ord('1'), ord('8')):
                args.append(chr(n))
        if 'm' in args:
            args.append('pm')
        for arg in args:
            neighbours |= {nbour for nbour in self.neighbours if nbour.state == arg}
        return neighbours

    def _intersection(self, other_field: 'Field') -> set:
        self_covered = self.get_nbours('*')
        other_field_covered = other_field.get_nbours('*')
        logging.debug(f'self_covered: {self_covered}')
        logging.debug(f'other_field_covered: {other_field_covered}')
        intersection = self_covered.intersection(other_field_covered)
        return intersection

    def _difference(self, other_field: 'Field') -> set:
        self_covered =  self.get_nbours('*')
        other_field_covered = other_field.get_nbours('*')
        difference = self_covered.difference(other_field_covered)
        return difference

    ###
    # POINTING MINES
    ###

    def figure_out(self):
        """
        Runs one by one submethods for pointing mines and numbers around field

        Submethods has to changes fields status to:
        'pm' - potential mines
        'pn' - potential number

        :return: potential_mines, potential_numbers : set, set
        """
        potential_mines = set()
        potential_numbers = set()
        methods = (
            self._check_if_state_equals_cov_neighbours,
            self._check_whats_with_neighbours
        )
        for method in methods:
            pot_mines, pot_numbers = method(potential_mines, potential_numbers)
            potential_mines |= pot_mines
            potential_numbers |= pot_numbers

        logg.info(f"{self} pointed {potential_mines} as mines")
        logg.info(f"{self} pointed {potential_numbers} as numbers")

        return potential_mines, potential_numbers

    def _check_if_state_equals_cov_neighbours(self, pot_mines, pot_numbers):
        covered_neighbours = self.get_nbours('*')
        mine_neighbours = self.get_nbours('m')
        if len(covered_neighbours) == int(self.state) - len(mine_neighbours):
            for n in covered_neighbours:
                pot_mines.add(n)
                n.state = 'pm'
        return pot_mines, pot_numbers

    def _check_whats_with_neighbours(self, pot_mines, pot_numbers):
        logg.debug(f"Checking whats with {self} neighbours")
        for nn in self.get_nbours('n'):
            intersection = self.get_nbours('*').intersection(
                nn.get_nbours('*'))
            difference = self.get_nbours('*').difference(
                nn.get_nbours('*'))
            if not intersection:
                continue
            logg.debug(f"Intersection with {nn}: {intersection}")
            logg.debug(f"Difference with {nn}: {difference}")
            mines_in_intersection = int(nn.state) - \
                                    len(nn.get_nbours('m'))
            other_mines_count = int(self.state) - mines_in_intersection - \
                                len(self.get_nbours('m'))
            if mines_in_intersection < 0:
                logg.error(f"{self} x {nn}: mines in intersection "
                
                           f"{mines_in_intersection}")

            logg.debug(f"other mines: {other_mines_count}")
            if other_mines_count == 0 and intersection == nn.get_nbours('*'):
                pot_numbers |= self.get_nbours('*').difference(
                    nn.get_nbours('*'))
                logg.debug(f"Potential numbers: {pot_numbers}")
            elif other_mines_count == len(difference) and intersection == nn.get_nbours('*'):
                pot_mines |= difference
                for field in difference:
                    field.state = 'pm'
                logg.debug(f"Potenial mines: {pot_mines}")
            elif (len(difference) + min(len(intersection), int(nn.state))) == int(self.state) - len(self.get_nbours('m')):
                pot_mines |= difference
                nn_difference = nn.get_nbours('*').difference(intersection)
                pot_numbers |= nn_difference
                for field in difference:
                    field.state = 'pm'
                logg.debug(f"Potenial mines (2nd): {pot_mines}, {len(difference)}+")
                for field in nn_difference:
                    field.state = 'pn'
                logg.debug(f"Potenial numbers (3nd): {pot_numbers}, {len(nn_difference)}")
        return pot_mines, pot_numbers
