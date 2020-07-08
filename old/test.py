import time
def test():
    a = 0
    for i in range(1000):
        for k in range(i,1000):
            for j in range(k, 1000):
                a += i + k + j


def timeFunc():
    start = time.process_time()
    test()
    end = time.process_time()
    print("{0:.2f}, {1}".format((end-start), "yes"))

from datetime import datetime
# dd/mm/YY H:M:S
#dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)	

from new import filename
print(filename)
