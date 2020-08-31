from count_exact import count_hom_with_timeout
from count_homomorphism import count_homSub_with_timeout
from encode_in_cnf import produce_cnf
import os
from typing import List, Tuple


def extract_file_names(dir_path: str, no_size_limit: bool = False) -> Tuple[List[str], List[str]]:
    graph_names = []
    pattern_names = []
    for dirpath, _, files in os.walk(dir_path):
        for file_name in files:
            full_file_name = "{}/{}".format(dirpath, file_name)
            if os.path.getsize(full_file_name) < 5 * 1024 or no_size_limit:
                if "patterns" not in dirpath:
                    graph_names.append(full_file_name)
                else:
                    pattern_names.append(full_file_name)
    return (graph_names, pattern_names)


def check_sanity(dir_path, solvers, problem_type, target_path, timeout):
    graphs, patterns = extract_file_names(dir_path)
    for graph in graphs:
        for pattern in patterns:
            for solver in solvers:
                test_file = produce_cnf(problem_type, pattern, graph, target_path)
                results = count_hom_with_timeout(test_file, solver, timeout, problem_type)
                reference = count_homSub_with_timeout("hom", pattern, graph, timeout)
                result_str = "h:{},g:{},solver:{},encoded:{},homSub:{},eq:{}".format(
                    pattern.split("/")[-1],
                    graph.split("/")[-1],
                    solver,
                    results,
                    reference,
                    results[0] == reference[0],
                )
                print(result_str)


def main():
    dir_path = "input/graphs-test/"
    target_path = "input/cnf-test"

    solvers = ["ganak", "sharp", "approxmc3", "approxmc4"]
    # solvers = solvers[:2]
    problem_types = ["--hom", "--emb"]
    problem_type = problem_types[0]
    timeout = 300
    check_sanity(dir_path, solvers, problem_type, target_path, timeout)
