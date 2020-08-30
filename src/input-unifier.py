import os

from encode_in_cnf import read_graph
from graph import Graph

dir_path = "input/unfixed-graphs/"
target_path = "input/graphs"


def write_graph_file(graph: Graph, output_file_name: str):
    metadata = "p tw {} {}".format(graph.number_of_verticies, graph.number_of_edges)
    with open(output_file_name, "w") as graph_file:
        graph_file.write(metadata)
        graph_file.writelines(" ".join([str(x) for x in y] + ["\n"]) for y in graph.edges)

if __name__ == "__main__":
    for dirpath, dirnames, files in os.walk(dir_path):
        for file_name in files:
            if "." not in file_name:
                full_file_name = "{}/{}".format(dirpath, file_name)
                target_dir = "{}/{}".format(target_path, dirpath.split("/")[-1])
                target_file_name = "{}/{}.gr".format(target_dir, file_name)
                graph = read_graph(full_file_name)
                if not os.path.exists(target_dir):
                    os.mkdir(target_dir)
                write_graph_file(graph, target_file_name)
