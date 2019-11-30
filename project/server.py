#!/bin/python3
from flask import Flask, request, render_template
from saver import Saver

app = Flask(__name__)
s = Saver('test.db')

@app.route('/', methods=['GET', 'POST'])
def indexGet():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        answer = {
            "data": '',
            "errors": []
        }
        if not request.form['data']:
            answer["errors"].append('Input string is empty')
        if not request.form['lifeTime']:
            answer["errors"].append('life time not chosen')
        if len(answer["errors"]) > 0:
            return answer
        data, ltime = request.form['data'], request.form['lifeTime']
        print(f'server get data: {data}, ltime: {ltime}')
        saveMessage(answer, data, ltime)
        return answer    

def saveMessage(answer, msg, ltime):
    res = s.AddRecord(msg, ltime)
    if res is None:
        answer["errors"].append('internal error, try again later')
    else:
        answer["data"] = res

if __name__ == '__main__':
    app.run(debug=True)
