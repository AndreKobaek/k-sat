import subprocess
from os import system
from typing import List

from cnf import CNF
from cnf_io import write_cnf_file

tempFileName = "input/inputFile.txt"
output = "input/output.txt"


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


def read_result() -> int:
    with open(output, "r") as exactCount:
        resultLines = exactCount.readlines()
    return int(resultLines[-5])


def count_exact_file(filename: str, output_file: str) -> List:
    query = "./../sharpSAT/build/Release/sharpSAT {} > {}".format(filename, output_file)
    system(query)
    return read_result_file(output_file)


def read_result_file(output_file: str) -> List:
    with open(output_file, "r") as exactCount:
        resultLines = exactCount.readlines()
    if resultLines != []:
        for line in resultLines:
            if line[:4] == "time":
                return [int(resultLines[-5]), line.split()[-1]]
    else:
        return [-1, -1]
