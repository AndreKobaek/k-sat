from hom_sub_sanity_check import extract_file_names
from encode_in_cnf import read_graph
from graph_density import calc_density

if __name__ == "__main__":
    folders = [
        "ag",
        "cfi",
        "cmz",
        "k",
        "paley",
        "sts",
        "triang",
        "kublenz"
    ]
    print("folder, name, #vert, #edge, density")
    for folder in folders:
        dir_path_graphs = "input/graphs/{}".format(folder)
        graphs, _ = extract_file_names(dir_path_graphs,folder=="kublenz")

        for graph in graphs:
            tmp_graph = read_graph(graph)
            edges = tmp_graph.number_of_edges
            vertices = tmp_graph.number_of_verticies
            density = calc_density([vertices], [edges])
            name = graph.split("/")[-1]
            print(f"{folder},{name},{vertices},{edges},{density[0]:.3f}")
