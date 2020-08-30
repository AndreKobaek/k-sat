import signal
from os import chdir, getcwd, killpg, system, setsid, kill
from subprocess import PIPE, Popen, TimeoutExpired
from time import monotonic as timer
from typing import List, Tuple

from count_approx import check_if_ind, append_ind_set, read_approx_result
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
    return read_sharp_result()


def count_sharp_with_timeout(filename: str, timeout_limit: int) -> int:
    query = ["./../sharpSAT/build/Release/sharpSAT {} > {}".format(filename, output)]
    # stolen from https://stackoverflow.com/questions/36952245/subprocess-timeout-failure
    with Popen(query, shell=True, stdout=PIPE, preexec_fn=setsid) as process:
        try:
            output_text = process.communicate(timeout=timeout_limit)[0]
            return read_sharp_result()
        except TimeoutExpired:
            killpg(process.pid, signal.SIGINT)  # send signal to the process group
            output_text = process.communicate()[0]
            return -1


ind_set_timeout = 10


def count_hom_with_timeout(filename: str, solver: str, timeout_limit: int, count_type: str) -> Tuple[int, float]:
    reset_cwd = getcwd()
    if solver == "ganak":
        chdir("../ganak/scripts/")
        query = ["./run_ganak.sh ../../src/{} > ../../src/{}".format(filename, output)]
    elif solver == "sharp":
        query = ["./../sharpSAT/build/Release/sharpSAT {} > {}".format(filename, output)]
    elif solver[:8] == "approxmc":
        if not check_if_ind(filename):
            bool_timeout = append_ind_set(filename, ind_set_timeout)
            if not bool_timeout:
                return [-1, timeout_limit]
        query = ["approxmc{} {} > {}".format(solver[-1], filename, output)]
    else:
        print("incorrect solver input")
        return (None, None)
    # stolen from https://stackoverflow.com/questions/36952245/subprocess-timeout-failure
    start = timer()
    with Popen(query, shell=True, stdout=PIPE, preexec_fn=setsid) as process:
        try:
            output_text = process.communicate(timeout=timeout_limit)[0]
        except TimeoutExpired:
            killpg(process.pid, signal.SIGINT)  # send signal to the process group
            chdir(reset_cwd)
            return (-1, 2 * timeout_limit)
    time = timer() - start
    auto_size = 1
    if solver == "ganak":
        chdir(reset_cwd)
    if count_type == "--emb":
        auto_size = read_auto_size(filename)
    if solver == "ganak":
        sols = int(read_ganak_result() / auto_size)
    elif solver == "sharp":
        sols = int(read_sharp_result() / auto_size)
    else:
        sols = int(read_approx_result() / auto_size)
    return (sols, time)


def count_exact_ganak(filename: str) -> int:
    query_str = "./run_ganak.sh ../../src/{} > ../../src/{}".format(filename, output)
    reset_cwd = getcwd()
    chdir("../ganak/scripts/")
    system(query_str)
    chdir(reset_cwd)
    return read_ganak_result()


def count_hom_ganak(filename: str) -> int:
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


def read_sharp_result() -> int:
    with open(output, "r") as exactCount:
        resultLines = exactCount.readlines()
    return int(resultLines[-5])


def read_ganak_time() -> float:
    with open(output, "r") as result_file:
        result_lines = result_file.readlines()
    for line in result_lines:
        if len(line) > 5 and line[:6] == "c time":
            return float(line.split()[-1][:-1])
    return -1.0


def read_sharp_time() -> float:
    with open(output, "r") as result_file:
        result_lines = result_file.readlines()
    for line in result_lines:
        if len(line) > 5 and line[:5] == "time:":
            return float(line.split()[-1][:-1])
    return -1.0


def count_sharp_file(filename: str, output_file="input/output.txt") -> List:
    query = "./../sharpSAT/build/Release/sharpSAT {} > {}".format(filename, output_file)
    system(query)
    return read_sharp_result_and_time(output_file)


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


def read_sharp_result_and_time(output_file: str) -> List:
    with open(output_file, "r") as exactCount:
        resultLines = exactCount.readlines()
    if resultLines != []:
        for line in resultLines:
            if line[:4] == "time":
                return [int(resultLines[-5]), line.split()[-1]]
    else:
        return [-1, -1]
