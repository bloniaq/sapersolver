class Solver:

    def __init__(self):
        print('app initialized successfully')

    def solve(self):
        game = True
        win = False
        while game:
            # solving
            if self.mine_left() == 0:
                win = True
            game = False
        return win

    def mine_left(self):
        pass
