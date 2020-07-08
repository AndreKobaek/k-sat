from random import randint, sample
from typing import List

from cnf import CNF
from cnf_io import append_clauses

# Generates list of expectedly s/2 random values between 1 and n


def generate_row_direct(n: int, s: int) -> List[int]:
    entries = sample(range(1, n + 1), s)
    return [x for x in entries if randint(0, 1)]


# generate the bit sequnce random number from [1,2**s-1] and take every variable at true bit position and let them enter.
def generate_unempty_row2(n: int, s: int) -> List[int]:
    return []


# Infinite loop potential, use within timeout
def generate_unempty_row(n: int, s: int) -> List[int]:
    generated_row = generate_row_direct(n, s)
    while generated_row == []:
        generated_row = generate_row_direct(n, s)
    return generated_row


# Takes a row of variables (row), and a b-vector entry (b \in (0,1)) and generates a list of clauses (list(list())), using the binary representation of 2^len(row)


def generate_clauses(row: list(), b: int) -> List[List[int]]:
    clauses = list(list())
    stringFormat = "{0:0" + str(len(row)) + "b}"
    for i in range(2 ** len(row) - 1):
        bin = [int(b) for b in stringFormat.format(i)]
        if sum(bin) % 2 == b:
            clauses.append([(a * 2 - 1) * b for (a, b) in zip(bin, row)])
    return clauses


# Generates list of no_of_rows elements with 0 and 1's randomly chosen


def b_column_vector(no_of_rows: int) -> List[int]:
    return [randint(0, 1) for x in range(no_of_rows)]


# Appends a list of clauses (list of list) to a copy of the input CNF, returning the copy


def generate_hashing(F: CNF, s: int, no_of_rows: int, n: int) -> List[List[int]]:
    clauses = list(list())
    b = b_column_vector(no_of_rows)
    for i in range(no_of_rows):
        row = generate_unempty_row(n, s)
        # row = generate_row_direct(n, s)
        if row != []:
            for clause in generate_clauses(row, b[i]):
                clauses.append(clause)
        else:
            if b[i] == 1:
                return None
    return clauses
