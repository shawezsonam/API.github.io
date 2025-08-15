from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "🚀 Flask NSE Proxy API is running!"})

@app.route("/price/<symbol>")
def price(symbol):
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol.upper()}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        price_info = data.get("priceInfo", {})
        return jsonify({
            "symbol": symbol.upper(),
            "lastPrice": price_info.get("lastPrice"),
            "change": price_info.get("change"),
            "percentChange": price_info.get("pChange")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
