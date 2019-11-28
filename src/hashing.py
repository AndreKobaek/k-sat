import copy
import random
from countFew import *
from typing import List

def generate_row_direct(n: int, s: int) -> List[int]:
    entries = random.sample(range(1, n+1), s)
    return [x for x in entries if random.randint(0,1)]

def generate_clauses(row: list(), b: int) -> List[List[int]]:
    clauses = list(list())
    stringFormat = "{0:0" + str(len(row)) + "b}"
    for i in range(2**len(row)-1):
        bin = [int(b) for b in stringFormat.format(i)]
        if (sum(bin)%2 == b):
            clauses.append([ (a*2-1)*b for (a,b) in zip(bin,row)])
    return clauses

def b_column_vector(no_of_rows: int) -> List[int]:
    return [random.randint(0,1) for x in range(no_of_rows)]

def append_clauses(F: CNF, clauses: List[List[int]]) -> CNF:
    F = copy.deepcopy(F)
    for clause in clauses:
        F.clauses.append(clause)
    return F

def generate_hashing(s: int, no_of_rows: int, n: int) -> List[List[int]]:
    clauses = list(list())
    b = b_column_vector(no_of_rows)
    for i in range(no_of_rows):
        row = generate_row_direct(n, s)
        if len(row)!=0:
            clauses.append(generate_clauses(row, b[i]))
    return clauses

### IRRELEVANT

# def generate_row(n: int):
#     one_entries = list(range(n))
#     random.shuffle(one_entries)
#     input_to_alter = one_entries[:s]
#     return_row = [0]*n
#     for i in input_to_alter:
#         if random.randint(0,1)==1:
#             return_row[i] = i+1
#     return return_row

# def hashing_matrix(rows: int, columns: int):
#     A = np.array(generate_row(columns))
#     for i in range(rows-1):
#         A = np.vstack([A,np.array(generate_row(columns))])
#     return A