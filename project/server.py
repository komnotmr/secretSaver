#!/bin/python3
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def indexGet():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        return saveMessage()

def saveMessage():
    return 'asdsad'



if __name__ == '__main__':
    app.run(debug=True)
