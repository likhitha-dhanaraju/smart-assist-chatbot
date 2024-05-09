import sys
sys.dont_write_bytecode = True

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from utils.amazon_scrapper_for_product_recommendation import amazon_scrapping_for_prod_recom

import os
import re
import warnings
import requests
import random
import time
import pandas as pd

warnings.filterwarnings("ignore")


root = r'C:\\Users\\likhi\\Documents\\02 Pycharm Datasets\\01 Master Thesis\\07 QnA\\Saved Models\\Version 6 - 7\\'
qna_model = T5ForConditionalGeneration.from_pretrained(os.path.join(root, "trained_t5_model_first_10_percent_data_shuffled_epoch 5"))
qna_tokenizer = T5Tokenizer.from_pretrained(os.path.join(root, "trained_t5_model_first_10_percent_data_shuffled_epoch 5"))

# Load the model from the saved directory
output_dir = r"C:\Users\likhi\Documents\02 Pycharm Datasets\01 Master Thesis\08 Review Data\Saved Models"
review_model = AutoModelForSeq2SeqLM.from_pretrained(os.path.join(output_dir, 'Review Summarisation'))
review_tokenizer = AutoTokenizer.from_pretrained(os.path.join(output_dir, 'Review Summarisation'))
# Create a new pipeline with the loaded model
loaded_review_summarizer = pipeline("summarization", model=review_model, tokenizer=review_tokenizer)

cosine_similarity_model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')  #'msmarco-distilbert-base-v4'


def get_proxies():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    url = 'https://free-proxy-list.net/'

    r = requests.get(url, headers=headers)
    page = BeautifulSoup(r.text, 'html.parser')

    proxies = []

    for proxy in page.find_all('tr'):
        i = ip = port = 0

        for data in proxy.find_all('td'):
            if i == 0:
                ip = data.get_text()
            if i == 1:
                port = data.get_text()
            i += 1

        if ip != 0 and port != 0 and '.' in ip:
            proxies += [{'http': 'http://' + ip + ':' + port}]

    return proxies


ua = UserAgent()


def get_random_headers():
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'Connection': 'keep-alive',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.random,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    return headers


def scrape_data_from_url(url):

    proxies_list = get_proxies()
    proxies = random.choice(proxies_list)
    headers = get_random_headers()

    cleaned_url = requests.get(url, proxies=proxies, headers=headers, timeout=10).url
    print(cleaned_url)
    if 'amazon.com' in url or 'amazon.co.uk' in url or 'amazon.in' in url or 'amazon.ca' in url:
        scraped_data = amazon_scrapping_for_prod_recom(cleaned_url, proxies=proxies, headers=headers)
        return scraped_data
    else:
        return "NOT AMAZON"

def generate_product_response(user_input, scraped_data):

    context_input = ""
    data_keys = [i.lower() for i in scraped_data.keys()]
    if 'title' in data_keys:
        context_input += "product title is " + scraped_data['Title']
    # if 'variant_data' != []:
    #     for i, item in enumerate(scraped_data['variant_data']):
    #         context_input += "variant {}".format(i+1) + "is " + scraped_data['variant_data'][i]['product_' + str(i+1)]['name']
    if 'description' in data_keys:
        if type(scraped_data['description']) == list:
            for line in scraped_data['description']:
                context_input += "product description is " + line.strip()
        else:
            context_input += "product description is " + scraped_data['description']

    if 'product_overview' != {}:
        for key, value in scraped_data['product_overview'].items():
            context_input += key + ":" + value + ". "


    # Tokenize input text
    inputs = qna_tokenizer(user_input, context_input, padding="max_length", truncation=True,
                       max_length=512, add_special_tokens=True)
    input_ids = torch.tensor(inputs["input_ids"], dtype=torch.long).unsqueeze(0)
    attention_mask = torch.tensor(inputs["attention_mask"], dtype=torch.long).unsqueeze(0)

    # Generate answer
    with torch.no_grad():
        output = qna_model.generate(input_ids=input_ids, attention_mask=attention_mask)  # Adjust max_length as needed
        response = qna_tokenizer.decode(output.flatten(), skip_special_tokens=True)
        # response = response.replace("See more is", "")

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


