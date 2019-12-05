#!/bin/python3
#~server.py~
from flask import Flask, request, render_template
from modules.brutSecure import BrutSecure
from modules.answer import Answer
from modules.saver import Saver

app = Flask(__name__)
dbSaver = Saver('./test.db', removeIntervalMinutes=1)
brutSecure = BrutSecure()
brutSecure.enable()

@app.route('/', methods=['GET', 'POST'])
def indexGet():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        a = Answer()
        if not brutSecure.Add(request.remote_addr):
            if brutSecure.isBrut(request.remote_addr):
                a.addError(f"banned for a {brutSecure.banTime.seconds} seconds")
                return a.getAnswer()

        if not request.form.get('data'):
            a.addError('empty request')
            return a.getAnswer()

        if setAnswer(request.form, a):
            print ('valid data')
        else:
            print ('invalid data')

        return a.getAnswer()

def setAnswer(req, a):
    if not req.get('data'):
        a.addError('Input string is empty')
    elif dbSaver.isCode(req['data']):
        res = dbSaver.getRecord(req['data'])
        for r in res:
            a.setData(r['message'])
    elif not req.get('lifeTime'):
        a.addError('life time not chosen')
    else:
        a.setData(dbSaver._addRecord(req['data'], req['lifeTime']))
    return a.isOk()
  
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)