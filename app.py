from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Home route
@app.route("/")
def home():
    return jsonify({"message": "🚀 Flask API chal rahi hai Bhai!"})

# Hello API
@app.route("/hello/<name>")
def hello(name):
    return jsonify({"message": f"Hello, {name}! 👋"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
