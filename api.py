from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "welcome home"

app.run(debug=True)
