from input-unifier import dir_path
from score_analyzer import analyze
from domain_general_experiment import run_experiment
import os


folders = [
    "ag",
    "cfi",
    "cmz",
    "k",
    "paley",
    "triang",
]


def create_dir_if_abscent(dir_path: str):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

experiment_name = "large_problems"


if __name__ == "__main__":


    create_dir_if_abscent("input/generated-cnf-hom-sub")

    #Run the expiriments
    for experiment in folders:
        run_experiment(experiment, experiment_name)
    
    create_dir_if_abscent("results")
    
    #Run the analyser
    analyze(experiment_name)

