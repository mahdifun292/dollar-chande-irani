from flask import Flask, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

TGJU_URL = "https://www.tgju.org/profile/price_dollar_rl"


def get_dollar_price():

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/140.0 Safari/537.36"
        )
    }

    response = requests.get(
        TGJU_URL,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    element = soup.select_one(".price")

    if not element:
        raise Exception(
            "Dollar price element not found"
        )

    price = element.get_text(
        strip=True
    )

    return price


@app.route("/")
def home():

    return send_from_directory(
        ".",
        "index.html"
    )


@app.route("/api/dollar")
def dollar():

    try:

        price = get_dollar_price()

        return jsonify({
            "success": True,
            "price": price
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
