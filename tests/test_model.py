from solver.model import *
import pytest


class Test_Model:

    @pytest.fixture
    def basic_model(self) -> Board:
        TOP = 200
        LEFT = 400
        model = Board(
            TOP,
            LEFT
        )
        return model

    def test_model_init(self, basic_model):
        assert basic_model is not None
        assert isinstance(basic_model, Board)

    def test_dimensions(self, basic_model):
        assert basic_model.columns == 30
        assert basic_model.rows == 16

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

class Test_Field:

    @pytest.fixture
    def basic_field(self) -> Field:
        COLUMN = 4
        ROW = 8
        X = 50
        Y = 70
        field = Field(
            COLUMN,
            ROW,
            X,
            Y
        )
        return field

    def test_field_init(self, basic_field):
        assert basic_field is not None
        assert isinstance(basic_field, Field)
        assert basic_field.col is not None
        assert basic_field.row is not None
        assert basic_field.x is not None
        assert basic_field.y is not None
        assert basic_field.state == 'c'
        assert basic_field.neighbours == []
