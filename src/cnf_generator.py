from random import randint, sample

from cnf import CNF
from cnf_io import write_cnf_file


def sign_chooser(n: int) -> int:
    if randint(0, 1):
        return n
    return -n


def generate_cnf(number_of_literals: int, clause_width, number_of_clauses: int) -> CNF:
    cnf = CNF()
    cnf.number_of_clauses = 0
    cnf.clauses = list(list())
    literals = set()

    while cnf.number_of_clauses < number_of_clauses:
        clause_elements = sample(range(1, number_of_literals + 1), clause_width)
        for elem in clause_elements:
            literals.add(elem)

        final_clause = sorted(list(map(sign_chooser, clause_elements)))

        if final_clause not in cnf.clauses:
            cnf.clauses.append(final_clause)
            cnf.number_of_clauses += 1

    cnf.number_of_literals = max(literals)
    return cnf


filepath_extension = "home/akob/project/"


def make_test_files(
    number_of_cnfs: int, number_of_clauses: int, number_of_literals: int, clause_width: int,
):
    for i in range(number_of_cnfs):
        F = generate_cnf(number_of_literals, clause_width, number_of_clauses)
        write_cnf_file(
            F,
            "generated-input/cnf-gen-L{}-W{}-C{}.cnf".format(F.number_of_literals, clause_width, number_of_clauses),
        )


def write_test_file(F: CNF, clause_width: int, folder_location: str) -> str:
    filename = "cnf-gen-L{}-W{}-C{}.cnf".format(F.number_of_literals, clause_width, F.number_of_clauses)
    write_cnf_file(F, folder_location + filename)
    return filename


# for number_of_literals in [220]:
#     for number_of_clauses in [25, 50, 75, 100, 125, 150, 175, 200, 1000]:
#         make_test_files(5, number_of_clauses, number_of_literals, 3)
