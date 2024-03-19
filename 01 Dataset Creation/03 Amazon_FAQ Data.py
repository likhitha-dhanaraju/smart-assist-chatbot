import os
from tqdm import tqdm
import json
from selenium import webdriver
import time
from utils.Amazon_captcha_solver_v2 import custom_Amazon_captcha_solver
from selenium.webdriver.common.by import By

import warnings
warnings.filterwarnings("ignore")

base_url = "https://www.amazon.com/ask/questions/asin/"
product_dir = r"C:/Users/likhi/Documents/02 Pycharm Datasets/01 Master Thesis/04 Product Data/"
destination_dir = r"C:/Users/likhi/Documents/02 Pycharm Datasets/01 Master Thesis/07 QnA/QnA Limit 100"

if not os.path.exists(destination_dir):
    os.mkdir(destination_dir)

product_limit = 100


category_products_list = {}

for category in tqdm(os.listdir(product_dir)):
    products = []
    category_path = os.path.join(product_dir, category)
    for product in sorted(os.listdir(category_path))[:product_limit]:
        product_name = product.strip().split('Product_')[-1]
        products.append(product_name)
    products = list(set(products))
    category_products_list[category] = products


print('Setting up the Amazon website....')

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument("--incognito")
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)

## Testing with Amazon Home Page URL to enter CAPTCHA to avoid looking like a robot

custom_Amazon_captcha_solver(driver, driver_close=False)

try:
    driver.maximize_window()
except:
    print("Window already maximised")

print("Finished setting up after Captcha")

QnA_data = {}

print("Extracting QnA data...")

for category in category_products_list.keys():

    print(category)
    QnA_data = {}
    for i, product_name in enumerate(tqdm(category_products_list[category])):

        if i % 50 == 0 and i!= 0:
            driver.close()
            driver = webdriver.Chrome(options=options)

            custom_Amazon_captcha_solver(driver, driver_close=False)

            with open(os.path.join(destination_dir, category + '_Amazon QnA_data.json'), 'w') as f:
                json.dump(QnA_data, f)
                f.close()

        url = base_url + product_name

        driver.get(url)
        time.sleep(1)

        num_of_qna = len(driver.find_elements(By.XPATH, '//*[@class="a-section askTeaserQuestions"]/div'))

        if num_of_qna > 0:

            try:
                # Find all question-answer pairs
                question_answer_pairs = []

                for qa_div in range(num_of_qna):
                    question = driver.find_element(By.XPATH, '//*[@class="a-section askTeaserQuestions"]/div[' + str(
                        qa_div + 1) + ']/div/div[2]/div[1]/div/div[2]/a/span').text
                    answer = driver.find_element(By.XPATH,
                                                 '//*[@class="a-section askTeaserQuestions"]/div[' + str(
                                                     qa_div + 1) + ']/div/div[2]/div[2]/div/div[2]/span[1]').text
                    question_answer_pairs.append([question, answer])

                QnA_data[product_name] = question_answer_pairs
            except:

                pass

driver.close()

print("Finished extracing QnA data for all products!")
