from os import system

from cnf_io import read_cnf_file, read_auto_size, write_cnf_file
from compute_ind_set import extract_ind_set

output = "input/output.txt"


def check_if_ind(filename: str) -> bool:
    with open(filename, "r") as cnf_file:
        lines = cnf_file.readlines()
    for line in lines:
        if len(line) > 5 and line[:5] == "c ind":
            return True
    return False


def append_ind_set(filename: str) -> bool:
    ind_set = extract_ind_set(filename)
    formula = read_cnf_file(filename)
    auto_size = formula.automorphism_group_size if formula.automorphism_group_size is not None else 0
    write_cnf_file(formula, filename, auto_size, ind_set)


def read_result(filename: str, result_type: str):
    with open(filename, "r") as result:
        result_lines = result.readlines()
    if result_type == "sol":
        for line in result_lines:
            if line[0] == "s":
                return int(line.split()[-1])
    elif result_type == "time":
        for line in result_lines:
            if len(line) > 25 and line[:18] == "c [appmc] FINISHED":
                return float(line.split()[-2])
    return -1


def count_approxmc(filename: str, version: int) -> int:
    if not check_if_ind(filename):
        append_ind_set(filename)
    cmd = "approxmc{} {} > {}".format(version, filename, output)
    system(cmd)
    return read_result(output, "sol")


def count_hom_approxmc(filename: str, version: int) -> int:
    count = count_approxmc(filename, version)
    auto_size = read_auto_size(filename)
    return count / auto_size

def get_approxmc_time() -> int:
    return read_result(output, "time")