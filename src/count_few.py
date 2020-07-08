from math import copysign
from os import getcwd, system
from sys import argv, maxsize
from typing import List

from cnf_io import CNF, write_cnf_file

solverName = "minisat_static"
job_number = 1  # int(argv[5])
# path = os.getcwd()
# checker = True
SATsolver = "./minisat_static"
# filename = "testFile.cnf"
tempFileName = "input/inputFile-{}.txt".format(job_number)
output = "input/output-{}.txt".format(job_number)
# query_solver = SATsolver + " " + tempFileName + " " + output + " >/dev/null"


def query_solver(F: CNF, solver: str = solverName) -> bool:
    if F is None or F.number_of_literals is None:
        return False
    if F.number_of_clauses != 0:
        write_cnf_file(F, tempFileName)
        if "abcd" not in solverName:
            query = "./solvers/{} {} {} >/dev/null".format(solverName, tempFileName, output)
        else:
            query = "./solvers/{} {} > {}".format(solverName, tempFileName, output)
        system(query)
        return satisfiable()
    else:
        return True


def satisfiable() -> bool:
    with open(output, "r") as satResult:
        resultLines = satResult.readlines()
    sub = " SATISFIABLE"
    if resultLines == []:
        return False
    return [s for s in resultLines if sub in s] != [] or resultLines[0][:3] == "SAT"


def remove_or_subtract(clause: list) -> List[int]:
    return_list = []
    for literal in clause:
        if abs(literal) != 1:
            return_list += [int(copysign(abs(literal) - 1, literal))]
    return return_list


def set_var(cnf: CNF, var: int) -> CNF:
    reduced_cnf = CNF()
    reduced_cnf.clauses = list(list())
    for clause in cnf.clauses:
        if var not in clause:
            new_clause = remove_or_subtract(clause)
            if new_clause == []:
                return None
            reduced_cnf.clauses.append(new_clause)
    reduced_cnf.number_of_literals = cnf.number_of_literals - 1
    reduced_cnf.number_of_clauses = len(reduced_cnf.clauses)
    return reduced_cnf


def count_few(F: CNF, maximum_runs: int = maxsize) -> int:
    if query_solver(F):
        if F.number_of_literals > 0:
            number_of_solutions = count_few(set_var(F, 1), maximum_runs) + count_few(set_var(F, -1), maximum_runs)
            if number_of_solutions <= maximum_runs:
                return number_of_solutions
            return None
        else:
            return 1
    else:
        return 0
