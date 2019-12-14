from countFew import *


def write_cnf_file(F: CNF, filename: str):
    metadata = "p cnf {} {}\n".format(
        F.number_of_literals, F.number_of_clauses)
    clauses = ""
    for clause in F.clauses:
        clauses += " ".join([str(x) for x in clause] + ["0"+os.linesep])
    with open(filename, "w") as cnfFile:
        print(metadata + clauses.rstrip(), file=cnfFile)

def add_inverted_clause(F: CNF):
    with open(output, "r") as satResult:
        resultLines = satResult.readlines()

    F.clauses.append([-int(x) for x in resultLines[1].split()[:-1]])
    F.number_of_clauses += 1

def count_few(F: CNF, maximum_runs: int = sys.maxsize):
    number_of_solutions = 0
    for _ in range(maximum_runs):
        write_cnf_file_2(F, tempFileName)
        os.system(query_solver)
        if satisfiable():
            add_inverted_clause(F)
            number_of_solutions += 1
        else:
            return number_of_solutions
    return False


def set_up_naive(filename: str, a: int = sys.maxsize):
    copyInputFile(filename, tempFileName)
    F = read_cnf_file(tempFileName)
    return count_few(F, a)


def add_inverted_clause2():
    with open(output, "r") as satResult:
        resultLines = satResult.readlines()

    with open(tempFileName) as fileInput:
        inputLines = fileInput.readlines()

    clauses = ""
    for line in inputLines:
        if line[:1] != "p":
            clauses += line
        else:
            lineElems = line.split()
            clauses += " ".join(lineElems[:3] +
                                [str(int(lineElems[3]) + 1), "\n"])
    appendClause = ""
    for n in resultLines[1].split():
        appendClause = "{} {} ".format(appendClause, -int(n))
    with open(tempFileName, "w") as newInputFile:
        print(clauses + appendClause, file=newInputFile)

