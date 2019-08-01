from flask import Flask, request
import sys
import os

app = Flask(__name__)

app.config['store'] = sys.argv[1]
store = app.config.get('store')

@app.route('/')
def index():
    return "welcome home"

@app.route('/files/create', methods=['POST'])
def create():
    data = request.get_json()
    name, contents = data['name'], data['contents']

    f = open(store+'/'+name, "w")
    f.write(contents)
    f.close()

    return "File '{}' created at '{}'.".format(name, store), 201

@app.route('/files/read')
def list():
    files = os.listdir(store)

    if len(files) == 0:
        return "No files found in {}".format(store)

    return '\n'.join(sorted(files))

@app.route('/files/read/<filename>')
def read(filename):
    f = open(store+'/'+filename, "r")
    contents = f.read()
    f.close()

    return contents

@app.route('/files/update/<filename>', methods=['PUT'])
def update(filename):
    data = request.get_json()
    contents = data['contents']

    f = open(store+'/'+filename, "w")
    f.write(contents)
    f.close()

    return "File '{}' in '{}' updated.".format(filename, store)

@app.route('/files/delete/<filename>', methods=['DELETE'])
def delete(filename):
    os.remove(store+'/'+filename)
    return "File '{}' deleted from '{}'.".format(filename, store)

app.run(debug=True)
