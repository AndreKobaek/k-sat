import copy
import random
from countFew import *
from typing import List


def generate_row_direct(n: int, s: int) -> List[int]:
    entries = random.sample(range(1, n+1), s)
    return [x for x in entries if random.randint(0, 1)]


def generate_clauses(row: list(), b: int) -> List[List[int]]:
    clauses = list(list())
    stringFormat = "{0:0" + str(len(row)) + "b}"
    for i in range(2**len(row)-1):
        bin = [int(b) for b in stringFormat.format(i)]
        if (sum(bin) % 2 == b):
            clauses.append([(a*2-1)*b for (a, b) in zip(bin, row)])
    return clauses


def b_column_vector(no_of_rows: int) -> List[int]:
    return [random.randint(0, 1) for x in range(no_of_rows)]


def append_clauses(F: CNF, new_clauses: List[List[int]]) -> CNF:
    F = copy.deepcopy(F)
    for new_clause in new_clauses:
        F.clauses.append(new_clause)
    F.number_of_clauses += len(new_clauses)
    return F


def generate_hashing(F: CNF, s: int, no_of_rows: int, n: int) -> List[List[int]]:
    clauses = list(list())
    b = b_column_vector(no_of_rows)
    for i in range(no_of_rows):
        row = generate_row_direct(n, s)
        if len(row) != 0:
            for clause in generate_clauses(row, b[i]):
                clauses.append(clause)
        else :
            if b[i] ==1:
                return None
    return clauses