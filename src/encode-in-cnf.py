from sys import argv
from graph import Graph
from cnf import CNF
from cnf_io import write_cnf_file

problemType = argv[1]
if not problemType in ["--hom", "--emb"]:
    print('Aborted - please select either "--hom" or "--emb"')
pattern_filename = argv[2]
graph_filename = argv[3]

def graph_reader(graph_filename: str) -> Graph:
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
            graph.number_of_edges = int(metadata[3])
        elif line[0] == "%":
            metadata = line.split()
            # skipping comment lines not containing meta data, but using same indicator character
            try:
                graph.number_of_verticies = int(metadata[1])
                graph.number_of_edges = int(metadata[2])
            except:
                pass
        else:
            graph.edges.append([int(x) for x in line.strip("e").split()])
    return graph


def produce_cnf(problemType: str, pattern_filename: str, graph_filename: str):
    #read input files
    pattern = graph_reader(pattern_filename)
    graph = graph_reader(graph_filename)
    #create CNF:
    cnf = CNF(number_of_literals=pattern.number_of_verticies * graph.number_of_verticies, clauses=list(list()))
    #adding clauses to guarantee that each a is mapped to at least one vertex
    for i in range(pattern.number_of_verticies):
        cnf.clauses.append(list(range(graph.number_of_verticies*i+1,graph.number_of_verticies*(i+1))))
    
    for i in range(pattern.number_of_verticies):
        for j in range(1, graph.number_of_verticies+1):
            for k in range(j+1, graph.number_of_verticies+1):
                cnf.clauses.append([-(j*i+1), -(k*(i+1))])
    
    #dictionary, to use for finding non existant pairs:
    
    non_existant_pairs = {}
    for i in range(1, graph.number_of_verticies):
        non_existant_pairs[i] = list(range(1, graph.number_of_verticies+1))

    for v, w in graph.edges:
        non_existant_pairs[v].remove(w)

        
    for a, b in pattern.edges:
        for v, ws in non_existant_pairs.items():
            for w in ws:
                cnf.clauses.append([-((a-1)*graph.number_of_verticies+v),-((b-1)*graph.number_of_verticies+w)])
                cnf.clauses.append([-((a-1)*graph.number_of_verticies+w),-((b-1)*graph.number_of_verticies+v)])

    cnf.number_of_clauses = len(cnf.clauses)
    write_cnf_file(cnf, "what-is-this.cnf")
        

produce_cnf(problemType, pattern_filename, graph_filename)