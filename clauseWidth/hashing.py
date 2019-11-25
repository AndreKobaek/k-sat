import numpy as np
import random

s = 2
n = 5

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
b = hashing_matrix(5, n)
a = np.random.randint(2, size=n).transpose()
#b = np.array(list(range(1,n+1))).transpose()
print(a)
#print(a[1,1])