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

    # def test_get_field(self, basic_model):
    #     row = 4
    #     col = 6
    #     field = basic_model.get_field(col, row)
    #     assert field.row == row
    #     assert field.col == col
    #     assert field._x == 678
    #     assert field._y == 576

    def test_generate_fields(self, basic_model):
        assert len(basic_model.fields) == basic_model.rows
        assert len(basic_model.fields) * len(basic_model.fields[0]) == basic_model.rows * basic_model.columns


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
        assert basic_field._x is not None
        assert basic_field._y is not None
        assert basic_field.state == 'covered'
        assert basic_field.neighbours == []
