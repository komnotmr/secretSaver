#!/bin/python3

from saver import Saver
from hashlib import blake2b

def main():
    path = './test.db'
    n = 10000
    print ('Dropping table')
    s = Saver(path)
    s._ShowTable()
    #s._DropTable()
    #s._Commit()
    #print ('Initing table')
    #s = Saver(path)
    #print ('Generation data')
    #for i in range(n):
    #    s.AddRecord(f'str{i}', f'message{n-i}')
    #print ('Commiting changes')
    #s._Commit()
    #print ('Result:')
    #s._ShowTable()

main()