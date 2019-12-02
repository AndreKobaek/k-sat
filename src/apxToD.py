from hashing import *
from countFew import *
import os
import math
import sys
tempFileName = "input/inputFile.txt"
# s = two times clausewidth perhaps.


# Set a = 1000
# 10 sec * x <= 30 min running time of minisat -> a <= 180
# choose a and t from this condition

def the_algorithm(filename: str, epsilon: float, delta: float, s: int):
    copyInputFile(filename, tempFileName)
    F = read_cnf_file(tempFileName)
    n = F.number_of_literals
    if n / math.log(n) <= 8 / delta:
        return count_few_branching(F)
    t = math.ceil(delta * n / 2.0 + 2.0 * math.log(1 / epsilon))
    a = math.ceil(2 ** (t + (delta * n) / 2))
    print(t)
    print(t+(delta*n)/2)
    try:
        return count_few_branching(F, a)
    except OutOfRunsException:
        z_m = 0
        for m in range(n-t):
            z_m = inner_m_loop(F, m, t, a, n, s)
            if z_m != None:
                return z_m
        return None


def the_algorithm_2(filename: str, a: int, s: int):
    copyInputFile(filename, tempFileName)
    F = read_cnf_file(tempFileName)
    n = F.number_of_literals
    t = math.ceil(1/3 * n / 2.0 + 2.0 * math.log(1.0 / 0.5))
    print("#literals/n: {}, #clauses: {}, t: {}".format(F.number_of_literals, F.number_of_clauses, t))
    if n <= 50:
        return count_few_branching(F)
    try:
        return count_few_branching(F, a)
    except OutOfRunsException:
        z_m = 0
        for m in range(n-t):
            z_m = inner_m_loop(F, m, t, a, n, s)
            if z_m != None:
                return z_m
        return None


def inner_m_loop(F: CNF, m: int, t: int, a: int, n: int, s: int):
    z = 0
    for i in range(2**t):
        if z>0: print("m: {}, i: {}, z_i: {}, n: {}, #c: {}".format(m, i, z, F.number_of_literals, F.number_of_clauses))
        hashed_clauses = generate_hashing(F, s, m+t, n)
        if hashed_clauses != None:
            F_mi = append_clauses(F, hashed_clauses)
        else:
            return None
        try:
            z += count_few_branching(F_mi, 4*a)
        except OutOfRunsException:
            return None
        if z >= 4*a:
            return None
    return 2**(m*z)


#print(the_algorithm_2("input/"+sys.argv[1]+".cnf", 1000, 6))

externalDir = '/media/andre/LinUXB/research-project/'
subDir1 = 'agile/'
subDir2 = 'main/'
subDir3 = 'incremental/'
subDir4 = 'random/'
directory = externalDir+subDir3
entries = os.listdir(directory)
a = 100
s = 6
for entry in entries:
    filename = directory+entry
    k = the_algorithm_2(filename,a,s)
    if k != None: print(filename+" "+str(k))