#!/bin/python3

import sqlite3

class Saver:
    def __init__(self, dbPath):
        if not type(dbPath) is str:
            raise ValueError('dbPath should be string')

        self._dbPath = dbPath
        self._cursor = None
        self._connection = None
        self._Open()
       
    def _Cursor(self):
        self._cursor = self._connection.cursor()

    def _CreateTable(self):
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages 
            (
                id INTEGER NOT NULL PRIMARY KEY,
                message TEXT NOT NULL,
                lifeTime INTEGER NOT NULL
            );
        ''')
    
    def _Commit(self):
        if self._connection:
            self._connection.commit()
    
    def _Open(self):
        if self._connection:
            self._Close()

        try:
            self._connection = sqlite3.connect(self._dbPath)
        except:
            print('error: connect to dataBase')

        self._Cursor()
        self._CreateTable()

    def _Close(self):
        if self._connection:
            self._Commit()
            self._connection.close()
            self._connection, self._cursor = None, None

    def AddRecord(self, message, lifeTime):
        self._cursor.execute('''
        INSERT INTO messages (message, lifeTime) VALUES (?, ?);
        ''', [message, lifeTime])
        self._Commit()
    
    def _ShowTable(self):
        res = self._cursor.execute('''
        SELECT id, message as msg, lifeTime as ltime FROM messages
        ''')
        for row in res:
            print(row)

    def _RemoveDataBase(self):
        pass
