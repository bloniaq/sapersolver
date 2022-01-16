from solver.model import *
import pytest
import logging


log = logging.getLogger('solver.tests')


class TestModel:

    @pytest.fixture
    def basic_model(self) -> Board:
        TOP = 200
        LEFT = 400
        model = Board(TOP, LEFT)
        return model

    def test_model_init(self, basic_model):
        assert basic_model is not None
        assert isinstance(basic_model, Board)

    def test_dimensions(self, basic_model):
        assert basic_model.columns == 30
        assert basic_model.rows == 16

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

    def test_mark_pot_mines_covered_eq_state(self, basic_model):
        basic_model.fields[0][1].state = '2'
        basic_model.fields[1][1].state = '3'
        basic_model.fields[0][2].state = '_'
        basic_model.fields[1][2].state = '1'
        basic_model.get_potential()
        assert basic_model.fields[0][0].state == 'pm'
        assert basic_model.fields[1][0].state == 'pm'

    # def test_sets_calculations_1(self, basic_model):
    #     basic_model.fields[0][1].state = '3'
    #     basic_model.fields[0][2].state = 'm'
    #     basic_model.fields[1][1].state = '2'
    #     basic_model.fields[1][2].state = '1'
    #     basic_model.fields[2][1].state = '3'
    #     basic_model.fields[2][2].state = '1'
    #     basic_model.fields[3][1].state = 'm'
    #     basic_model.fields[3][2].state = '2'
    #     basic_model._sets_calculations(basic_model.fields[1][1])
    #     assert basic_model.fields[3][0].state == 'pm'
    #     basic_model.fields[3][0].state == '*'
    #     basic_model._sets_calculations(basic_model.fields[2][1])
    #     assert basic_model.fields[3][0].state == 'pm'

    # def test_sets_calculations_2(self, basic_model):
    #     basic_model.fields[1][0].state = 'm'
    #     basic_model.fields[1][1].state = '2'
    #     basic_model.fields[1][2].state = '1'
    #     basic_model.fields[1][3].state = '1'
    #     basic_model._sets_calculations(basic_model.fields[1][2])
    #     assert basic_model.fields[0][1].state == 'pf'
    #     basic_model.fields[0][1].state = '*'
    #     basic_model._sets_calculations(basic_model.fields[1][3])
    #     assert basic_model.fields[0][1].state == 'pf'


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

    @pytest.fixture
    def custom_board(self):

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
        assert basic_field.isnumber()
        basic_field.state = '2'
        assert basic_field.isnumber()
        basic_field.state = '3'
        assert basic_field.isnumber()
        basic_field.state = '4'
        assert basic_field.isnumber()
        basic_field.state = '5'
        assert basic_field.isnumber()
        basic_field.state = '6'
        assert basic_field.isnumber()
        basic_field.state = '7'
        assert basic_field.isnumber()
        basic_field.state = '8'
        assert basic_field.isnumber()
        basic_field.state = '*'
        assert not basic_field.isnumber()
        basic_field.state = 'm'
        assert not basic_field.isnumber()
        basic_field.state = 'e'
        assert not basic_field.isnumber()

    def test_iscomplete(self, custom_board):
        board_rows, board_columns = 3, 3
        states = (
            '_', '1', '*',
            'm', '3', '*',
            'm', '3', '*'
        )
        fields = custom_board(board_rows, board_columns, states).fields

        assert not fields[1][1].iscomplete()
        assert not fields[2][1].iscomplete()
        assert fields[0][1].iscomplete()

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
            '*', '2', '1', '2',
            '*', '2', 'm', '2',
            '1', '1', '1', '2'
        )
        fields = custom_board(board_rows, board_columns, states).fields
        field_1 = fields[0][1]
        field_2 = fields[1][1]
        assert field_1._intersection(field_2) == {fields[0][0], fields[1][0]}

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

        assert len(fields[1][1].getcoveredneighbours()) == 2
        assert len(fields[2][1].getcoveredneighbours()) == 1

    def test_two_ones_near_border(self, custom_board):
        board_rows, board_columns = 3, 3
        states = (
            '*', '1', '_',
            '*', '1', '_',
            '*', '2', '_'
        )
        fields = custom_board(board_rows, board_columns, states).fields

        checked_field = fields[1][1]
        expected_potential_number = fields[2][0]

        potential_mines = set()
        potential_numbers = set()
        potential_mines, potential_numbers =\
            checked_field._check_whats_with_neighbours(
                potential_mines, potential_numbers)
        assert not potential_mines
        assert expected_potential_number in potential_numbers

    def test_mineneighbours(self, custom_board):
        board_rows, board_columns = 3, 2
        states = (
            '_', '*',
            'm', '2',
            '*', '1'
        )
        fields = custom_board(board_rows, board_columns, states).fields

        assert len(fields[1][1].getmineneighbours()) == 1
        assert len(fields[2][1].getmineneighbours()) == 1
