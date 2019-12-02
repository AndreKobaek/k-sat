import os
from apxToD import *
#localDir = '../benchmark-data/randomSatUnzip/'
externalDir = '/media/andre/LinUXB/research-project/'
subDir1 = 'agile/'
subDir2 = 'main/'
subDir3 = 'incremental/'
subDir4 = 'random/'
directory = externalDir+subDir2

def check_clause_width():
    maxClause = 0
    entries = os.listdir(directory)
    for entry in entries:
        filename = directory+entry
        f = open(filename, "r")
        clauseWidth = 0
        lines = f.readlines()
        for line in lines:
            if line[0] != "c" and line[0] != "p":
                clauseWidth = max(clauseWidth, len(line.split()))
        maxClause = max(maxClause,clauseWidth)
        print(entry+ ", "+ str(clauseWidth))
    print("maxclause width in dir: "+str(maxClause))

entries = os.listdir(directory)
a = 100
s = 6
for entry in entries:
    filename = directory+entry
    the_algorithm_2(filename,a,s)