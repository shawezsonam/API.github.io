from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}
products = [{"id": 1, "name": "Laptop", "price": 50000},
            {"id": 2, "name": "Phone", "price": 20000}]
messages = []

@app.route("/")
def home():
    return jsonify({"status": "success", "message": "Universal API Running 🚀"})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    if email in users:
        return jsonify({"status": "error", "message": "User already exists"})
    users[email] = {"name": data.get("name"), "password": data.get("password")}
    return jsonify({"status": "success", "message": "Signup successful"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if email in users and users[email]["password"] == password:
        return jsonify({"status": "success", "message": f"Welcome {users[email]['name']}!"})
    return jsonify({"status": "error", "message": "Invalid credentials"})

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify({"status": "success", "products": products})

@app.route("/message", methods=["POST"])
def send_message():
    data = request.json
    messages.append(data)
    return jsonify({"status": "success", "message": "Message saved", "total_messages": len(messages)})

@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify({"status": "success", "messages": messages})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
