#!/bin/python3

from saver import Saver

def main():
    s = Saver('test.db')
    s._ShowTable()
    s.AddRecord('msg1', '124124532')
    s.AddRecord('msg2', '234429499')
    s._Commit()
    s._ShowTable()

main()