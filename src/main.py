import os

from domain_general_experiment import run_experiment
from input_unifier import dir_path
from score_analyzer import analyze

small_instances = ["ag", "cfi", "cmz", "k", "paley", "triang", "sts"]
large_instances = ["kublenz"]


def create_dir_if_abscent(dir_path: str):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


timeout = 45


if __name__ == "__main__":

    create_dir_if_abscent("input/generated-cnf-hom-sub")

    # Run the experiments
    experiment_name = "small_problems"

    for experiment in small_instances:
        run_experiment(experiment, experiment_name, 45)

    create_dir_if_abscent("results")

    analyze(experiment_name)

    experiment_name = "large_problems"

    for experiment in large_instances:
        run_experiment(experiment, experiment_name, 900)

    # Run the analyser
    analyze(experiment_name)
