import solver.controller as contr

def test_solved():
    app = contr.Controller()
    assert isinstance(app, contr.Controller)
    assert app.solve()