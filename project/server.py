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
        print(f'server get data: {request.form}')
        if not request.form:
            print ('empty request')
            answer["errors"].append('empty request')
            return answer
        if proccessInput(request.form, answer):
            print ('valid data')
        else:
            print ('invalid data')
            for e in answer['errors']:
                print(e)
        return answer    

def proccessInput(req, answer):
    # check message or code
    if not req['data']:
        answer["errors"].append('Input string is empty')
    elif s.isCode(req['data']):
        res = s.getRecord(req['data'])
        for r in res:
            answer['data'] = r['message']
        # else it just message and we check lifeTime
    elif not req['lifeTime']:
        answer["errors"].append('life time not chosen')
    else:
        answer['data'] = s.addRecord(req['data'], req['lifeTime'])
    return len(answer["errors"]) > 0
  
if __name__ == '__main__':
    app.run(debug=True)
