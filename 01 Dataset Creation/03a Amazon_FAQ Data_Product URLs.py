import os
from tqdm import tqdm
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

base_url = "https://www.amazon.com/ask/questions/asin/"

product_dir = r"C:/Users/likhi/Documents/02 Pycharm Datasets/01 Master Thesis/04 Product Data/"
destination_dir = r"C:/Users/likhi/Documents/02 Pycharm Datasets/01 Master Thesis/07 QnA/"

products_list = []

for category in tqdm(os.listdir(product_dir)):
    category_path = os.path.join(product_dir, category)
    for product in os.listdir(category_path)[:100]:
        product_name = product.strip().split('Product_')[-1]
        products_list.append(base_url+product_name)

products_list = list(set(products_list))

products_list_df = pd.DataFrame(products_list, columns=['urls'])
products_list_df.to_csv(destination_dir + 'products_qna_amazon_urls.csv', index=False)
