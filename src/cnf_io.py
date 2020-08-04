from copy import deepcopy
from shutil import copyfile
from typing import List

from cnf import CNF

# from runApxToD import tempFileName


def copy_input_file(filename: str, tempFile: str):
    copyfile(filename, tempFile)


def write_cnf_file(F: CNF, filename: str, auto_size: int = 0, ind_set: List[int] = []):
    if auto_size > 0:
        auto_size_line = "c automorphism group size {}\n".format(auto_size)
    metadata = "p cnf {} {}\n".format(F.number_of_literals, F.number_of_clauses)
    if ind_set != []:
        ind_set_line = "c ind " + " ".join([str(x) for x in ind_set]) + " 0\n"
    with open(filename, "w") as cnf_file:
        if ind_set != []:
            cnf_file.write(ind_set_line)
        if auto_size > 0:
            cnf_file.write(auto_size_line)
        cnf_file.write(metadata)
        cnf_file.writelines(" ".join([str(x) for x in y] + ["0\n"]) for y in F.clauses)


def read_cnf_file(filename: str) -> CNF:
    with open(filename, "r") as cnfFile:
        lines = list(filter(lambda line: line.strip(), cnfFile.readlines()))
    cnf = CNF()
    cnf.clauses = list(list())
    for line in lines:
        if len(line) > 20 and line[:20] == "c automorphism group":
            cnf.automorphism_group_size = int(line.split()[-1])
        elif line[0] == "c":
            continue
        elif line[0] == "p":
            metadata = line.split()
            cnf.number_of_literals = int(metadata[2])
            cnf.number_of_clauses = int(metadata[3])
        else:
            cnf.clauses.append([int(x) for x in line.split()[:-1]])
    return cnf


def read_auto_size(filename: str) -> int:
    with open(filename, "r") as cnfFile:
        lines = list(filter(lambda line: line.strip(), cnfFile.readlines()))
    for line in lines:
        if len(line) > 20 and line[:20] == "c automorphism group":
            return int(line.split()[-1])
        else:
            continue


def append_clauses(F: CNF, new_clauses: List[List[int]]) -> CNF:
    F = deepcopy(F)
    for new_clause in new_clauses:
        F.clauses.append(new_clause)
    F.number_of_clauses += len(new_clauses)
    return F
