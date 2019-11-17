import sys
clauseWidth = 0

for line in sys.stdin:
    if line[0] != "c" and line[0] != "p":
        intline = line.split()
        n = len(intline)
        clauseWidth = max(clauseWidth,(n-1))

print(clauseWidth)