def product_data_for_recommendation(product_data, similarity_score_column_required):
    product_data_overview = product_data['product_overview']
    product_data_overview_text = ". ".join([key + " is " + value
                                            for key, value in product_data_overview.items()])
    if type(product_data['description']) == list:
        product_description_text = ". ".join(product_data['description'])
    else:
        product_description_text = product_data['description']

    product_data_title = product_data['Title']
    product_data_url = product_data['url']

    final_product_text_for_similarity = product_data_overview_text + ". " + product_description_text

    if similarity_score_column_required:
        final_product_data = {'product_name': product_data_title.strip(),
                              'product_overview': final_product_text_for_similarity.strip(),
                              'product_link': product_data_url,
                              'product_image_link': product_data['image_link'],
                              'similarity_score': 0}
    else:
        final_product_data = {'product_name': product_data_title.strip(),
                              'product_overview': final_product_text_for_similarity.strip(),
                              'product_link': product_data_url}

    return final_product_data


def search(phrase, product_title):
    proxies_list = get_proxies()
    proxies = random.choice(proxies_list)
    headers = get_random_headers()

    phrase = phrase + " as " + product_title
    phrase = re.sub(r'[^a-zA-Z0-9]', ' ', phrase)
    phrase = re.sub(' ', '+', phrase)

    url_amazon = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'.format(phrase)
    print(url_amazon)

    try:
        source_code = requests.get(url_amazon, headers=headers, proxies=proxies, timeout=10)
        # If response status code is 503, wait for a while and retry
        if source_code.status_code == 503:
            print("503 Error. Retrying after 5 seconds...")
            time.sleep(5)
            return search(phrase, product_title)
        source_code.raise_for_status()  # Raise an error for any other HTTP status codes
    except Exception as e:
        print("Error occurred:", e)
        return None

    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    all_product_links = soup.find_all('a',
                                      {
                                          "class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
    all_image_links = soup.find_all('img', {"class": "s-image"})

    similar_products_df = pd.DataFrame(columns=['product_name', 'product_overview',
                                                'product_link', 'product_image_link',
                                                'similarity_score'])
    counter = 0
    counter_limit = 3

    for link, image_link in zip(all_product_links, all_image_links):
        product_link = "https://www.amazon.com" + link['href']

        try:
            proxies = random.choice(proxies_list)
            headers = get_random_headers()
            product_image_url = image_link['src']

            if not 'www.amazon.comhttps' in product_link:
                product_data = amazon_scrapping_for_prod_recom(product_link, proxies, headers)
                product_data['image_link'] = product_image_url
                print(product_image_url)
                final_product_data = product_data_for_recommendation(product_data,
                                                                     similarity_score_column_required=True)

                if len(final_product_data['product_overview']) > 1:
                    similar_products_df = pd.concat([similar_products_df, pd.DataFrame([final_product_data])], axis=0)
                    counter += 1
                    if counter >= counter_limit:
                        break

        except ConnectionError:
            break


    similar_products_df.reset_index(inplace=True, drop=True)

    return similar_products_df


def similarity_scores(similar_products_df, current_product_data):
    base_text = cosine_similarity_model.encode(current_product_data['product_overview'])

    for i in range(1, len(similar_products_df)):
        text_1 = cosine_similarity_model.encode(similar_products_df.iloc[i]['product_overview'])
        score = cosine_similarity([text_1], [base_text])[0][0]
        similar_products_df.loc[i, 'similarity_score'] = score

    sorted_similar_products_df = similar_products_df.sort_values('similarity_score',
                                                                 ascending=False).reset_index(drop=True)
    return sorted_similar_products_df


def generate_recommendation_response(user_input, scraped_data):
    current_product_data = product_data_for_recommendation(scraped_data, similarity_score_column_required=False)
    similar_products_df = search(user_input, current_product_data['product_name'])
    sorted_similar_products_df = similarity_scores(similar_products_df, current_product_data)

    print(sorted_similar_products_df)

    return sorted_similar_products_df
