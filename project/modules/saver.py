#!/bin/python3
#~saver.py~
import sqlite3 
import uuid 
import re # regular expressions

from datetime import datetime, timedelta
from sqlite3 import DatabaseError
from threading import Thread

import time

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
    ''',
    "removeOldRecords": f'''
        DELETE FROM {tableName}
        WHERE lifeTime < strftime('%s','now');
    '''
}

# sqlite default returns tuple
# for return dictonary use dict_factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Saver:
    # dbPath: text - path to database file
    def __init__(self, dbPath, removeIntervalMinutes=30):
        # check args
        if not type(dbPath) is str:
            raise TypeError('dbPath should be string')
        self._pttrn = re.compile('^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$')
        self._initTime = datetime.now()
        self._gen = uuid
        self._cursor = None
        self._dbPath = dbPath
        self._connection = None
        self._Open()
        self._intervalSchedule = timedelta(minutes=removeIntervalMinutes)
        self._scheduleThread = Thread(target=self._scheduleRemover)
        self._scheduleThread.daemon = True
        self.startSchedule()

    def startSchedule(self):
        self._scheduleThread.start()

    def _scheduleRemover(self):
        while True:
            time.sleep(5)
            now = datetime.now()
            if now > self._initTime + self._intervalSchedule:
                print('Saver: removing old records')
                self.removeOldRecords()
                self._initTime = now

    def _GenID(self):
        return str(self._gen.uuid4())

    def _Cursor(self):
        self._cursor = self._connection.cursor()

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
        except DatabaseError:
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
        self._query("createTable")

    def _DropTable(self):
        self._query("dropTable")

    def _query(self, methodName, *args):
        if not methodName:
            raise ValueError('methodName should be String')
        res = None
        try:
            if not self._cursor:
                self._Cursor()
            res = self._cursor.execute(scripts[methodName], args)
        except DatabaseError as err:
            print(f'query error:', err)
        except Exception as exc:
            print(f'query error:', exc)
        else:
            self.Commit()
            return res
        return None

    def _addRecord(self, message, lifeTime):
        id = self._GenID()
        self._query("addRecord", message, id, lifeTime)
        return id

    def isCode(self, code):
        return self._pttrn.match(code)

    def getRecord(self, code):
        return self._query("getRecord", code)

    def removeOldRecords(self):
        self._query("removeOldRecords")
        
    def showTable(self):
        for row in self._query("selectAll"):
            print(row)