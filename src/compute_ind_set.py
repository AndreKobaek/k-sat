import signal

from os import chdir, getcwd, system  # , killpg, setsid, kill

# from subprocess import PIPE, Popen, TimeoutExpired
# from time import monotonic as timer
from typing import List

output = "computed-set.ind"


def read_ind_set():
    with open("input/" + output, "r") as computed_set:
        ind_set = computed_set.readlines()
    try:
        return list(map(int, ind_set[0].split()))
    except:
        return []


def clear_ind_set():
    with open("input/" + output, "w") as set_to_clear:
        pass


def extract_ind_set(filename: str, timeout_limit: int) -> List[int]:
    clear_ind_set()
    query = "./mis.py ../src/{} --timeout {} --out ../src/input/{} > /dev/null".format(
        filename, timeout_limit, output
    )
    reset_cwd = getcwd()
    chdir("../mis")
    system(query)
    chdir(reset_cwd)
    return read_ind_set()
