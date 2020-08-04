import os
from typing import List

output = "computed-set.ind"


def read_ind_set():
    with open("input/" + output) as computed_set:
        ind_set = computed_set.readlines()
    return list(map(int, ind_set[0].split()))


def extract_ind_set(filename: str) -> List[int]:
    cmd = "./mis.py ../src/{} --out ../src/input/{}".format(filename, output)
    reset_cwd = os.getcwd()
    os.chdir("../mis")
    os.system(cmd)
    os.chdir(reset_cwd)
    return read_ind_set()
