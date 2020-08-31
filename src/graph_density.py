from typing import List
from hom_sub_sanity_check import extract_file_names
from encode_in_cnf import read_graph
from statistics import mean


def calc_density(vertices: List[int], edges: List[int]) -> List[int]:
    densities = []
    for edge, vertex in zip(edges, vertices):
        density = (2 * edge) / (vertex * (vertex - 1))
        densities.append(density)
    return densities


if __name__ == "__main__":
    folders = [
        "ag",
        "cfi",
        "cmz",
        "k",
        "paley",
        "sts",
        "triang",
    ]
    print("folder, #files, avg_#vert, avg_#edg, density")
    for folder in folders:
        dir_path_graphs = "input/graphs/{}".format(folder)
        graphs, _ = extract_file_names(dir_path_graphs)
        vertices = []
        edges = []
        for graph in graphs:
            tmp_graph = read_graph(graph)
            edges.append(tmp_graph.number_of_edges)
            vertices.append(tmp_graph.number_of_verticies)
        densities = calc_density(vertices, edges)
        output = "{}, {}, {:.1f}, {:.1f}, {:.3f}".format(
            folder, len(densities), mean(vertices), mean(edges), sum(densities) / len(densities)
        )
        print(output)
