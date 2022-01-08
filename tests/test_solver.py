import solver.controller as contr

def test_solved():
    app = contr.Solver()
    assert isinstance(app, contr.Solver)
    assert app.solve()