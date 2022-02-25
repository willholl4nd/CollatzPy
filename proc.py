import time
from database import Database
from multiprocessing import Pool
from timeit import default_timer as timer 

def t(func):
    def wrapper(*args):
        time1 = time.localtime().tm_gmtoff
        c = func(args[0])
        time2 = time.localtime().tm_gmtoff
        print(f'Time to complete: {time2-time1}, count: {c}')

    return wrapper
        
def div(num):
    count = 0
    tempnum = num 

    while num != 1:
        if(num % 2 == 0):
            num = num / 2
            count += 1
        else:
            num = (num * 3 + 1) / 2
            count += 2

    return tempnum,count

class myProc:

    def __init__(self, start_num, start_count, total_find, database, processes):
        self.start_num = start_num
        self.start_count = start_count
        self.total_find = total_find
        self.database = database
        self.current_find = 0
        self.processes = processes

    def run(self):
        #while(self.current_find <= self.total_find):
        counts_array = []
        num = 1000000
        with Pool(processes=self.processes) as p:
            mapset = [i+self.start_num for i in range(1,num)]
            counts_array = p.map_async(func=div, iterable=mapset)

            counts_array.wait()

        c = sorted(counts_array.get())
        for i in c:
            if(i[1] > self.start_count):
                self.start_count = i[1]
                print(f'found {i[0]} with count {i[1]}')
                self.database.insert(i[0],i[1])
                self.current_find += 1
                self.database.connection.commit()
        self.start_num += num



if __name__ == "__main__":
    d = Database()
    #proc = myProc(d.first, d.count, 10, d)
    proc = myProc(d.first, d.count, 10, d, 10)
    start = timer()
    proc.run()
    end = timer()
    print(f'Took {end-start} seconds')
    d.close()



