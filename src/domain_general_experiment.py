import pandas as pd

from datetime import datetime

from count_exact import count_hom_with_timeout
from count_homomorphism import count_homSub_with_timeout
from encode_in_cnf import produce_cnf
from hom_sub_sanity_check import extract_file_names


dir_path_patterns = "input/graphs/patterns"
target_path = "input/generated-hom-sub"
#"kublenz"
#specific_test_graphs = [f"{dir_path_graphs}/jazzmusicians.gr",f"{dir_path_graphs}/euroroads.gr"]
#Specific_test_patterns = [f"{dir_path_patterns}/square.gr",f"{dir_path_patterns}/cycle5.gr",f"{dir_path_patterns}/trianglehouse.gr"]

solvers = ["ganak", "sharp", "homSub", "approxmc3", "approxmc4"]
solvers = solvers[:3]
problem_types = ["--hom", "--emb"]
timeout = 45

data_fields = ["h", "g", "cnf", "datetime", "solver", "sols", "time", "experiment", "timeout", "problem_type", "i"]

def run_experiment(experiment, experiment_name):
    dir_path_graphs = "input/graphs/{}".format(experiment)

    dt_str = datetime.now().strftime("%d-%m-%Y-%H-%M")

    output_file = "input/{}-{}".format(experiment, dt_str)

    df = pd.DataFrame(columns=data_fields)
    graphs, _ = extract_file_names(dir_path_graphs)
    _, patterns = extract_file_names(dir_path_patterns)

    #graphs = specific_test_graphs
    #patterns = Specific_test_patterns

    total_combinations = len(graphs) * len(patterns) * len(problem_types)
    k = 0
    for problem_type in problem_types:
        count_type = "sub" if problem_type == "--emb" else "hom"
        for graph in graphs:
            for pattern in patterns:
                k += 1
                cnf_file = produce_cnf(problem_type, pattern, graph, target_path)
                for solver in solvers:
                    for i in range(10):
                        dt_str = datetime.now().strftime("%H:%M:%S")
                        print(
                            "{}, {}, {}, {}/{} - {}".format(
                                pattern.split("/")[-1], graph.split("/")[-1], solver, k, total_combinations, dt_str
                            )
                        )
                        if solver == "homSub":
                            results = count_homSub_with_timeout(count_type, pattern, graph, timeout)
                        else:
                            results = count_hom_with_timeout(cnf_file, solver, timeout, problem_type)

                        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        df = df.append(
                            {
                                "h": pattern.split("/")[-1],
                                "g": graph.split("/")[-1],
                                "cnf": cnf_file.split("/")[-1],
                                "datetime": dt_string,
                                "solver": solver,
                                "sols": results[0],
                                "time": results[1],
                                "experiment": experiment,
                                "timeout": timeout,
                                "problem_type": problem_type,
                                "i": i,
                            },
                            ignore_index=True,
                        )

    df.to_csv(output_file)
