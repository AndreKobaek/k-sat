import random
from datetime import datetime

import numpy
import pandas as pd

from cnf_io import append_clauses, read_cnf_file
from count_exact import count_exact
from hashing import generate_hashing

r = 6
seed = 10

output_file = "input/output_hashing_experiement-r{}-nonemp-{}.csv".format(r, "y")
data_fields = ["s", "r", "n", "sol", "file", "datetime", "experiment", "seed"]
filename = "generated-input-bin_search/cnf-gen-L220-W3-C965-I6.cnf"
# 16032 solutions


def perform_experiment():
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    original_f = read_cnf_file(filename)
    df = pd.DataFrame(columns=data_fields)

    # no_of_rows in hashing
    random.seed(seed)
    # with open(output_file, "w", newline="") as csvfile:
    #     csvwriter = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     csvwriter.writerow(data_fields)
    for s in range(1, 2):
        for _ in range(1000):
            # generate clauses to be appended
            hashed_clauses = generate_hashing(original_f, s, r, original_f.number_of_literals)
            # check if clause generation is possible
            if hashed_clauses is None:
                sol = None
            else:
                temp_f = append_clauses(original_f, hashed_clauses)
                sol = count_exact(temp_f)

            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            df = df.append(
                {
                    "s": s,
                    "r": r,
                    "n": original_f.number_of_clauses,
                    "sol": sol,
                    "file": filename,
                    "datetime": dt_string,
                    "experiment": "hashing_experiment.py",
                    "seed": seed,
                },
                ignore_index=True,
            )
    df.to_csv(output_file)


def analyse_result():
    data = pd.read_csv(output_file)
    print("s,mean,std,count")
    for i in range(data.s.min(), data.s.max() + 1):
        subset = data[data.s == i]
        print("{},{:.2f},{:.2f},{}".format(i, subset.sol.mean(), subset.sol.std(), subset.sol.count()))


# perform_experiment()
analyse_result()
