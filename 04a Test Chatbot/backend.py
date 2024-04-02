from flask import Flask, request, jsonify
from transformers import T5ForConditionalGeneration, T5Tokenizer
import os

app = Flask(__name__)

root =  r'C:\\Users\\likhi\\Documents\\02 Pycharm Datasets\\01 Master Thesis\\07 QnA\\Saved Models\\'
model = T5ForConditionalGeneration.from_pretrained(os.path.join(root, "trained_t5_model_10_percent_data_epoch_10"))
tokenizer = T5Tokenizer.from_pretrained(os.path.join(root, "trained_t5_model_10_percent_data_epoch_10"))

@app.route("/generate_response", methods=["POST"])
def generate_response():
    user_input = request.json.get("user_input")
    input_ids = tokenizer.encode(user_input, return_tensors="pt", max_length=512, truncation=True)
    output_ids = model.generate(input_ids, max_length=50, num_beams=4, early_stopping=True)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
