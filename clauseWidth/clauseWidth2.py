import os
#localDir = '../benchmark-data/randomSatUnzip/'
externalDir = '/media/andre/LinUXB/research-project/'
subDir = ['main/', 'incremental/', 'random/']


def check_clause_width(directory: str):
    maxClause = 0
    entries = os.listdir(directory)
    for entry in entries:
        filename = directory+entry
        with open(filename, "r") as f:
            lines = f.readlines()

        clauseWidth, literals, clauses = 0, 0, 0
        for line in lines:
            if line[0] != "c" and line[0] != "p": 
                clauseWidth = max(clauseWidth, len(line.split())-1)
            if line[0] == "p":
                metadata = line.split()
                literals = metadata[2]
                clauses = metadata[3]
        maxClause = max(maxClause,clauseWidth)
        print("{}, {}, {}, {}".format(entry, literals, clauses, maxClause))

print("filename, literals, clauses, width")
for subD in subDir:
    check_clause_width(externalDir+subD)