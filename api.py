from flask import Flask, request
import sys

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


app.run(debug=True)
