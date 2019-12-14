from shutil import copyfile
import copy
import math
import os
import sys
import time
from typing import List
from dataclasses import dataclass
from datetime import datetime

global_var = 0
counter = 0
#path = os.getcwd()
#tempFileName = "tester2.txt"
tempFileName = "input/inputFile.txt"
#checker = True
SATsolver = "./minisat_static"
#filename = "testFile.cnf"
output = "input/output.txt"
#query_solver = SATsolver + " " + tempFileName + " " + output + " >/dev/null"


class OutOfRunsException(Exception):
    pass

@dataclass
class CNF:
    number_of_literals: int = None
    number_of_clauses: int = None
    clauses: List[List[int]] = None


def query_solver(F: CNF, solver: str) -> bool:
    global counter
    global global_var
    counter += 1
    if F == None or F.number_of_literals == None:
        return False
    if F.number_of_clauses != 0:
        write_cnf_file(F, tempFileName)
        if "abcd" not in solver:
            query = "./solvers/{} {} {} >/dev/null".format(solver, tempFileName, output)    
        else:
            query = "./solvers/{} {} > {}".format(solver, tempFileName, output)
        start = time.time()
        os.system(query)
        end = time.time()
        global_var += end-start
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


def read_cnf_file(filename: str) -> CNF:
    with open(filename, "r") as cnfFile:
        lines = list(filter(lambda line: line.strip(), cnfFile.readlines()))
    cnf = CNF()
    cnf.clauses = list(list())
    for line in lines:
        if line[0] == "c":
            continue
        if line[0] == "p":
            metadata = line.split()
            cnf.number_of_literals = int(metadata[2])
            cnf.number_of_clauses = int(metadata[3])
        else:
            cnf.clauses.append([int(x) for x in line.split()[:-1]])
    return cnf


def write_cnf_file(F: CNF, filename: str):
    metadata = "p cnf {} {}\n".format(
        F.number_of_literals, F.number_of_clauses)
    with open(filename, "w") as cnfFile:
        cnfFile.write(metadata)
        cnfFile.writelines(" ".join([str(x) for x in y] + ["0\n"]) for y in F.clauses)


def remove_or_subtract(clause: list) -> List[int]:
    return_list = []
    for literal in clause:
        if abs(literal) != 1:
            return_list += [int(math.copysign(abs(literal) - 1, literal))]
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


def copyInputFile(filename: str, tempFile: str):
    copyfile(filename, tempFileName)


def count_few_branching(F: CNF, solver: str, maximum_runs: int = sys.maxsize) -> int:
    satisfiable = query_solver(F, solver)
    if satisfiable:
        if F.number_of_literals > 0:
            number_of_solutions = count_few_branching(set_var(
                F,  1), solver, maximum_runs) + count_few_branching(
                set_var(F, -1), solver, maximum_runs)
            if number_of_solutions <= maximum_runs:
                return number_of_solutions
            raise OutOfRunsException("FAIL")
        else:
            return 1
    else:
        return 0


def set_up_branching(filename: str, solver: str, a: int):
    copyInputFile(filename, tempFileName)
    start = time.time()
    F = read_cnf_file(tempFileName)
    k = 0
    try:
        k = count_few_branching(F, solver, a)
    except OutOfRunsException:
        k = None
    end = time.time()
    total_duration = end-start
    global counter
    global global_var
    print("File: {0}, Solver: {1}, Total: {2:.2f}, SolverPercent: {3:.2f}, solution: {4}".format(
        filename, solver, total_duration, 100*global_var/total_duration, k))

# Test for time spent on queries 
dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
solvers = ['minisat_static', 'glucose_static']# 'abcdSAT', 'abcdsat_r17']
files = ['testFile.cnf', 'testFile2.cnf', 'testFile4.cnf', 'testFile5.cnf', 'testFile7.cnf', 'simpleCNF.txt'] #[ 'simpleCNF.txt'] #
print("Experiment 2 - How much time is spent on queries, run @ {}. With the test files {} and the solvers {}".format(dt_string, files, solvers))	
for file in files:
    for solver in solvers:
        set_up_branching('test/'+file, solver, 5)
        counter = 0
        global_var = 0
