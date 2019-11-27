import numpy as np
import random

s = 6 #two times clausewidth perhaps.
n = 5

def generate_row_direct(n: int, s: int):
    entries = list(range(1,n+1))
    random.shuffle(entries)
    return [x for x in entries[:s] if random.randint(0,1)]

def zero_to_minus(a: int):
    if a == 0:
        return -1
    return a

def generate_clauses(row: list(), b: int):
    clauses = list(list())
    for i in range(2**len(row)):
        stringFormat = "{0:0"+str(len(row))+"b}"
        bin = [int(b) for b in stringFormat.format(i)]
        if (sum(bin)%2 == b) and sum(bin)>0:
            bin = [zero_to_minus(x) for x in bin]
            clauses.append([ a*b for (a,b) in zip(bin,row)])
    return clauses

print(generate_clauses([10,20,30,40,50], 0))

def b_column_vector(row_length: int):
    np.random.randint(2, size=n).transpose()

#b = hashing_matrix(5, n)
#a = 
#print(b)
# print(a)
# for i in range(n):
#     c = list(filter(lambda x: x>0, b[i][:]))
#     print(c)
#     print(a[i])
# c = list(range(n))
# d = list([-1,1,-1,1,1])
# e = [x*y for x,y in zip(c,d)]
# print(e)

#b = np.array(list(range(1,n+1))).transpose()
#print(a)
#print(a[1,1])

def generate_row(n: int):
    one_entries = list(range(n))
    random.shuffle(one_entries)
    input_to_alter = one_entries[:s]
    return_row = [0]*n
    for i in input_to_alter:
        if random.randint(0,1)==1:
            return_row[i] = i+1
    return return_row

def hashing_matrix(rows: int, columns: int):
    A = np.array(generate_row(columns))
    for i in range(rows-1):
        A = np.vstack([A,np.array(generate_row(columns))])
    return A