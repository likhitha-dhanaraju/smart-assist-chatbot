import sys
sys.dont_write_bytecode = True

from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from utils.amazon_scrapper import amazon_scrapping

import os
import warnings
warnings.filterwarnings("ignore")


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
    if 'amazon.com' in url or 'amazon.co.uk' in url or 'amazon.in' in url or 'amazon.ca' in url:
        scraped_data = amazon_scrapping(url)
        return scraped_data
    else:
        return "NOT AMAZON"

def generate_product_response(user_input, scraped_data):

    context_input = ""
    data_keys = [i.lower() for i in scraped_data.keys()]
    if 'title' in data_keys:
        context_input += "product title is " + scraped_data['Title']
    if 'variant_data' != []:
        for i, item in enumerate(scraped_data['variant_data']):
            context_input += "variant {}".format(i+1) + "is " + scraped_data['variant_data'][i]['product_' + str(i+1)]['name']
    if 'description' in data_keys:
        if type(scraped_data['description']) == list:
            for line in scraped_data['description']:
                context_input += "product description is " + line.strip()
        else:
            context_input += "product description is " + scraped_data['description']

    if 'product_overview' != {}:
        for key, value in scraped_data['product_overview'].items():
            context_input += key + ":" + value

    model_input = f"context: {context_input} question: {user_input} about the product"
    input_ids = qna_tokenizer.encode(model_input, return_tensors="pt", truncation=True)
    output_ids = qna_model.generate(input_ids, max_length=32, num_beams=4, early_stopping=True)
    response = qna_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response


def generate_review_response(scraped_data):

    if scraped_data['reviews'] != []:

        product_data_reviews = ["Title: " + i['header'] + '. Text:' + i['text']
                                for i in scraped_data['reviews']]
        product_data_reviews_text = '. '.join(product_data_reviews)
        model_response = loaded_review_summarizer(product_data_reviews_text, min_length = 50)
        response = model_response[0]['summary_text']
        return response
    else:
        return "There are no customer reviews for this product yet!"

def generate_recommendation_response(user_input, scraped_data):
    model_input = f"context: {scraped_data} question: {user_input} about customized product recommendations"
    input_ids = qna_tokenizer.encode(model_input, return_tensors="pt", truncation=True)
    output_ids = qna_model.generate(input_ids, max_length=64, num_beams=4, early_stopping=True)
    response = qna_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response
