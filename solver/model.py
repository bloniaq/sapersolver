import logging
from solver.exceptions import *

log = logging.getLogger('solver.c.model')

log.setLevel(logging.INFO)


class Board:
    ROWS = 16
    COLUMNS = 30

    def __init__(self, left, top, rows=ROWS, columns=COLUMNS, pref_state=None) -> None:
        self.columns = columns
        self.rows = rows
        self._init_fields(left, top, pref_state)
        self._bind_neighbours()

    def _init_fields(self, left, top, preferred_state=None):
        self.fields = []
        self.fieldset = set()
        log.debug(f"init fields parameters values: left: {left}, top: {top}")

        # Adjustment to center of minesweeper field button
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
                self.fieldset.add(field)
                # 51 is width of button in pixels
                x += 51
            x = first_row_x
            y += 51
            self.fields.append(row_list)

    def get_board_string(self):
        """
        Create string to show current board state in command line
        :return:
            board
                a prepared string
        """
        board = '\n'
        for row in self.fields:
            for field in row:
                board += field.state + '\t'
            board += '\n'

        return board

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
                if field.is_complete() and field.get_nbours('*'):
                    field.state = 'pn'
                    fields_to_click.add(field)
        log.info(f"complete_fields_w_cov_neighbours: {fields_to_click}")
        return fields_to_click

    def get_potentials(self):
        """
        Marks fields recognized as potential mines and safe for uncover
        (potential numbers).
        :return:
        """
        number_fields = {field for field in self.fieldset if field.is_number()}

        log.info("Marking obvious mines ")
        for field in number_fields:
            field.mark_obvious_mines()

        log.info("Iterating over numeric neighbours of numeric fields")
        for field in number_fields:
            field.iterate_over_num_neighbours()

        # pot_mines = {field for field in self.fieldset if field.state == 'pm'}

        pot_completes = {field for field in self.fieldset if field.is_complete()}
        for field in pot_completes:
            field.mark_potentials(field.get_nbours('*'), 'pn')

        log.info("Marking obvious mines ")
        for field in number_fields:
            field.mark_obvious_mines()

        pot_mines = {field for field in self.fieldset if field.state == 'pm'}
        pot_numbers = {field for field in self.fieldset if field.state == 'pn'}

        log.debug(self.get_board_string())

        return pot_mines, pot_numbers


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
        return f'Field = {self.state.upper()} | r:{self.row}, c:{self.col}'

    def _get_region(self):
        x = self.x - 20
        y = self.y - 20
        width = 40
        length = 40
        return x, y, width, length

    ###
    # PRINTING METHODS
    ###

    def current_neighbourhood_string(self):
        n_nw = self._pick_rel_neighbour(-1, -1)
        n_n = self._pick_rel_neighbour(-1, 0)
        n_ne = self._pick_rel_neighbour(-1, 1)
        n_w = self._pick_rel_neighbour(0, -1)
        n_e = self._pick_rel_neighbour(0, 1)
        n_sw = self._pick_rel_neighbour(1, -1)
        n_s = self._pick_rel_neighbour(1, 0)
        n_se = self._pick_rel_neighbour(1, 1)
        board = f"{n_nw.state}\t {n_n.state}\t{n_ne.state}\n" \
                f"{n_w.state}\t#{self.state}#\t{n_e.state}\n" \
                f"{n_sw.state}\t {n_s.state}\t{n_se.state}"
        return board

    def _pick_rel_neighbour(self, row_offset, col_offset):
        for n in self.neighbours:
            if n.row == self.row + row_offset and \
                    n.col == self.col + col_offset:
                return n
        return Field(self.row + row_offset, self.col + col_offset,
                     100, 100, 'X')

    ###
    # READING FIELD METHODS
    ###

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

    def m_left(self):
        mines_left = int(self.state) - len(self.get_nbours('m', 'pm'))
        if mines_left < 0:
            raise NegativeMinesLeftCountError(self,
                                              self.current_neighbourhood_string())
        return mines_left

    def is_number(self):
        if '0' < self.state < '9':
            return True
        else:
            return False

    def is_complete(self):
        if not self.is_number():
            return False
        if self.state == 'pn':
            return False
        mine_neighbours = 0
        for n in self.neighbours:
            if n.state in ('m', 'pm'):
                mine_neighbours += 1
        if mine_neighbours == int(self.state):
            return True
        else:
            return False

    def intersection_with(self, other_field: 'Field') -> set:
        self_covered = self.get_nbours('*')
        other_field_covered = other_field.get_nbours('*')
        intersection = self_covered.intersection(other_field_covered)
        log.debug(f"    Intersection: {len(intersection)} {intersection}")
        return intersection

    def difference_with(self, other_field: 'Field') -> set:
        self_covered = self.get_nbours('*')
        other_field_covered = other_field.get_nbours('*')
        difference = self_covered.difference(other_field_covered)
        log.debug(f"    Difference: {difference} [[[{self} - {other_field}]]]")
        return difference

    def _analyze_pair_with(self, n):
        """
        Returns properties of a self and n pair
        :param n: Field
        :return:
            intersection : set
                a common set of (*) fields
            self_diff_n : set
                a set of neighbours of self, which aren't neighbour of n
            n_diff_self : set
                a set of neighbours of n, which aren't neighbour of self
            min_mines_num : int
                a minimal number of mines in intersection
            max_mines_num : int
                a maximum number of mines in intersection
            exact : int
                if minimum and maximum number of mines in intersection are
                equal - it's exact number of mines in intersection; otherwise
                it's None
        """
        log.debug(f"SELF NEIGHBOURHOOD:\n"
                  f"{self.current_neighbourhood_string()}")
        log.debug(f"N NEIGHBOURHOOD:\n"
                  f"{n.current_neighbourhood_string()}")
        intersection = self.intersection_with(n)
        self_diff_n = self.difference_with(n)
        n_diff_self = n.difference_with(self)

        min_mines_num = max(
            self.m_left() - len(self_diff_n),
            n.m_left() - len(n_diff_self),
            0
        )
        max_mines_num = min(
            len(intersection),
            n.m_left(),
            self.m_left()
        )
        exact = None
        if min_mines_num == max_mines_num:
            exact = min_mines_num

        return intersection, self_diff_n, n_diff_self, \
            min_mines_num, max_mines_num, exact

    ###
    # POINTING MINES
    ###

    def mark_obvious_mines(self):
        if self.m_left() == len(self.get_nbours('*')):
            self.mark_potentials(self.get_nbours('*'), 'pm', "Obvious")

    def iterate_over_num_neighbours(self):
        fields_to_cooper = set()
        for cov_neighbour in self.get_nbours('*'):
            fields_to_cooper |= {field for field in cov_neighbour.get_nbours('n')}

        for n in self.get_nbours('n') | fields_to_cooper:

            log.debug(f"Iteration over {self}: neighbour: {n}")

            if n.is_complete():
                self.mark_potentials(n.get_nbours('*'), 'pn',
                                     f"Neighbour {n} complete")

            intersection, self_diff_n, n_diff_self, minimum, maximum, exact = \
                self._analyze_pair_with(n)

            if not intersection:
                continue

            if n.get_nbours('*') == intersection:

                log.debug(f"All {n} ('*') neighbours are in intersec subset")
                log.debug(f"In intersection there are exactly "
                          f"{exact} mines")
                if self.m_left() == exact:
                    self.mark_potentials(self_diff_n, 'pn', '1')
                    if self.m_left() == len(intersection):
                        self.mark_potentials(intersection, 'pm', '2')
                if n.m_left() == exact:
                    self.mark_potentials(n_diff_self, 'pn', '3')
                    if n.m_left() == len(intersection):
                        self.mark_potentials(intersection, 'pm', '4')
                if self.m_left() - n.m_left() == 0:
                    self.mark_potentials(self_diff_n, 'pn',
                                         '2nd if: self.m_left() - '
                                         'n.m_left() == 0')
                if self.m_left() - n.m_left() > 0 and \
                        self.m_left() - n.m_left() == len(self_diff_n):
                    self.mark_potentials(self_diff_n, 'pm',
                                         '3rd if: self.m_left() - n.m_left() '
                                         '> 0 and self.m_left() == '
                                         'len(self_diff_n)')
            elif (len(n.get_nbours('*')) > len(intersection)) and \
                    exact is not None and \
                    len(intersection) > 0:
                log.debug(f"Neighbour {n} has more ('*') neighbours than len(intersection)")
                log.debug(f"    There are min {minimum} and max "
                          f"{maximum} mines in intersection")

                if self.m_left() - exact == 0:
                    self.mark_potentials(self_diff_n, 'pn',
                                         "1st minimum = maximum, "
                                         "self.m_left() - exact")
                if self.m_left() - exact == len(self_diff_n):
                    self.mark_potentials(self_diff_n, 'pm',
                                         "2nd minimum = maximum, "
                                         "self.m_left() - exact == "
                                         "len(self_diff_n)")
                if n.m_left() - exact == 0:
                    self.mark_potentials(n_diff_self, 'pn',
                                         "3rd minimum = maximum, "
                                         "n.m_left() - exact == 0")
                if n.m_left() - exact == len(n_diff_self):
                    self.mark_potentials(n_diff_self, 'pm',
                                         "4th minimum = maximum, "
                                         "n.m_left() - exact == "
                                         "len(n_diff_self)")

    def mark_potentials(self, fieldset, mark, info=None):
        for field in fieldset:
            if field.state in ('*', 'pn'):
                log.info(f"Marking {field} as {mark.upper()} by\n"
                         f"\t\t{self}.\n"
                         f"\t\t{info}")
                field.state = mark
