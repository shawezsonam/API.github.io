from flask import Flask, jsonify
from flask_cors import CORS
import requests, random, threading, time, os, csv
from datetime import datetime
from kiteconnect import KiteConnect, KiteTicker
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# --------------------------
# 🔹 Zerodha Credentials
# --------------------------
API_KEY = "YOUR_API_KEY"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

# --------------------------
# 🔹 Stock Symbols
# --------------------------
STOCK_SYMBOLS = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK"]
stocks = {sym: {"price": random.uniform(1000, 3000), "change": 0, "volume": f"{random.randint(1,10)}M"} for sym in STOCK_SYMBOLS}

# Live ticks storage
live_ticks = {}
token_map = {}

# --------------------------
# 📌 Download & Parse Instruments
# --------------------------
INSTRUMENT_FILE = "instruments_nse.csv"

def load_instruments():
    global token_map
    if not os.path.exists(INSTRUMENT_FILE):
        print("📥 Downloading instruments list from Zerodha...")
        url = "https://api.kite.trade/instruments"
        resp = requests.get(url)
        with open(INSTRUMENT_FILE, "wb") as f:
            f.write(resp.content)
    # Parse CSV
    with open(INSTRUMENT_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tradingsymbol = row["tradingsymbol"].strip().upper()
            if row["exchange"] == "NSE":
                token_map[tradingsymbol] = int(row["instrument_token"])
    print(f"✅ Loaded {len(token_map)} NSE instruments.")

load_instruments()

# --------------------------
# 📌 Yahoo Finance Fallback Stocks
# --------------------------
@app.route("/stocks")
def get_stocks():
    result = []
    try:
        qs = ",".join([f"{sym}.NS" for sym in STOCK_SYMBOLS])
        resp = requests.get(f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={qs}", timeout=2)
        data = resp.json().get("quoteResponse", {}).get("result", [])
        if data:
            for item in data:
                sym = item.get("symbol", "").split(".")[0]
                result.append({
                    "symbol": sym,
                    "price": round(item.get("regularMarketPrice", 0), 2),
                    "change": round(item.get("regularMarketChangePercent", 0), 2),
                    "volume": f"{int(item.get('regularMarketVolume',0)/1000000)}M"
                })
            return jsonify(result)
    except:
        pass

    for sym in STOCK_SYMBOLS:
        delta = round(random.uniform(-25, 25), 2)
        stocks[sym]["price"] = round(stocks[sym]["price"] + delta, 2)
        stocks[sym]["change"] = delta
        result.append({"symbol": sym, **stocks[sym]})
    return jsonify(result)

# --------------------------
# 📌 NSE Indices (Nifty, BankNifty, Sensex)
# --------------------------
@app.route("/indices")
def indices():
    indices_data = {
        "NIFTY50": "^NSEI",
        "BANKNIFTY": "^NSEBANK",
        "SENSEX": "^BSESN"
    }
    result = []
    try:
        qs = ",".join(indices_data.values())
        resp = requests.get(f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={qs}", timeout=2)
        data = resp.json().get("quoteResponse", {}).get("result", [])
        for item in data:
            name = item.get("shortName", item.get("symbol"))
            price = round(item.get("regularMarketPrice", 0), 2)
            change = round(item.get("regularMarketChangePercent", 0), 2)
            result.append({"index": name, "price": price, "change": change})
        if result:
            return jsonify(result)
    except:
        pass

    # fallback simulated data
    for name in indices_data.keys():
        result.append({"index": name, "price": round(random.uniform(30000, 200000), 2), "change": round(random.uniform(-1, 1), 2)})
    return jsonify(result)

# --------------------------
# 📌 Zerodha Quote
# --------------------------
@app.route("/zerodha-quote/<symbol>")
def zerodha_quote(symbol):
    try:
        quote = kite.quote(exchange="NSE", tradingsymbol=symbol.upper())
        data = quote.get("NSE:" + symbol.upper(), {})
        return jsonify({
            "symbol": symbol.upper(),
            "last_price": data.get("last_price"),
            "ohlc": data.get("ohlc"),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --------------------------
# 📌 Zerodha WebSocket Streaming
# --------------------------
def start_websocket():
    kws = KiteTicker(API_KEY, ACCESS_TOKEN)

    def on_ticks(ws, ticks):
        for tick in ticks:
            token = tick['instrument_token']
            live_ticks[token] = {
                "last_price": tick['last_price'],
                "volume": tick.get('volume', 0),
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }

    def on_connect(ws, response):
        print("✅ Zerodha WebSocket Connected")
        tokens = []
        for sym in STOCK_SYMBOLS:
            token = token_map.get(sym.upper())
            if token:
                tokens.append(token)
        print("🔹 Subscribing tokens:", tokens)
        ws.subscribe(tokens)
        ws.set_mode(ws.MODE_LTP, tokens)

    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.connect(threaded=True)

threading.Thread(target=start_websocket, daemon=True).start()

@app.route("/zerodha-stream")
def zerodha_stream():
    return jsonify({"live_data": live_ticks})

# --------------------------
# 📌 Live Market News (Moneycontrol scraping)
# --------------------------
@app.route("/news")
def market_news():
    result = []
    try:
        resp = requests.get("https://www.moneycontrol.com/news/business/markets/", timeout=3)
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("div.listing-news a")[:5]
        for a in cards:
            headline = a.get_text(strip=True)
            link = a.get("href")
            result.append({"headline": headline, "url": link})
        if result:
            return jsonify({"source": "live", "news": result})
    except Exception as e:
        print("Scraping failed:", e)

    # fallback static headlines
    fallback = [
        {"headline": "Reliance surges on earnings beat", "url": ""},
        {"headline": "TCS Q1 revenue up 12% YoY", "url": ""},
        {"headline": "Sensex up 300 pts amid global rally", "url": ""}
    ]
    return jsonify({"source": "fallback", "news": fallback})

# --------------------------
@app.route("/")
def home():
    return jsonify({"message": "🚀 Indian Stock Combo API Ready with Zerodha Live Stream, Indices & News"})

# --------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
