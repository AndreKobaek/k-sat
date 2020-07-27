from sys import argv
from os import system
from graph import Graph

output_file = "input/output_graph.txt"

# input_pattern = argv[1]
# input_graph = argv[2]


def count_hom(input_pattern: int, input_graph: int, output_file=output_file) -> int:
    query_str = "./../SubgraphThesis/experiments-build/experiments/experiments  -count -h {} -g {} > {}".format(
        input_pattern, input_graph, output_file
    )
    system(query_str)
    return read_result()


def read_result(output_file=output_file) -> int:
    with open(output_file, "r") as exactCount:
        resultLines = exactCount.readlines()
    try:
        return int(resultLines[0])
    except:
        return -1
