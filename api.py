from flask import Flask, request
import sys
import os

app = Flask(__name__)

def process_configuration():
    app.config['store'] = sys.argv[1]
    store = app.config.get('store')

    if not os.path.isdir(store):
        sys.exit("The provided store configuration (`{}`) is not an existing directory.".format(store))

    return store

@app.route('/')
def index():
    return "welcome home"

@app.route('/files/create', methods=['POST'])
def create():
    data = request.get_json()
    name, contents = data['name'], data['contents']

    full_path = store+'/'+name
    if not os.path.exists(full_path):
        write_file(full_path, contents)
        return "File '{}' created at '{}'.".format(name, store), 201
    else:
        return "File '{}' already exists in '{}'.".format(name, store), 409

@app.route('/files/read')
def list():
    files = os.listdir(store)

    if len(files) == 0:
        return "No files found in {}".format(store)

    return '\n'.join(sorted(files))

@app.route('/files/read/<filename>')
def read(filename):
    full_path = store+'/'+filename
    if os.path.exists(full_path):
        f = open(store+'/'+filename, "r")
        contents = f.read()
        f.close()
        return contents
    else:
        return "File '{}' not found in '{}'.".format(filename, store), 404

@app.route('/files/update/<filename>', methods=['PUT'])
def update(filename):
    data = request.get_json()
    contents = data['contents']

    full_path = store+'/'+filename
    if os.path.exists(full_path):
        write_file(full_path, contents)
        return "File '{}' in '{}' updated.".format(filename, store)
    else:
        return "File '{}' not found in '{}'.".format(filename, store), 404

@app.route('/files/delete/<filename>', methods=['DELETE'])
def delete(filename):
    full_path = store+'/'+filename
    if os.path.exists(full_path):
        os.remove(full_path)
        return "File '{}' deleted from '{}'.".format(filename, store)
    else:
        return "File '{}' not found in '{}'.".format(filename, store), 404

def write_file(filename, contents):
    f = open(filename, "w")
    f.write(contents)
    f.close()

store = process_configuration()
app.run(debug=True)
