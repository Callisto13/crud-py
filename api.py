from flask import Flask, request
from handlers import Handlers
import os
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return """
Actions:

POST /files/create
    data: name, contents
    description: create a file with desired contents

GET /files/read
    data: none
    description: read all files stored by the service

GET /files/read/<filename>
    data: none
    description: read a named file

PUT /files/update/<filename>
    data: contents
    description: update a named file

DELETE /files/delete/<filename>
    data: none
    description: delete a named file

    """

@app.route('/files/create', methods=['POST'])
def create():
    data = request.get_json()
    return handlers.create(data['name'], data['contents'])

@app.route('/files/read')
def list():
    return handlers.list()

@app.route('/files/read/<filename>')
def read(filename):
    return handlers.read(filename)

@app.route('/files/update/<filename>', methods=['PUT'])
def update(filename):
    data = request.get_json()
    return handlers.update(filename, data['contents'])

@app.route('/files/delete/<filename>', methods=['DELETE'])
def delete(filename):
    return handlers.delete(filename)


def process_configuration():
    app.config['store'] = sys.argv[1]
    store = app.config.get('store')
    if not os.path.isdir(store):
        sys.exit("The provided store configuration (`{}`) is not an existing directory.".format(store))
    return store

store = process_configuration()
handlers = Handlers(store)
app.run(debug=True)
