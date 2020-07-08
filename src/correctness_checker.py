from os import scandir
from time import time

from cnf_io import read_cnf_file
from count_exact import count_exact
from count_few import count_few


def check_correctness():
    with scandir("generated-input/") as cnf_problems:
        for cnf_problem in cnf_problems:
            F = read_cnf_file("generated-input/" + cnf_problem.name)
            timer_exact = time()
            exact_solutions = count_exact(F)
            timer_exact = time() - timer_exact
            if exact_solutions < 10000:
                timer_few = time()
                few_solutions = count_few(F)
                timer_few = time() - timer_few
                print(
                    "CNF: {0}: CE = {1} in {2:.2f}, CF = {3} in {4:.2f}".format(
                        cnf_problem.name, exact_solutions, timer_exact, few_solutions, timer_few,
                    )
                )
            else:
                print("CNF: {0}: CE = {1} in {2:.2f}".format(cnf_problem.name, exact_solutions, timer_exact))


def check_solutions(cnf_problem: string):
    with scandir("/home/akob/project/generated-input/") as cnf_problems:
        for cnf_problem in cnf_problems:
            F = read_cnf_file("/home/akob/project/generated-input/" + cnf_problem.name)
            timer_exact = time()
            exact_solutions = count_exact(F)
            timer_exact = time() - timer_exact
            print("CNF: {0}: CE = {1} in {2:.2f}".format(cnf_problem.name, exact_solutions, timer_exact))


check_solutions()
