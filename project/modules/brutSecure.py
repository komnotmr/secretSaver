#!/bin/python3
#~brutSecure.py~
from datetime import datetime, timedelta

class BrutSecure():
    def __init__(self, banTimeMinutes=5, intervalTimeMinutes=1, maxRequests=30):
        self.delayed = datetime.now() - timedelta(weeks=1)
        self.ipTable = {}
        self.deltaTime = timedelta(minutes=intervalTimeMinutes)
        self.limitRequests = maxRequests
        self.banTime = timedelta(minutes=banTimeMinutes)
        self.enabled = False
    
    def _initIP(self):
        return [0, datetime.now()+self.deltaTime, self.delayed]

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
    # ip: string - (request's address)
    def Add(self, ip):
        if not ip in self.ipTable.keys():
            self.ipTable[ip] = self._initIP()
            return True
        return False
    # ip: string - (request's address)
    def isBrut(self, ip):
        if not self.enabled:
            return False
        if not ip in self.ipTable.keys():
            return False
        now = datetime.now()
        if now < self.ipTable[ip][2]:
            return True
        if self.ipTable[ip][0] < self.limitRequests:
            self.ipTable[ip][0] += 1
            return False
        else:
            if now <= self.ipTable[ip][1]:
                self.ipTable[ip][0] = 0
                self.ipTable[ip][1] = now + self.banTime + self.deltaTime
                self.ipTable[ip][2] = now + self.banTime
                print(f'BrutSecure: ban ip addres {ip}, too many requests')
                return True
            else:
                self.ipTable[ip] = self._initIP()
                return False
    
    def ShowIps(self):
        for e in self.ipTable:
            print(f'{e}:{self.ipTable[e][0]},{self.ipTable[e][1]},{self.ipTable[e][2]}')











