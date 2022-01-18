from solver.model import *
import pytest
import logging


log = logging.getLogger('solver.tests.test_model')


@pytest.fixture
def custom_board():
    def create_testboard(rows, cols, states: tuple) -> Board:
        if cols * rows != len(states):
            log.error("Passed wrong number of arguments")
            return Board(0, 0, 5, 5, '!')
        board = Board(0, 0, rows, cols)
        state = (state for state in states)
        for row in board.fields:
            for field in row:
                field.state = next(state)
        return board

    return create_testboard


class TestModel:

    @pytest.fixture
    def basic_model(self) -> Board:
        return Board(200, 400)

    def test_model_init(self, basic_model):
        assert basic_model is not None
        assert isinstance(basic_model, Board)

    def test_dimensions(self, basic_model):
        assert basic_model.columns == basic_model.COLUMNS
        assert basic_model.rows == basic_model.ROWS

    def test_preffered_state(self):
        board_R = Board(200, 400, pref_state='R')
        assert board_R.fields[0][0].state == 'R'
        board_None = Board(200, 400, pref_state=None)
        assert board_None.fields[0][0].state == '*'

    def test_get_field(self, basic_model):
        row = 3
        col = 5
        field = basic_model.fields[row][col]
        assert field.row == row
        assert field.col == col
        # Assumming that button grid spacing is 51 pixels
        assert field.x == 478
        assert field.y == 576

    def test_generate_fields(self, basic_model):
        assert len(basic_model.fields) == basic_model.rows
        assert len(basic_model.fields) * len(basic_model.fields[0]) == basic_model.rows * basic_model.columns

    def test_neighbours_middle(self, basic_model):
        tested_field = basic_model.fields[4][5]
        neighbours = tested_field.neighbours
        assert neighbours
        assert isinstance(neighbours, set)

        expected_neighbours = {
            basic_model.fields[3][4],
            basic_model.fields[3][5],
            basic_model.fields[3][6],
            basic_model.fields[4][4],
            basic_model.fields[4][6],
            basic_model.fields[5][4],
            basic_model.fields[5][5],
            basic_model.fields[5][6]
        }
        assert expected_neighbours == neighbours

    def test_neighbours_topleftcorner(self, basic_model):
        tested_field = basic_model.fields[0][0]
        neighbours = tested_field.neighbours

        expected_neighbours = {
            basic_model.fields[0][1],
            basic_model.fields[1][0],
            basic_model.fields[1][1]
        }
        assert expected_neighbours == neighbours

    def test_neighbours_bottomrightcorner(self, basic_model):
        tested_field = basic_model.fields[15][29]
        neighbours = tested_field.neighbours

        expected_neighbours = {
            basic_model.fields[14][28],
            basic_model.fields[14][29],
            basic_model.fields[15][28]
        }
        assert expected_neighbours == neighbours


