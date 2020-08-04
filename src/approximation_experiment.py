import os
import random
import signal
from contextlib import contextmanager
from datetime import datetime

import pandas as pd

from cnf_io import read_cnf_file
from count_exact import count_exact_with_timeout
from run_apx_to_d import run_apx_to_d

seed = 10
random.seed(seed)


@contextmanager
def timeout(time):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    raise TimeoutError


def perform_experiment():
    directory = "test_input/"
    entries = os.listdir(directory)
    entries.sort()
    dt_string = datetime.now().strftime("%d-%m-%Y")
    output_file = "input/output_approximation_experiment_{}.csv".format(dt_string)

    data_fields = ["s", "n", "approx", "sol", "file", "datetime", "experiment", "seed"]
    experiment = "approximation_experiment.py"

    df = pd.DataFrame(columns=data_fields)
    for entry in entries:
        if entry.endswith(".cnf"):
            print(entry)
            F = read_cnf_file(directory + entry)
            sol = count_exact_with_timeout(F, 30)
            delta = 0.33
            epsilon = 0.5
            s = 9
            approx = run_apx_to_d(directory + entry, delta, epsilon, s, 30)

            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            df = df.append(
                {
                    "s": s,
                    "n": F.number_of_clauses,
                    "approx": approx,
                    "sol": sol,
                    "file": entry,
                    "datetime": dt_string,
                    "experiment": experiment,
                    "seed": seed,
                },
                ignore_index=True,
            )
    df.to_csv(output_file)


perform_experiment()
