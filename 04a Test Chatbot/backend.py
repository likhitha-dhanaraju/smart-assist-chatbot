from flask import Flask, render_template, request, jsonify
from response_decode import generate_response
from flask_cors import CORS

import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.get("/")
def index_get():
    return render_template("popup.html")

@app.route("/generate_response", methods=["POST"])
def predict():
    text = request.get_json().get("message")
    url = request.get_json().get("url")  # Get the URL from the request
    # TODO: check if text if valid

    response = generate_response(text, url)
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)