import numpy as np 
from timeit import default_timer as timer
from numba import vectorize
from database import Database

def format(a):
    format_string = ''
    l = str(a)
    if len(l) > 3:
        for i in range(len(l)-1,-1,-1):
            format_string = l[i] + format_string
            if (len(l)-i) % 3 == 0:
                format_string = ',' + format_string
        return format_string
    else:
        return l

class GPU_collatz:
    def __init__(self, number_blocks, database, total_count):
        self.number_blocks = number_blocks
        self.database = database
        self.total_count = total_count
        self.start_int = d.first+1
        self.end_int = d.first+number_blocks
        self.best_count = d.count


    def run(self):
        cur_count = 0
        while cur_count < self.total_count:
            o = [i for i in range(self.start_int, self.end_int)]
            a = np.array(o, dtype='uint64')
            b = vector_collatz(a)

            for k,v in np.ndenumerate(b):
                if v > self.best_count:
                    cur_count += 1 
                    print(f'{format(a[k])}, {format(v)}')
                    self.database.insert(int(a[k]),int(v))
                    self.best_count = v
                    self.database.connection.commit()
            self.start_int += self.number_blocks
            self.end_int += self.number_blocks
            print(f'{format(self.start_int)}')


@vectorize(["uint64(uint64)"],target='cuda')
def vector_collatz(a):
    count = 0
    while a != 1:
        if a % 2 == 0:
            a = a / 2 
            count += 1
        else: 
            a = (a * 3 + 1) / 2
            count += 2
    return count

def collatz(a):
    count = 0
    while a != 1:
        if a % 2 == 0:
            a = a / 2 
            count += 1
        else: 
            a = (a * 3 + 1) / 2
            count += 2
    return count


if __name__ == "__main__":
    d = Database()

    G = GPU_collatz(300000000, d, 4)
    G.run()

    '''
    start = timer()
    b = [collatz(i) for i in o]
    end = timer()

    print(f"Took {end-start} seconds")'''
    d.close()

