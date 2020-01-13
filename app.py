#!flask/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"


# describe the data available in an existing dataset
@app.route('/describe')
def describe():
    return ""

# query an existing dataset
@app.route('/q')
def describe():
    return ""

@app.route('/prepare')
def prepare():
    return ""

# Upload a new dataset (api)
@app.route('/register')
def register():
    return ""

if __name__ == '__main__':
    app.run(debug=True)
