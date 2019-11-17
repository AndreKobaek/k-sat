import os
externalDir = '/media/andre/LinUXB/research-project/'
#localDir = '../benchmark-data/randomSatUnzip/'
subDir1 = 'agile/'
subDir2 = 'main/'
subDir3 = 'incremental/'
subDir4 = 'random/'
directory = externalDir+subDir2
entries = os.listdir(directory)

maxClause = 0
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