from sys import argv

from cnf import CNF
from cnf_io import write_cnf_file
from count_exact import count_sharp_file
from graph import Graph
from os import path

suggested_dir = "input/generated-hom-sub"


def read_graph(graph_filename: str) -> Graph:
    # print(graph_filename)
    with open(graph_filename, "r") as graph_file:
        lines = list(filter(lambda line: line.strip(), graph_file.readlines()))
    graph = Graph()
    graph.edges = list(list())
    for line in lines:
        if line[0] == "c":
            continue
            # extract meta data, if using p-char as metadata indicator
        elif line[0] == "p":
            metadata = line.split()
            graph.number_of_verticies = int(metadata[2])

        elif line[0] == "%":
            metadata = line.split()
            # skipping comment lines not containing meta data, but using same indicator character
            try:
                graph.number_of_verticies = int(metadata[1])
            except:
                pass
        else:
            split_char = ""
            if line[0] == "n" or line[0] == "e":
                split_char = line[0]
            graph.edges.append(sorted([int(x) for x in line.strip(split_char).split()]))
            # check if duplicates
    graph.number_of_edges = len(graph.edges)
    return graph


def produce_cnf(
    problemType: str,
    pattern_filename: str,
    graph_filename: str,
    target_dir: str = suggested_dir,
    compute_automorph_size=True,
) -> str:
    cnf_file_name = "{}/cnf-{}-h-{}-g-{}.cnf".format(
        target_dir,
        problemType.strip("--"),
        pattern_filename.split("/")[-1].split(".")[0],
        graph_filename.split("/")[-1].split(".")[0],
    )
    # if file already exists, return filename.
    if path.isfile(cnf_file_name):
        return cnf_file_name
    # read input files
    pattern = read_graph(pattern_filename)
    graph = read_graph(graph_filename)
    # create CNF:
    cnf = CNF(number_of_literals=pattern.number_of_verticies * graph.number_of_verticies, clauses=list(list()))

    def pair(a: int, v: int) -> int:
        return (a - 1) * graph.number_of_verticies + v

    # adding clauses to guarantee that each a is mapped to at least one vertex
    for a in range(1, pattern.number_of_verticies + 1):
        cnf.clauses.append(list(pair(a, v) for v in range(1, graph.number_of_verticies + 1)))

    for a in range(1, pattern.number_of_verticies + 1):
        for v in range(1, graph.number_of_verticies + 1):
            for w in range(v + 1, graph.number_of_verticies + 1):
                cnf.clauses.append([-pair(a, v), -pair(a, w)])

    # dictionary, to use for finding non existant pairs:

    non_existant_pairs = {}
    for i in range(1, graph.number_of_verticies + 1):
        non_existant_pairs[i] = list(range(i, graph.number_of_verticies + 1))

    for v, w in graph.edges:
        assert v < w
        non_existant_pairs[v].remove(w)

    for a, b in pattern.edges:
        for v, ws in non_existant_pairs.items():
            for w in ws:
                cnf.clauses.append([-pair(a, v), -pair(b, w)])
                if pair(a, v) != pair(a, w) or pair(b, w) != pair(b, v):
                    cnf.clauses.append([-pair(a, w), -pair(b, v)])

    # changed second pair to negative, not in the SS notes.
    if problemType == "--emb":
        for v in range(1, graph.number_of_verticies + 1):
            for a in range(1, pattern.number_of_verticies + 1):
                for b in range(a + 1, pattern.number_of_verticies + 1):
                    clause = [-pair(a, v), -pair(b, v)]
                    if clause not in cnf.clauses:
                        cnf.clauses.append(clause)

        # count the automorphism group size, by counting embeddings of the pattern unto the pattern.
        # embed it in a comment comment line on top.
    auto_size = 0
    if compute_automorph_size:
        auto_size_problem = produce_cnf("--emb", pattern_filename, pattern_filename, target_dir, False)
        auto_size = int(count_sharp_file(auto_size_problem)[0])

    cnf.number_of_clauses = len(cnf.clauses)
    write_cnf_file(cnf, cnf_file_name, auto_size)
    return cnf_file_name


if __name__ == "__main__":
    problemType = argv[1]
    if not problemType in ["--hom", "--emb"]:
        print('Aborted - please select either "--hom" or "--emb"')
    pattern_filename = argv[2]
    graph_filename = argv[3]
    produce_cnf(problemType, pattern_filename, graph_filename)
