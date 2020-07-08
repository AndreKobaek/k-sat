import sys

import pytest

from cnf import CNF
from cnf_io import read_cnf_file
from hashing import *


@pytest.mark.parametrize("n, s", [(100, 20), (200, 10)])
def test_generate_row_direct(n, s):
    assert generate_row_direct(n, s) != [], "test failed"
    assert max(generate_row_direct(n, s)) <= n + 1
    assert min(generate_row_direct(n, s)) >= 1


@pytest.mark.parametrize("r", [1, 10, 100, 1000])
def test_b_column_vector(r):
    assert len(b_column_vector(r)) == r, "bad length"
    assert max(b_column_vector(r)) <= 1, "bad max value"
    assert min(b_column_vector(r)) >= 0, "bad min value"


@pytest.fixture
def fixed_cnf() -> CNF:
    return read_cnf_file("tests/simpleCNF.txt")


@pytest.mark.parametrize("new_clauses", [[[1, 2, 3], [3, 2, 1]], [1, 2, 3], [2, 2, 2], [4, 4, 4, 4], [1, 1]])
def test_append_clauses(fixed_cnf, new_clauses):
    assert fixed_cnf.number_of_clauses == 2
    assert append_clauses(fixed_cnf, new_clauses).number_of_clauses == fixed_cnf.number_of_clauses + len(new_clauses)
    for clause in new_clauses:
        assert clause in append_clauses(fixed_cnf, new_clauses).clauses


def test_generate_clauses():
    assert generate_clauses([1, 2, 3], 1) == [[-1, -2, 3], [-1, 2, -3], [1, -2, -3]]
    assert generate_clauses([1, 2, 3], 0) == [[-1, -2, -3], [-1, 2, 3], [1, -2, 3], [1, 2, -3]]
    assert generate_clauses([1], 1) == []
    assert generate_clauses([1], 0) == [[-1]]
