from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/hello/<name>")
def hello(name):
    return jsonify({"message": f"Hello, {name}! 👋"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
