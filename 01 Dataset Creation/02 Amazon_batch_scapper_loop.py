import os.path

from utils.Amazon_batch_scrapper import amazon_batch_scrapping

url_folder = '02a Product Urls_to COLAB'

print(os.path.exists(url_folder))

while(True):
    try:
        amazon_batch_scrapping(url_folder)
    except:
        continue
