from flask import Flask, escape, request
import os

app = Flask(__name__)
port = int(os.getenv('PORT', 3000))

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

app.run(host='0.0.0.0', port=port)