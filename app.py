from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/hello/<name>")
def hello(name):
    return jsonify({"message": f"Hello, {name}! 👋"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
