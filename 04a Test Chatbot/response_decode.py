from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import json
import os

root = r'C:\\Users\\likhi\\Documents\\02 Pycharm Datasets\\01 Master Thesis\\07 QnA\\Saved Models\\'
qna_model = T5ForConditionalGeneration.from_pretrained(os.path.join(root, "trained_t5_model_10_percent_data_epoch_10"))
qna_tokenizer = T5Tokenizer.from_pretrained(os.path.join(root, "trained_t5_model_10_percent_data_epoch_10"))

# Load the model from the saved directory
output_dir = r"C:\Users\likhi\Documents\02 Pycharm Datasets\01 Master Thesis\08 Review Data\Saved Models"

review_model = AutoModelForSeq2SeqLM.from_pretrained(os.path.join(output_dir, 'Review Summarisation'))
review_tokenizer = AutoTokenizer.from_pretrained(os.path.join(output_dir, 'Review Summarisation'))

# Create a new pipeline with the loaded model
loaded_review_summarizer = pipeline("summarization", model=review_model, tokenizer=review_tokenizer)


def scrape_data_from_url(url):
    # Implement scraping logic here
    # This is just a placeholder function
    # Replace it with your actual scraping code

    scraped_data = "Product title is Perler Beads Assorted Multicolor Fuse Beads for Kids Crafts, 11000 pcs. Product overview is Color is Multicolor Material is Plastic Size is 11,000 Count Brand is Perler Shape is Round Item Weight is 1.69 Pounds Number of Pieces is 11000. Product description is Includes (11000) assorted Perler fuse beads and reusable ironing paper in plastic storage jar. This mega set of 11,000 Perler fuse beads comes with 30 different colors, including toothpaste, pastel lavender, butterscotch, and neon pink. Use your assorted Perler fuse beads with pre-made Perler bead design or get creative and make your own. These multicolor Perler beads are great arts and crafts activity for children. Use Perler pegboards, ironing paper, and an iron to complete your craft. Multicolor Perler beads set suitable for ages and up."
    return scraped_data

def generate_product_response(user_input, scraped_data):
    model_input = f"context: {scraped_data} question: {user_input} about the product"
    input_ids = qna_tokenizer.encode(model_input, return_tensors="pt", truncation=True)
    output_ids = qna_model.generate(input_ids, max_length=64, num_beams=4, early_stopping=True)
    response = qna_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response


def generate_review_response(product_data_reviews_text):
    model_response = loaded_review_summarizer(product_data_reviews_text, min_length = 50)
    response = model_response[0]['summary_text']

    return response


def generate_recommendation_response(user_input, scraped_data):
    model_input = f"context: {scraped_data} question: {user_input} about customized product recommendations"
    input_ids = qna_tokenizer.encode(model_input, return_tensors="pt", truncation=True)
    output_ids = qna_model.generate(input_ids, max_length=64, num_beams=4, early_stopping=True)
    response = qna_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response


def generate_response(url):
    global response

    print("Let's chat! (type 'quit' to exit)")

    print("Bot: Select one of the options - Ask about Product, Ask about customer reviews or Ask about customized Product reviews. Select Main Menu to go back")

    while True:
        main_option = input("You: ")

        scraped_data = scrape_data_from_url(url)

        if main_option == "Ask about the product":
            print("Bot: Please ask your questions!")
            while True:
                user_input = input("You: ")
                if user_input == 'Main Menu':
                    break
                response = generate_product_response(user_input, scraped_data)
                print("Bot:", response)

        elif main_option == "Ask about customer reviews":
            product_file_path = r"C:\Users\likhi\Documents\02 Pycharm Datasets\01 Master Thesis\04 Product Data\Women's Fashion_Clothing\Product_B0B6412QWW\Product_B0B6412QWW.json"

            product_data = json.load(open(product_file_path, 'r'))
            product_data_reviews = ["Title: " + i['header'] + '. Text:' + i['text']
                                    for i in product_data['reviews']]
            product_data_reviews_text = '. '.join(product_data_reviews)
            response = generate_review_response(product_data_reviews_text)
            print("Bot:", response)

        elif main_option == "Ask about customized Product reviews":
            while True:
                user_input = input("You: ")
                if user_input == 'Main Menu':
                    break
                response = generate_recommendation_response(user_input, scraped_data)
                print("Bot:", response)

        elif main_option == 'quit':
            break

        else:
            response = 'Bot: No response'


generate_response('test')