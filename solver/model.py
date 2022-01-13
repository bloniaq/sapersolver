import logging as lg


lg.basicConfig(level=lg.INFO)


class Board:

    COLUMNS = 30
    ROWS = 16

    def __init__(self, top, left) -> None:
        self.columns = self.COLUMNS
        self.rows = self.ROWS

