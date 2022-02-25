import time
import mariadb

def t(func):
    def wrapper(*args):
        time1 = time.localtime().tm_gmtoff
        c = func(args[0])
        time2 = time.localtime().tm_gmtoff
        print(f'Time to complete: {time2-time1}, count: {c}')

    return wrapper
        
    
class Database:

    def getfirst(self):
        self.cursor.execute("select count(*) as count from collatzpy")
        row = self.cursor.fetchone()
        if(row[0] == 0):
            self.first = 1
            self.count = 0
            return

        self.cursor.execute("select * from collatzpy order by value desc")
        row = self.cursor.fetchone()
        self.first = row[0]
        self.count = row[1]
        
    def insert(self, num, count):
        try:
            self.cursor.execute("insert into collatzpy (value, count) values (?, ?)", (num,count))
        except mariadb.Error as e:
            print(f'Error inserting: {e}')

    def close(self):
        self.connection.close()


    def __init__(self):
        self.connection = mariadb.connect(user="root", 
                password="asdf1234", host="localhost", database="collatz")
        self.cursor = self.connection.cursor()
        self.getfirst()



