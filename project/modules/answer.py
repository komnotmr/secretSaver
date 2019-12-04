#!/bin/python3
# ~answer.py~
class Answer:
    def __init__(self):
        self.__data = ''
        self.__errors = []

    def setData(self, data):
        if not data:
            raise ValueError('data should be String')
        self.__data = data
    
    def addError(self, errTxt):
        if not errTxt:
            raise ValueError('errTxt should be String')
        self.__errors.append(errTxt)

    def clearErrors(self):
        self.__errors = []
    
    def clearData(self):
        self.__data = ''

    def clear(self):
        self.clearData()
        self.clearErrors()

    def isOk(self):
        return len(self.__errors) == 0
    
    def getAnswer(self):
        return {
            "data": self.__data,
            "errors": self.__errors
        }