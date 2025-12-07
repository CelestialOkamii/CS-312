# See additional instructions for these tests in the instructions for the project

from tsp_solve import matrix_reducer
from math import inf


def test_reduced_cost_matrix_1():
    start_matrix = [
        [0, 7, 1],
        [2, 0, 6],
        [2, 1, 0]
    ]

    reduced_matrix, lower_bound = matrix_reducer(start_matrix)

    assert lower_bound == 0
    assert reduced_matrix == [
        [0, 7, 1],
        [2, 0, 6],
        [2, 1, 0]
    ]


def test_reduced_cost_matrix_2():
    start_matrix = [
        [inf, 7, 3, 12],
        [3, inf, 6, 14],
        [5, 8, inf, 6],
        [9, 3, 5, inf]
    ]

    reduced_matrix, lower_bound = matrix_reducer(start_matrix)
    assert lower_bound == 15
    assert reduced_matrix == [
        [inf, 4, 0, 8],
        [0, inf, 3, 10],
        [0, 3, inf, 0],
        [6, 0, 2, inf]
    ]

# Add more tests as necessary...
