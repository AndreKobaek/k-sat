from shutil import copyfile
import copy
import math
import os
import sys
#path = os.getcwd()
#tempFileName = "tester2.txt"
tempFileName = "inputFile.txt"
checker = True
SATsolver = "./minisat_static"
#filename = "testFile.cnf"
output = "output.txt"
query_solver = SATsolver + " " + tempFileName + " " + output + " >/dev/null"

def satisfiable():
    with  open(output, "r") as satResult:    
        resultLines =  satResult.readlines()
    if resultLines[0][:3] == "SAT":
        return True
    return False
class OutOfRunsException(Exception):
    pass
class CNF:
    pass

def read_cnf_file(filename: str):
    with open(filename,"r") as cnfFile:
        lines = cnfFile.readlines()
    cnf = CNF()
    cnf.clauses = list(list())
    for line in lines:
        if line[0] != "c":
            if line[0] == "p":
                metadata = line.split()
                cnf.number_of_literals = int(metadata[2])
                cnf.number_of_clauses = int(metadata[3])
            else:
                if len(line.split())!= 0:
                    cnf.clauses.append([int(x) for x in line.split()[:-1]])
    return cnf

def write_cnf_file(cnf: CNF, filename: str):
    metadata = "p cnf {} {}\n".format(cnf.number_of_literals,cnf.number_of_clauses)
    clauses = ""
    for clause in cnf.clauses:
        clauses += " ".join([str(x) for x in clause] + ["0\n"])
    with open(filename,"w") as cnfFile:
        print(metadata + clauses.rstrip(), file=cnfFile)

def remove_or_subtract(clause: list):
    return_list = []
    for literal in clause:
        if abs(literal) != 1:
            return_list += [int(math.copysign(abs(literal)-1,literal))]
    return return_list

def set_var(cnf: CNF, var: int):
    reduced_cnf = CNF()
    reduced_cnf.clauses = list(list())
    for clause in cnf.clauses:
        if var not in clause:
            reduced_cnf.clauses.append(remove_or_subtract(clause))
    reduced_cnf.number_of_literals = cnf.number_of_literals - 1
    # max(max(max(reduced_cnf.clauses,[-sys.maxsize-1])),abs(min(min(reduced_cnf.clauses,[sys.maxsize]))))
    reduced_cnf.number_of_clauses = len(reduced_cnf.clauses)
    return reduced_cnf

def copyInputFile(filename:str, tempFile:str):
    copyfile(filename, tempFileName)

copyInputFile("simpleCNF.txt", tempFileName)

def count_few_branching(F: CNF, maximum_runs:int):
    write_cnf_file(F,tempFileName)
    os.system(query_solver)
    if satisfiable():
        F = read_cnf_file(tempFileName)
        if F.number_of_literals != 0:
            number_of_solutions = count_few_branching(set_var(F,  1), maximum_runs) + count_few_branching(set_var(F, -1), maximum_runs)
            if number_of_solutions <= maximum_runs:
                return number_of_solutions
            raise OutOfRunsException("FAIL")
        else:
            return 1
    else:
        return 0




def set_up_branching(filename: str, a: int):
    copyInputFile(filename,tempFileName)
    F = read_cnf_file(tempFileName)
    return count_few_branching(F, a)

# try:
#     print(set_up_branching("simpleCNF.txt",sys.maxsize))
# except OutOfRunsException:
#     print("FAIL")

def count_few(cnfFile: str, maximum_runs: int):
    tempFileName = cnfFile
    copyInputFile()
    number_of_solutions = 0
    for _ in range(maximum_runs):
        os.system(query_solver)
        if satisfiable():
            addInvertedClause()
            number_of_solutions += 1
        else:
            return number_of_solutions
    return False

def addInvertedClause():
    with  open(output, "r") as satResult:    
        resultLines =  satResult.readlines()
    
    with open(tempFileName) as fileInput:
        inputLines = fileInput.readlines()

    clauses = ""
    for line in inputLines:
        if line[:1] != "p":
            clauses += line
        else:
            lineElems = line.split()
            clauses += " ".join(lineElems[:3] + [str(int(lineElems[3]) + 1), "\n"])
    appendClause = ""
    for n in resultLines[1].split():
        appendClause = "{} {} ".format(appendClause,-int(n))
    with open(tempFileName, "w") as newInputFile:
        print(clauses + appendClause, file=newInputFile)