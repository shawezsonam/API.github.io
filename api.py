from flask import Flask, jsonify, request

app = Flask(__name__)
SECRET_KEY = "Shawez123"  # API ko lock karne ke liye key

@app.route('/')
def home():
    return jsonify({"message": "✅ Shawez Bhai ki API chal rahi hai!"})

@app.route('/api/calc')
def calc():
    key = request.args.get('key')
    if key != SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 403
    a = request.args.get('a', default=0, type=int)
    b = request.args.get('b', default=0, type=int)
    return jsonify({"result": a + b})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
