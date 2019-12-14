from hashing import *
from countFew import *
import time
import os
import math
import sys
import countFew
tempFileName = "input/inputFile.txt"

def the_algorithm(filename: str, epsilon: float, delta: float, s: int):
    copyInputFile(filename, tempFileName)
    F = read_cnf_file(tempFileName)
    n = F.number_of_literals
    if n / math.log(n, 2) <= 8 / delta:
        return count_few_branching(F)
    t = math.ceil(delta * n / 2.0 + 2.0 * math.log(1 / epsilon, 2))
    a = math.ceil(2 ** (t + (delta * n) / 2))
    try:
        return count_few_branching(F, a)
    except OutOfRunsException:
        z_m = 0
        for m in range(n-t):
            z_m = inner_m_loop(F, m, t, a, n, s)
            if z_m != None:
                return z_m
        return None

def the_algorithm_test(filename: str, solver: str, a: int, s: int):
    copyInputFile(filename, tempFileName)
    F = read_cnf_file(tempFileName)
    n = F.number_of_literals
    if n / math.log(n, 2) <= 24:
        return count_few_branching(F, solver)
    try:
        return count_few_branching(F, solver, a)
    except OutOfRunsException:
        t = math.ceil(1/3 * n / 2.0 + 2.0 * math.log(1.0 / 0.9, 2))
        z_m = 0
        for m in range(n-t):
            z_m = inner_m_loop(F, solver, m, t, a, n, s)
            if z_m != None:
                return z_m
        return None


def inner_m_loop(F: CNF, solver: str, m: int, t: int, a: int, n: int, s: int):
    z = 0
    for i in range(2**t):
        hashed_clauses = generate_hashing(F, s, m+t, n)
        if hashed_clauses != None:
            F_mi = append_clauses(F, hashed_clauses)
        else:
            return None
        try:
            z += count_few_branching(F_mi, solver, 4*a)
        except OutOfRunsException:
            return None
        if z >= 4*a:
            return None
    return 2**(m*z)

# Paths for external harddrive data
externalDir = '/media/andre/LinUXB/research-project/'
#directory = os.getcwd()+'/test/'
subDir = ['agile/', 'main/', 'incremental/', 'random/','test02/']
solvers = ['minisat_static', 'glucose_static'] #,'abcdSAT','abcdsat_r17']
dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
directory = externalDir+subDir[4]
entries = os.listdir(directory)
print("Experiment 1 - Which solver performs better, run @ {}. With the test files {} and the solvers {}".format(dt_string, entries, solvers))	
a, s = 5, 6
for entry in entries:
    filename = directory+entry
    for solver in solvers:
        countFew.counter = 0
        start = time.time()
        k = the_algorithm_test(filename, solver, a, s)
        end = time.time()
        print("{0}, {1}, {2:.4f}, {3}, {4}, ".format(filename, solver, float(end-start), k, countFew.counter))