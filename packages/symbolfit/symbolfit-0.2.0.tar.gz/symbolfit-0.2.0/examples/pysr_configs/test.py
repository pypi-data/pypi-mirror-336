from pysr import PySRRegressor

pysr_config = PySRRegressor(
    model_selection = 'accuracy',
    niterations = 200,
    maxsize = 60,
    binary_operators = [
        '+', '*'
                     ],
    unary_operators = [
        'tanh', 'exp'
    ],
    nested_constraints = {
        'tanh':   {'tanh': 1, 'exp': 1, '*': 2},
        'exp':    {'tanh': 1, 'exp': 1, '*': 2},
        '*':      {'tanh': 2, 'exp': 2, '*': 2},
    },
    loss='loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
)
