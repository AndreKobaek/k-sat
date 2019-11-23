from shutil import copyfile
import os
#path = os.getcwd()
tempFileName = "tester2.txt"
#tempFileName = "inputFile.txt"
checker = True
SATsolver = "./minisat_static"
filename = "testFile.cnf"
output = "output.txt"
term = SATsolver + " " + tempFileName + " " + output + " >> log.txt"

def satisfiable():
    with  open(output, "r") as satResult:    
        resultLines =  satResult.readlines()
    
    if resultLines[0][:3] == "SAT":
        return True
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


def copyInputFile():
    copyfile(filename, tempFileName)

def count_few(maximum_runs: int):
    copyInputFile()
    number_of_fucking_solutions = 0
    for _ in range(3):
        os.system(term)
        if satisfiable():
            addInvertedClause()
            number_of_fucking_solutions += 1
        else:
            break
    return number_of_fucking_solutions

# def has_variables TODO