class TestField:

    @pytest.fixture
    def basic_field(self) -> Field:
        return Field(8, 4, 50, 70)

    @pytest.fixture
    def field_with_neighbours(self):
        x_foo = 100
        y_bar = 100
        field = Field(1, 1, x_foo, y_bar, state='2')
        nbour_nw = Field(0, 0, x_foo, y_bar, state='*')
        nbour_n = Field(0, 1, x_foo, y_bar, state='1')
        nbour_ne = Field(0, 2, x_foo, y_bar, state='_')
        nbour_w = Field(1, 0, x_foo, y_bar, state='*')
        nbour_e = Field(1, 2, x_foo, y_bar, state='1')
        nbour_sw = Field(2, 0, x_foo, y_bar, state='*')
        nbour_s = Field(2, 1, x_foo, y_bar, state='2')
        nbour_se = Field(2, 2, x_foo, y_bar, state='m')
        nbour_n.neighbours = {nbour_nw, nbour_ne, nbour_w, field, nbour_e}
        nbours = [nbour_nw, nbour_n, nbour_ne, nbour_w, nbour_e, nbour_sw,
                  nbour_s, nbour_se]
        field.neighbours = set(nbours)
        return field, nbours

    def test_field_init(self, basic_field):
        assert basic_field is not None
        assert isinstance(basic_field, Field)
        assert basic_field.col is not None
        assert basic_field.row is not None
        assert basic_field.x is not None
        assert basic_field.y is not None
        assert basic_field.state == '*'
        assert basic_field.neighbours == set()

    def test_isnumber(self, basic_field):
        basic_field.state = '1'
        assert basic_field.is_number()
        basic_field.state = '2'
        assert basic_field.is_number()
        basic_field.state = '3'
        assert basic_field.is_number()
        basic_field.state = '4'
        assert basic_field.is_number()
        basic_field.state = '5'
        assert basic_field.is_number()
        basic_field.state = '6'
        assert basic_field.is_number()
        basic_field.state = '7'
        assert basic_field.is_number()
        basic_field.state = '8'
        assert basic_field.is_number()
        basic_field.state = '*'
        assert not basic_field.is_number()
        basic_field.state = 'm'
        assert not basic_field.is_number()
        basic_field.state = 'e'
        assert not basic_field.is_number()

    def test_iscomplete(self, custom_board):
        board_rows, board_columns = 3, 3
        states = (
            '_', '1', '*',
            'm', '3', '*',
            'm', '3', '*'
        )
        fields = custom_board(board_rows, board_columns, states).fields

        assert not fields[1][1].is_complete()
        assert not fields[2][1].is_complete()
        assert fields[0][1].is_complete()

    def test_custom_board_fixture(self, custom_board):
        board_rows, board_columns = 4, 4
        states = (
            '*', '1', '_', '_',
            '*', '2', '1', '2',
            '*', '2', 'm', '2',
            '1', '1', '1', '2'
        )
        fields = custom_board(board_rows, board_columns, states).fields
        assert fields[0][0].state == '*'

    def test_intersection(self, custom_board):
        board_rows, board_columns = 4, 4
        states = (
            '*', '1', '_', '_',
            '*', '2', '1', '1',
            '*', '2', 'm', '1',
            '1', '1', '1', '1'
        )
        fields = custom_board(board_rows, board_columns, states).fields
        field_1 = fields[0][1]
        field_2 = fields[1][1]
        assert field_1.intersection_with(field_2) == {fields[0][0], fields[1][0]}

    def test_difference(self, custom_board):
        board_rows, board_columns = 4, 4
        states = (
            '*', '1', '_', '_',
            '*', '2', '1', '1',
            '*', '2', 'm', '1',
            '1', '1', '1', '1'
        )
        fields = custom_board(board_rows, board_columns, states).fields
        assert fields[1][1].difference_with(fields[0][1]) == {fields[2][0]}
        assert fields[2][1].difference_with(fields[3][1]) == {fields[1][0]}
        assert fields[1][1].difference_with(fields[2][1]) == {fields[0][0]}

    def test_get_nbours(self, custom_board):
        board_rows, board_columns = 3, 3
        states = (
            '*', '1', '_',
            '*', '2', '1',
            '*', '2', 'm'
        )
        fields = custom_board(board_rows, board_columns, states).fields

        field = fields[1][1]
        all_neighbours = field.get_nbours()
        assert all_neighbours == field.neighbours
        mine_neighbours = field.get_nbours('m')
        assert mine_neighbours == {fields[2][2]}
        number_neighbours = field.get_nbours('n')
        assert number_neighbours == {fields[0][1], fields[1][2], fields[2][1]}
        one_neighbours = field.get_nbours('1')
        assert one_neighbours == {fields[0][1], fields[1][2]}
        covered_nbours = field.get_nbours('*')
        assert covered_nbours == {fields[0][0], fields[1][0], fields[2][0]}

    def test_getcoveredneighbours(self, custom_board):
        board_rows, board_columns = 3, 2
        states = (
            '_', '*',
            'm', '2',
            '*', '1'
        )
        fields = custom_board(board_rows, board_columns, states).fields

        assert len(fields[1][1].get_nbours('*')) == 2
        assert len(fields[2][1].get_nbours('*')) == 1

    def test_mineneighbours(self, custom_board):
        board_rows, board_columns = 3, 2
        states = (
            '_', '*',
            'm', '2',
            '*', '1'
        )
        fields = custom_board(board_rows, board_columns, states).fields

        assert len(fields[1][1].get_nbours('m')) == 1
        assert len(fields[2][1].get_nbours('m')) == 1

    def test_mark_potentials(self, custom_board):
        board_rows, board_columns = 4, 4
        states = (
            '*', '*', '1', '_',
            '*', '*', '2', '1',
            '*', '*', '*', '2',
            '*', '*', '*', '1'
        )
        board = custom_board(board_rows, board_columns, states)
        fieldset = set()
        for row in board.fields:
            for field in row:
                fieldset.add(field)
        board.fields[0][0]._mark_potentials(fieldset, 'pm')
        assert board.fields[0][0].state == 'pm'
        assert board.fields[0][1].state == 'pm'
        assert board.fields[0][2].state == '1'
        assert board.fields[0][3].state == '_'
        assert board.fields[1][0].state == 'pm'
        assert board.fields[1][1].state == 'pm'
        assert board.fields[1][2].state == '2'
        assert board.fields[1][3].state == '1'
        assert board.fields[2][0].state == 'pm'
        assert board.fields[2][1].state == 'pm'
        assert board.fields[2][2].state == 'pm'
        assert board.fields[2][3].state == '2'
        assert board.fields[3][0].state == 'pm'
        assert board.fields[3][1].state == 'pm'
        assert board.fields[3][2].state == 'pm'
        assert board.fields[3][3].state == '1'

        board.fields[1][1]._mark_potentials(fieldset, 'pn')
        assert board.fields[0][0].state == 'pm'
        assert board.fields[0][1].state == 'pm'
        assert board.fields[0][2].state == '1'
        assert board.fields[0][3].state == '_'
        assert board.fields[1][0].state == 'pm'
        assert board.fields[1][1].state == 'pm'
        assert board.fields[1][2].state == '2'
        assert board.fields[1][3].state == '1'
        assert board.fields[2][0].state == 'pm'
        assert board.fields[2][1].state == 'pm'
        assert board.fields[2][2].state == 'pm'
        assert board.fields[2][3].state == '2'
        assert board.fields[3][0].state == 'pm'
        assert board.fields[3][1].state == 'pm'
        assert board.fields[3][2].state == 'pm'
        assert board.fields[3][3].state == '1'

        board = custom_board(board_rows, board_columns, states)
        fieldset = set()
        for row in board.fields:
            for field in row:
                fieldset.add(field)
        board.fields[2][2]._mark_potentials(fieldset, 'pn')
        assert board.fields[0][0].state == 'pn'
        assert board.fields[0][1].state == 'pn'
        assert board.fields[0][2].state == '1'
        assert board.fields[0][3].state == '_'
        assert board.fields[1][0].state == 'pn'
        assert board.fields[1][1].state == 'pn'
        assert board.fields[1][2].state == '2'
        assert board.fields[1][3].state == '1'
        assert board.fields[2][0].state == 'pn'
        assert board.fields[2][1].state == 'pn'
        assert board.fields[2][2].state == 'pn'
        assert board.fields[2][3].state == '2'
        assert board.fields[3][0].state == 'pn'
        assert board.fields[3][1].state == 'pn'
        assert board.fields[3][2].state == 'pn'
        assert board.fields[3][3].state == '1'

    def test_mines_left(self, custom_board):
        custom_rows, custom_columns = 3, 3
        states = (
            '2', '*', '*',
            'm', '*', '3',
            '3', '*', '*'
        )
        fields = custom_board(custom_rows, custom_columns, states).fields
        assert fields[0][0].m_left() == 1
        assert fields[2][0].m_left() == 2
        assert fields[1][2].m_left() == 3


