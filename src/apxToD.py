from hashing import *
from countFew import *
import math
import sys
tempFileName = "input/inputFile.txt"
#s = two times clausewidth perhaps.

def the_algorithm(filename: str, epsilon: float, delta: float, s: int):
    copyInputFile(filename, tempFileName)
    F = read_cnf_file(tempFileName)
    n = F.number_of_literals
    if n / math.log(n) <= 8 / delta:
        return count_few(F)
    t = math.ceil(delta * n / 2.0 + 2.0 * math.log(1 / epsilon))
    a = math.ceil(2 ** (t + (delta * n)/2))
    print(t)
    print(t+(delta*n)/2)
    try: 
        return count_few(F, a)
    except OutOfRunsException:
        z_m = 0
        for m in range(n-t):
            z_m += inner_m_loop(F, m, t, a, n, s)
        return (2**m) * z_m

def inner_m_loop(F: CNF, m:int, t:int, a:int, n: int, s: int):
    z_i = 0
    for i in range(2**t):
                hashed_clauses = generate_hashing(F, s, m+t, n)
                F_mi = append_clauses(F, hashed_clauses)
                try: 
                    z_i += count_few(F_mi, 4*a)
                except OutOfRunsException:
                    return z_i
                if z_i >= 4*a:
                    return z_i

print(the_algorithm("input/"+sys.argv[1]+".cnf",0.2,1/3, 6))