import sys
sys.dont_write_bytecode = True

from flask import Flask, request
from model_responses import *
from flask_cors import CORS

import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)  # Allow requests from your extension

@app.route("/scrape_data", methods=["POST"])
def scrape_data():
    global scraped_data
    url = request.get_json().get("url")
    scraped_data = scrape_data_from_url(url)
    return {'data': scraped_data}


@app.route("/product", methods=["POST"])
def product():
    text = request.get_json().get("user_input")
    response = generate_product_response(text, scraped_data)
    return {'data': response}


@app.route("/review", methods=["POST"])
def review():
    response = generate_review_response(scraped_data)
    return {'data': response}


@app.route("/recommendation", methods=["POST"])
def product_recommendation():
    user_input = request.get_json().get("user_input")
    response_df = generate_recommendation_response(user_input, scraped_data)
    return response_df.to_json(orient='records')

if __name__ == "__main__":
    app.run(debug=True)