class TestFunctional:

    def test_mark_obvious_mines(self, custom_board):
        custom_rows, custom_columns = 5, 5
        states = (
            '*', '1', '1', '*', '*',
            '1', '1', '1', '2', '2',
            '2', '2', '2', '_', '_',
            '*', '*', '2', '1', '1',
            '3', '*', '2', '1', '*'
        )
        fields = custom_board(custom_rows, custom_columns, states).fields
        fields[1][0].mark_obvious_mines()
        assert fields[0][0].state == 'pm'
        fields[1][3].mark_obvious_mines()
        assert fields[0][3].state == 'pm'
        assert fields[0][4].state == 'pm'

    def test_iterate_over_num_neighbours(self, custom_board):
        custom_rows, custom_columns = 7, 7
        states = (
            '*', '*', '*', '*', '*', '*', '*',
            '1', '1', '1', '1', '1', '1', '*',
            '_', '_', '_', '_', '_', '1', '*',
            '1', '2', '2', '1', '_', '1', '*',
            '*', '*', '*', '1', '_', '1', '*',
            '*', '*', '*', '3', '2', '1', '*',
            '*', '*', '*', '*', '*', '*', '*'
        )
        fields = custom_board(custom_rows, custom_columns, states).fields
        fields[1][1].iterate_over_num_neighbours()
        assert fields[0][2].state == 'pn'
        fields[3][1].iterate_over_num_neighbours()
        assert fields[4][2].state == 'pm'
        fields[5][4].iterate_over_num_neighbours()
        assert fields[6][3].state == 'pm'
        assert fields[4][6].state == 'pn'
        assert fields[5][6].state == 'pn'
        assert fields[6][6].state == 'pn'

    def test_few_ones_in_line(self, custom_board):
        board_rows, board_columns = 4, 3
        states = (
            '*', '1', '_',
            '*', '1', '_',
            '*', '1', '_',
            '*', '1', '_'
        )
        #   '*', '1', '_',
        #   '*', '1', '_',
        #   'n', '1', '_',
        #   '*', '1', '_'
        board = custom_board(board_rows, board_columns, states)

        board.fields[1][1].iterate_over_num_neighbours()
        assert board.fields[2][0].state == 'pn'

    def test_iterate_over_higher_num_neighbours(self, custom_board):
        custom_rows, custom_columns = 7, 7
        states = (
            '*', '*', '*', '*', '*', '*', '*',
            '*', '3', '4', 'm', '*', '*', '*',
            '*', '*', '1', '1', '*', '*', '*',
            '*', '*', '*', '*', '*', '*', '*',
            '*', '*', '*', 'm', '*', '*', '*',
            '*', '*', 'm', '3', '4', '2', '*',
            '*', '*', '*', 'm', '*', '*', '*'
        )
        #   '*', 'M', 'M', 'M', '*', '*', '*',
        #   '*', '3', '4', 'm', 'n', '*', '*',
        #   '*', 'n', '1', '1', 'n', '*', '*',
        #   '*', 'n', 'n', 'n', 'n', '*', '*',
        #   '*', '*', 'n', 'm', 'n', 'M', 'n',
        #   '*', '*', 'm', '3', '4', '2', 'n',
        #   '*', '*', 'n', 'm', 'n', 'M', 'n'
        board = custom_board(custom_rows, custom_columns, states)
        fields = board.fields
        pot_mines, pot_numbers = board.get_potentials()
        assert fields[0][0].state == '*'
        assert fields[0][1] in pot_mines
        assert fields[0][2] in pot_mines
        assert fields[0][3] in pot_mines

        assert fields[1][0].state == '*'
        assert fields[1][4] in pot_numbers

        assert fields[2][0].state == '*'
        assert fields[2][1] in pot_numbers
        assert fields[2][4] in pot_numbers

        assert fields[3][1] in pot_numbers
        assert fields[3][2] in pot_numbers
        assert fields[3][3] in pot_numbers
        assert fields[3][4] in pot_numbers

        assert fields[4][2] in pot_numbers
        assert fields[4][4] in pot_numbers
        assert fields[4][5] in pot_mines
        assert fields[4][6] in pot_numbers

        assert fields[5][6] in pot_numbers

        assert fields[6][2] in pot_numbers
        assert fields[6][4] in pot_numbers
        assert fields[6][5] in pot_mines
        assert fields[6][6] in pot_numbers

    def test_mark_pot_mines_covered_eq_state(self, custom_board):
        board_rows, board_columns = 3, 3
        states = (
            '*', '2', '_',
            '*', '3', '1',
            '*', '2', 'm'
        )
        #   'M', '2', '_',
        #   'M', '3', '1',
        #   'n', '2', 'm'
        board = custom_board(board_rows, board_columns, states)
        pot_mines, pot_numbers = board.get_potentials()
        assert board.fields[0][0] in pot_mines
        assert board.fields[1][0] in pot_mines
        assert board.fields[2][0] in pot_numbers

    def test_neighbour_misspoint_as_pot_nums(self, custom_board):
        board_rows, board_columns = 4, 4
        states = (
            '*', '*', '*', '*',
            '*', '3', 'm', 'm',
            '*', '4', '3', '3',
            '1', '2', 'm', '1'
        )
        #   'n', 'n', 'n', '*',
        #   'M', '3', 'm', 'm',
        #   'M', '4', '3', '3',
        #   '1', '2', 'm', '1'
        board = custom_board(board_rows, board_columns, states)
        pot_mines, pot_numbers = board.get_potentials()

        assert board.fields[0][0] in pot_numbers
        assert board.fields[0][1] in pot_numbers
        assert board.fields[0][2] in pot_numbers
        assert board.fields[1][0] in pot_mines
        assert board.fields[2][0] in pot_mines

    def test_sets_calculations_1(self, custom_board):
        board_rows, board_columns = 4, 3
        states = (
            '*', '3', 'm',
            '*', '3', '1',
            '*', '3', '1',
            '*', 'm', '1'
        )
        #   'M', '3', 'm',
        #   'M', '3', '1',
        #   'n', '3', '1',
        #   'M', 'm', '1'
        board = custom_board(board_rows, board_columns, states)
        pot_mines, pot_numbers = board.get_potentials()

        assert board.fields[0][0] in pot_mines
        assert board.fields[1][0] in pot_mines
        assert board.fields[3][0] in pot_mines
        assert board.fields[2][0] in pot_numbers

    def test_neighbour_numbers_iteration(self, custom_board):
        board_rows, board_columns = 5, 4
        states = (
            '*', '*', '*', '*',
            '*', 'm', '2', '*',
            'm', '3', '3', '*',
            'm', '3', '3', '*',
            '1', '2', 'm', '*'
        )
        #   '*', 'n', 'n', 'n',
        #   'n', 'm', '2', '*',
        #   'm', '3', '3', '*',
        #   'm', '3', '3', 'm',
        #   '1', '2', 'm', '*'
        board = custom_board(board_rows, board_columns, states)
        pot_mines, pot_numbers = board.get_potentials()

        assert board.fields[0][0].state == '*'
        assert board.fields[0][1] in pot_numbers
        assert board.fields[0][2] in pot_numbers
        assert board.fields[0][3] in pot_numbers
        assert board.fields[1][0] in pot_numbers
        assert board.fields[3][3] in pot_mines

    def test_ones_mark_pn_hastily(self, custom_board):
        board_rows, board_columns = 6, 6
        states = (
            '*', '*', '*', '*', '*', '*',
            '*', '4', '1', '1', '1', '*',
            '*', '2', '_', '_', '2', '*',
            '*', '1', '_', '_', '1', '*',
            '*', '1', '1', '_', '1', '1',
            '*', '*', '1', '_', '_', '_'
        )
        #   'm', 'n', 'm', 'n', 'n', 'n',
        #   'm', '4', '1', '1', '1', 'm',
        #   'm', '2', '_', '_', '2', 'n',
        #   'n', '1', '_', '_', '1', 'm',
        #   'n', '1', '1', '_', '1', '1',
        #   'n', 'm', '1', '_', '_', '_'

        board = custom_board(board_rows, board_columns, states)
        pot_mines, pot_numbers = board.get_potentials()

        assert board.fields[0][0] in pot_mines
        assert board.fields[0][1] in pot_numbers
        assert board.fields[0][2] in pot_mines
        assert board.fields[0][3] in pot_numbers
        assert board.fields[0][4] in pot_numbers
        assert board.fields[0][5] in pot_numbers

        assert board.fields[1][0] in pot_mines
        assert board.fields[1][5] in pot_mines

        assert board.fields[2][0] in pot_mines
        assert board.fields[2][5] in pot_numbers

        assert board.fields[3][0] in pot_numbers
        assert board.fields[3][5] in pot_mines

        assert board.fields[4][0] in pot_numbers

        assert board.fields[5][0] in pot_numbers
        assert board.fields[5][1] in pot_mines

    def test_two_ones_near_border(self, custom_board):
        board_rows, board_columns = 3, 3
        states = (
            '*', '1', '_',
            '*', '1', '_',
            '*', '1', '_'
        )
        #   'n', '1', '_',
        #   'm', '1', '_',
        #   'n', '1', '_'
        board = custom_board(board_rows, board_columns, states)

        pot_mines, pot_numbers = board.get_potentials()

        assert board.fields[0][0] in pot_numbers
        assert board.fields[1][0] in pot_mines
        assert board.fields[2][0] in pot_numbers

    def test_sets_calculations_2(self, custom_board):
        board_rows, board_columns = 6, 5
        states = (
            '*', '2', '1', '_', '_',
            '*', 'm', '1', '_', '_',
            '*', '3', '1', '_', '_',
            '*', '2', '1', '*', '_',
            '*', '2', 'm', '3', '2',
            '*', '*', '3', 'm', 'm'
        )
        #   'n', '2', '1', '_', '_',
        #   'm', 'm', '1', '_', '_',
        #   'm', '3', '1', '_', '_',
        #   'n', '2', '1', 'n', '_',
        #   'n', '2', 'm', '3', '2',
        #   'n', 'm', '3', 'm', 'm'
        board = custom_board(board_rows, board_columns, states)
        pot_mines, pot_numbers = board.get_potentials()

        assert board.fields[0][0] in pot_numbers
        assert board.fields[1][0] in pot_mines
        assert board.fields[2][0] in pot_mines
        assert board.fields[3][0] in pot_numbers
        assert board.fields[3][3] in pot_numbers
        assert board.fields[4][0] in pot_numbers
        assert board.fields[5][0] in pot_numbers
        assert board.fields[5][1] in pot_mines
