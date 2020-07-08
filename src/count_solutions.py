from time import time
from typing import List

from cnf import CNF
from cnf_io import read_cnf_file
from count_exact import count_exact

# F = read_cnf_file("/home/akob/project/generated-input/"+filename)
# filename = "cnf-gen-L{}-W{}-C{}.cnf".format(
#         F.number_of_literals, 3, F.number_of_clauses
#     )
# "CNF: {0}: CE = {1} in {2:.2f}".format(
#     filename, exact_solutions, timer_exact
#     )


def check_solutions(F: CNF) -> List[int]:
    timer_exact = time()
    exact_solutions = count_exact(filename, output_file)
    timer_exact = time() - timer_exact
    return [exact_solutions, timer_exact]
