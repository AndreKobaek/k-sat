from os import getcwd, scandir

from numpy import nan
from pandas import DataFrame, concat, read_csv

csv_location = getcwd() + "/experiment-find-cnf/"


def collect_results() -> DataFrame:
    names = ["filename", "#solutions", "time", "#C", "#L", "CW", "#job"]
    results = DataFrame(columns=names)
    with scandir(csv_location) as csv_files:
        for csv_file in csv_files:
            df1 = read_csv(csv_location + csv_file.name, names=names)
            results = concat([results, df1], ignore_index=True)
    return results


results = collect_results()
results["time"] = results["time"].apply(lambda x: float(x[:-1]))
results = results.sort_values(by=["#job"])
# results.to_csv("results.csv")
# print(results)
