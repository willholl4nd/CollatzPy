import os
import sys
import time

vals = {}

def store(func):
    global vals
    def wrapper(*args):
        #time1 = time.localtime()
        #if(args[0] == 1):
            #break
        if(not args[0] in vals.keys()):
            vals[args[0]] = func(args[0])

        return vals[args[0]]
        #time2 = time.localtime()
    return wrapper

@store
def collatz(num):
    count = 0
    while num != 1:
        if num % 2 == 1:
            num = num * 3 + 1
        else:
            num = num / 2

        count += 1
        collatz(int(num))

    return int(count)

sys.setrecursionlimit(10000)
#for i in range(1, 100000000):
for i in range(1, 10):
    collatz(i)

#collatz(670617279)

#Sorted by key
sorted_dict = sorted(vals.items(), key= lambda a: a[0])

#Sorted by value
sorted_dict2 = sorted(vals.items(), key= lambda a: a[1])

print(sorted_dict)
print(sorted_dict2)
