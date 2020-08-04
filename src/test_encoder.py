from sys import argv

from count_exact import count_hom_ganak, count_hom_sharp
from count_homomorphism import count_hom
from encode_in_cnf import produce_cnf

input_dir = "input/graphs/"
pattern_inputs = ["cycle5.gr", "cycle7.gr", "k3.gr"]
graph_inputs = ["paley-101.gr"]  # , "jazzmusicians.gr"]


def test_encoder(pattern_file: str, graph_file: str) -> bool:
    correct_result = count_hom(pattern_file, graph_file)
    cnf_file_name = produce_cnf("--emb", pattern_file, graph_file)
    result_ganak = count_hom_ganak(cnf_file_name)
    result_sharpSAT = count_hom_sharp(cnf_file_name)
    print("file:{},homSub:{},Ganak:{},sharpS:{}".format(cnf_file_name, correct_result, result_ganak, result_sharpSAT))


for pattern in pattern_inputs:
    for graph in graph_inputs:
        print(test_encoder(input_dir + pattern, input_dir + graph))
