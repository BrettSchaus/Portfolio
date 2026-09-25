import requests
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

load_dotenv()

app = Flask(__name__)

USERNAME = "brettschaus"
YOUR_ACCESS_KEY = os.getenv("MARKETSTACK_API_KEY")

MARKETSTACK_ENDPOINT = "https://api.apilayer.net/marketstack/v2/eod"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/stock")
def get_stock():
    user_params = {"access_key": YOUR_ACCESS_KEY, "symbols": "AAPL",}

    response = requests.get(MARKETSTACK_ENDPOINT, params=user_params)
    data = response.json()
    latest_data = data["data"][0]
    return jsonify({
        "symbol": latest_data["symbol"],
        "price": latest_data["close"]
    })


if __name__ == "__main__":
    app.run(debug=True)




