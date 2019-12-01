#!/bin/python3

import sqlite3 #sqlite provider
import uuid #generation unique id
import re # regular expressions

tableName = 'messages'
scripts = {
    "createTable": f'''
            CREATE TABLE IF NOT EXISTS {tableName} (
                id INTEGER NOT NULL PRIMARY KEY ,
                code VARCHAR(256) NOT NULL,
                message TEXT NOT NULL,
                lifeTime INTEGER NOT NULL
            ) ;
    ''',
    "addRecord": f'''
        INSERT INTO {tableName} (message, code, lifeTime) VALUES (?, ?, ?) ;
    ''',
    "selectAll": f'''
        SELECT * FROM {tableName} ;
    ''',
    "dropTable": f'''
        DROP TABLE IF EXISTS {tableName} ;
    ''',
    "getRecord": f'''
        SELECT * FROM {tableName}
        WHERE code = ?;
    '''
}
# sqlite default returns tuple
# for return dict use dict_factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Saver:
    # dbPath: text - path to database file
    def __init__(self, dbPath):
        # check args
        if not type(dbPath) is str:
            raise TypeError('dbPath should be string')

        self._gen = uuid
        self._cursor = None
        self._dbPath = dbPath
        self._connection = None

        self._Open()
   
    def _GenID(self):
        return str(self._gen.uuid4())

    # creating cursor
    def _Cursor(self):
        self._cursor = self._connection.cursor()
    # commiting changes 
    def Commit(self):
        if self._connection:
            self._connection.commit()
    # open connection
    def _Open(self):
        # close if already opened
        if self._connection:
            self._Close()
        # try connection 
        try:
            self._connection = sqlite3.connect(self._dbPath, check_same_thread = False)
            self._connection.row_factory = dict_factory
        except:
            print('error: connect to dataBase')
        # creating cursor and creating table if not exists
        self._Cursor()
        self._CreateTable()
    # closing connection
    def _Close(self):
        if self._connection:
            self.Commit()
            self._connection.close()
            self._connection, self._cursor = None, None
    # on dispose instance closing connection with commit
    def __del__(self):
        self._Close()
    
    def _CreateTable(self):
        self._cursor.execute(scripts["createTable"])

    def _DropTable(self):
        self._cursor.execute(scripts["dropTable"])

    def addRecord(self, message, lifeTime):
        try:
            if not self._cursor:
                self._Cursor()
            id = self._GenID()
            self._cursor.execute(scripts["addRecord"], [message, id, lifeTime])
            return id
        except:
            print('error: add record to table')
            return None

    def isCode(self, code):
        pttrn = re.compile('^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$')
        return pttrn.match(code)

    def getRecord(self, code):
        try:
            if not self._cursor:
                self._Cursor()
            res = self._cursor.execute(scripts["getRecord"], [code])
            return res
        except:
            print('error: get record from table')
            return None
    
    def _ShowTable(self):
        res = self._cursor.execute(scripts["selectAll"])
        for row in res:
            print(row)