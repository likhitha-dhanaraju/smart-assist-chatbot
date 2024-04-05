from flask import Flask, request, jsonify
from transformers import T5ForConditionalGeneration, T5Tokenizer
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
root = r'C:\\Users\\likhi\\Documents\\02 Pycharm Datasets\\01 Master Thesis\\07 QnA\\Saved Models\\'
model = T5ForConditionalGeneration.from_pretrained(os.path.join(root, "trained_t5_model_10_percent_data_epoch_10"))
tokenizer = T5Tokenizer.from_pretrained(os.path.join(root, "trained_t5_model_10_percent_data_epoch_10"))


def scrape_data_from_url(url):
    # Implement scraping logic here
    # This is just a placeholder function
    # Replace it with your actual scraping code

    scraped_data = "Product title is Perler Beads Assorted Multicolor Fuse Beads for Kids Crafts, 11000 pcs. Product overview is Color is Multicolor Material is Plastic Size is 11,000 Count Brand is Perler Shape is Round Item Weight is 1.69 Pounds Number of Pieces is 11000. Product description is Includes (11000) assorted Perler fuse beads and reusable ironing paper in plastic storage jar. This mega set of 11,000 Perler fuse beads comes with 30 different colors, including toothpaste, pastel lavender, butterscotch, and neon pink. Use your assorted Perler fuse beads with pre-made Perler bead design or get creative and make your own. These multicolor Perler beads are great arts and crafts activity for children. Use Perler pegboards, ironing paper, and an iron to complete your craft. Multicolor Perler beads set suitable for ages and up."
    return scraped_data


def generate_product_response(user_input, url):
    model_input = f"context: {scrape_data_from_url(url)} question: {user_input} about the product"
    input_ids = tokenizer.encode(model_input, return_tensors="pt", truncation=True)
    output_ids = model.generate(input_ids, max_length=64, num_beams=4, early_stopping=True)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response


def generate_review_response(user_input, url):
    model_input = f"context: {scrape_data_from_url(url)} question: {user_input} about customer reviews"
    input_ids = tokenizer.encode(model_input, return_tensors="pt", truncation=True)
    output_ids = model.generate(input_ids, max_length=64, num_beams=4, early_stopping=True)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response


def generate_recommendation_response(user_input, url):
    model_input = f"context: {scrape_data_from_url(url)} question: {user_input} about customized product recommendations"
    input_ids = tokenizer.encode(model_input, return_tensors="pt", truncation=True)
    output_ids = model.generate(input_ids, max_length=64, num_beams=4, early_stopping=True)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response


def generate_response(user_input, url):
    model_input = f"context: {scrape_data_from_url(url)} question: {user_input}"
    input_ids = tokenizer.encode(model_input, return_tensors="pt", truncation=True)
    output_ids = model.generate(input_ids, max_length=64, num_beams=4, early_stopping=True)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response


@app.route("/generate_response", methods=["POST"])
def generate_response_route():
    user_input = request.json.get("user_input")
    url = request.json.get("url")  # Get the URL from the request
    option = request.json.get("option")  # Get the option from the request

    if option == "Ask about the product":
        response = generate_product_response(user_input, url)
    elif option == "Ask about customer reviews":
        response = generate_review_response(user_input, url)
    elif option == "Ask about customized product recommendations":
        response = generate_recommendation_response(user_input, url)
    else:
        response = "Please select one of the options"

    return jsonify({"response": "SmartAssist : " + response})


if __name__ == "__main__":
    app.run(debug=True)
