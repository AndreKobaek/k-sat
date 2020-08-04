from datetime import datetime
from os import getcwd, listdir
from sys import argv
from types import LambdaType

from apx_to_d import apx_to_d
from cnf_io import copy_input_file, read_cnf_file

# input python run_apx_to_d.py "generated-input-bin_search/cnf-gen-L220-W3-C965-I6.cnf" 0.33 0.5 3 180 1337
# filename = argv[1]
# delta = float(argv[2])
# epsilon = float(argv[3])
# s = int(argv[4])
# timeout_limit = int(argv[5])
# job_number = int(argv[6])


def run_apx_to_d(
    filename: str, delta: float, epsilon: float, s: int, timeout_limit: int = 3000, job_number: int = None
) -> int:
    if job_number is not None:
        tempFileName = "input/inputFile-{}.txt".format(job_number)
    else:
        tempFileName = "input/inputFile.txt"
    copy_input_file(filename, tempFileName)
    F = read_cnf_file(tempFileName)
    return apx_to_d(F, delta, epsilon, s, timeout_limit)


# result_text = "{}, {}, {}, {}".format(filename, s, result, count_exact(F)-result)

# result_file = "{}/s-experiment-results/{}.csv".format(getcwd(), job_number)
# print(result_text)
# with open(result_file, "w") as result:
# result.write(result_text)

# solver function instead of string name of solver
# use lambda expression to parse specific solver into query_solver
# for entry in entries:
# Paths for external harddrive data
# externalDir = "/media/andre/LinUXB/research-project/"
# localpath = getcwd() # +'/test/'
# subDir = ["agile/", "main/", "incremental/", "random/", "test02/", "/generated-input/"]
# solvers = ["minisat_static", "glucose_static"]  # ,'abcdSAT','abcdsat_r17']
# dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
# directory = externalDir+subDir[4]
# directory = localpath + subDir[5]
# "/home/andre/Documents/research/k-sat/src/test01/"
# entries = os.listdir(directory)
# entries = directory + "cnf-gen-L220-W3-C100-J28.cnf"

# print(
# "Experiment 1 - Which solver performs better, run @ {}. \
# With the test files {} and the solvers {}".format(
#     dt_string, entries, solvers
# )
# )
