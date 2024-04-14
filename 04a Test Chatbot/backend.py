from flask import Flask, request, jsonify
from response_decode import generate_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route("/generate_response", methods=["POST"])
def generate_response_route():
    user_input = request.json.get("user_input")
    url = request.json.get("url")  # Get the URL from the request
    option = request.json.get("option")  # Get the option from the request

    response = generate_response(user_input, url, option)

    return jsonify({"response": "SmartAssist : " + response})

if __name__ == "__main__":
    app.run(debug=True)
