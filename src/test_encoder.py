from sys import argv
from count_exact import count_exact_ganak, count_exact_file
from count_homomorphism import count_hom
from encode_in_cnf import produce_cnf

input_dir = "input/graphs/"
pattern_inputs = ["cycle5.gr", "cycle7.gr", "k3.gr"]
graph_inputs = ["paley-101.gr"] #, "jazzmusicians.gr"]

def test_encoder(pattern_file: str, graph_file: str) -> bool:
    correct_result = count_hom(pattern_file, graph_file)
    cnf_file_name = produce_cnf("--hom", pattern_file, graph_file)
    result_ganak = count_exact_ganak(cnf_file_name)
    result_sharpSAT = count_exact_file(cnf_file_name)[0]
    print("file: {}, corr:{}, Ganak:{}, sharpS:{}".format(cnf_file_name, correct_result, result_ganak, result_sharpSAT))
    return correct_result == result_ganak or correct_result == result_sharpSAT

for pattern in pattern_inputs:
    for graph in graph_inputs:
        print(test_encoder(input_dir+pattern, input_dir+graph))
