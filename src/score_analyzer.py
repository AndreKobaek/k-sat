from sys import argv
import os
from typing import List

from pandas import DataFrame, concat, read_csv


def analyse_input(filename: str) -> DataFrame:
    # read input
    df = read_csv(filename)

    if df.empty:
        return None

    # consistent solution check
    cnfs = df["cnf"].drop_duplicates().values

    for cnf in cnfs:
        cnf_rows = df[df["cnf"] == cnf]["sols"]
        assert len(cnf_rows[cnf_rows != -1].unique()) == 1, f"{filename}-{cnf}"
        if len(cnf_rows[cnf_rows != -1].unique()) != 1:
            print(f"{filename} - {cnf}")

    # calculate par2 score
    averaged_runtimes_df = df.groupby(["cnf", "solver", "problem_type"])[["time"]].mean()

    par2 = averaged_runtimes_df.groupby(["solver", "problem_type"])[["time"]].sum()

    benchmark = df.iloc[0]["g"].split(".")[0]

    par2["size"] = len(df["g"].unique()) * len(df["h"].unique())

    par2["benchmark"] = benchmark

    return par2


def extract_file_names(dir_path: str, experiment: str) -> List[str]:
    results = []
    files = os.listdir(dir_path)
    for file_name in files:
        if experiment in file_name:
            full_file_name = f"{dir_path}/{file_name}"
            results.append(full_file_name)
    return results


def analyse_patterns(files: List[str]):
    concatenated_results = []
    for file in files:
        concatenated_results.append(read_csv(file))

    df = concat(concatenated_results)

    averaged_runtimes_df = df.groupby(["h", "cnf", "solver", "problem_type"])[["time"]].mean()

    par2 = averaged_runtimes_df.groupby(["h", "solver", "problem_type"])[["time"]].sum()

    return par2


def analyze(experiment_name):
    raw_results = extract_file_names("input", experiment_name)

    results_patterns = analyse_patterns(raw_results)

    # write output
    results_patterns.to_csv("results/pattern-results.csv")

    results = concat([analyse_input(filename) for filename in raw_results])

    results.to_csv(f"results/analysed-results-{experiment_name}.csv")


if __name__ == "__main__":
    experiment_name = argv[1]
    analyze(experiment_name)
