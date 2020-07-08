from os import getcwd
from sys import argv

from cnf_generator import generate_cnf
from cnf_io import write_cnf_file
from count_exact import count_exact_file

number_of_literals = int(argv[1])
number_of_clauses = int(argv[2])
clause_width = int(argv[3])
job_number = int(argv[4])

F = generate_cnf(number_of_literals, clause_width, number_of_clauses)
filename = "cnf-gen-L{}-W{}-C{}-J{}.cnf".format(F.number_of_literals, 3, F.number_of_clauses, job_number)
location = getcwd()
write_filename = "{}/generated-input/{}".format(location, filename)
write_cnf_file(F, write_filename)

output_file = "{}/input/output-{}.txt".format(location, job_number)

exact_solutions = count_exact_file(write_filename, output_file)

result_file = "{}/experiment-find-cnf/{}.csv".format(location, job_number)
result_text = "{},{},{},{},{},{},{}".format(
    filename,
    exact_solutions[0],
    exact_solutions[1],
    number_of_clauses,
    F.number_of_literals,
    clause_width,
    job_number,
)
with open(result_file, "w") as result:
    result.write(result_text)
