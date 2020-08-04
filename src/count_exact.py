import subprocess
from os import chdir, getcwd, system
from typing import List

from cnf import CNF
from cnf_io import read_auto_size, write_cnf_file

tempFileName = "input/inputFile.txt"
output = "input/output.txt"

# divide by the size of the automorphism group, the number of embeddings from the pattern to the pattern.
# find tools to compute the automorphism group, subgraphs and embeddings


def count_exact(F: CNF) -> int:
    write_cnf_file(F, tempFileName)
    query = "./../sharpSAT/build/Release/sharpSAT {} > {}".format(tempFileName, output)
    system(query)
    return read_result()


def count_exact_with_timeout(F: CNF, timeout_limit: int) -> int:
    write_cnf_file(F, tempFileName)
    query = ["./../sharpSAT/build/Release/sharpSAT {} > {}".format(tempFileName, output)]
    try:
        process = subprocess.run(query, shell=True, timeout=timeout_limit)
        return read_result()
    except:
        return None


def count_exact_ganak(input_cnf: str) -> int:
    query_str = "./run_ganak.sh ../../src/{} > ../../src/{}".format(input_cnf, output)
    reset_cwd = getcwd()
    chdir("../ganak/scripts/")
    system(query_str)
    chdir(reset_cwd)
    return read_ganak_result()


def count_hom_ganak(filename: str, output="input/output.txt") -> int:
    query_str = "./run_ganak.sh ../../src/{} > ../../src/{}".format(filename, output)
    reset_cwd = getcwd()
    chdir("../ganak/scripts/")
    system(query_str)
    chdir(reset_cwd)
    auto_size = read_auto_size(filename)
    return read_ganak_result() / auto_size


def read_ganak_result() -> int:
    with open(output, "r") as exactCount:
        resultLines = exactCount.readlines()
    for line in resultLines:
        if line[0] == "s":
            return int(line.split()[-1])
    return -1


def read_result() -> int:
    with open(output, "r") as exactCount:
        resultLines = exactCount.readlines()
    return int(resultLines[-5])


def read_ganak_time() -> float:
    with open(output, "r") as result_file:
        result_lines = result_file.readlines()
    for line in result_lines:
        if len(line)>5 and line[:6] == "c time":
            return float(line.split()[-1][:-1])
    return -1.0

def read_sharp_time() -> float:
    with open(output, "r") as result_file:
        result_lines = result_file.readlines()
    for line in result_lines:
        if len(line)>5 and line[:5] == "time:":
            return float(line.split()[-1][:-1])
    return -1.0

def count_exact_file(filename: str, output_file="input/output.txt") -> List:
    query = "./../sharpSAT/build/Release/sharpSAT {} > {}".format(filename, output_file)
    system(query)
    return read_result_file(output_file)


def count_hom_sharp(filename: str, output_file="input/output.txt") -> int:
    query = "./../sharpSAT/build/Release/sharpSAT {} > {}".format(filename, output_file)
    system(query)
    auto_size = read_auto_size(filename)
    return read_hom_result_file(output_file) / auto_size


def read_hom_result_file(output_file: str) -> int:
    with open(output_file, "r") as exactCount:
        resultLines = exactCount.readlines()
    if resultLines != []:
        return int(resultLines[-5])
    return -1


def read_result_file(output_file: str) -> List:
    with open(output_file, "r") as exactCount:
        resultLines = exactCount.readlines()
    if resultLines != []:
        for line in resultLines:
            if line[:4] == "time":
                return [int(resultLines[-5]), line.split()[-1]]
    else:
        return [-1, -1]
