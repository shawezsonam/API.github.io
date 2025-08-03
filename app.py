from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Users Database
users = {}

# Products Database
products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Phone", "price": 20000}
]

# Messages Database
messages = []

# ✅ Home Route
@app.route("/")
def home():
    return jsonify({"status": "success", "message": "Universal API Running 🚀"})

# ✅ Signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    if email in users:
        return jsonify({"status": "error", "message": "User already exists"})
    users[email] = {"name": data.get("name"), "password": data.get("password")}
    return jsonify({"status": "success", "message": "Signup successful"})

# ✅ Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if email in users and users[email]["password"] == password:
        return jsonify({"status": "success", "message": f"Welcome {users[email]['name']}!"})
    return jsonify({"status": "error", "message": "Invalid credentials"})

# ✅ Products
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify({"status": "success", "products": products})

# ✅ Send Message
@app.route("/message", methods=["POST"])
def send_message():
    data = request.json
    messages.append(data)
    return jsonify({"status": "success", "message": "Message saved", "total_messages": len(messages)})

# ✅ Get Messages
@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify({"status": "success", "messages": messages})

# ✅ Stocks (NEW AUTO ADDED ENDPOINT)
@app.route("/stocks", methods=["GET"])
def get_stocks():
    stocks_data = [
        {"symbol": "RELIANCE", "price": 2450, "change": 12.5, "volume": "1.5M"},
        {"symbol": "TCS", "price": 3520, "change": -5.2, "volume": "2.3M"},
        {"symbol": "HDFC", "price": 1650, "change": 8.3, "volume": "1.8M"}
    ]
    return jsonify(stocks_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
