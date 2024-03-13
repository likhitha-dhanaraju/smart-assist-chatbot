from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import os
from tqdm import tqdm
import pandas as pd
import requests
from utils.Amazon_captcha_solver_v2 import custom_Amazon_captcha_solver

## First 3 URLs have to be redone ( they were done for Low-to_high sorting )

class UrlsList():

    def __init__(self, url):
        self.url = url
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument("--incognito")
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=options)

        ## Testing with Amazon Home Page URL to enter CAPTHA to avoid looking like a robot

        custom_Amazon_captcha_solver(self.driver, driver_close=False)

        time.sleep(5)

        self.driver.get(url)


        try:
            self.driver.maximize_window()
        except:
            print("Window already maximised")

        self.page_count = 400
        self.total_count = 24 * int(self.page_count)

        print("page count: ", self.page_count, "and total_count: ", self.total_count)

        ## Limiting the page count to test the code
        # self.page_count = 2

    def list_of_products(self, folder, filename):

        SCROLL_TIME = 5
        end_length = 3000

        urls_list = []
        prev_url_list = []
        prev_url_list_len = 0
        urls_list_counter = 0
        print("Adding URLs to list")

        for page_number in tqdm(range(1, self.page_count+1)):
            self.driver.execute_script("window.scrollTo(0," + str(end_length) + ")")
            time.sleep(SCROLL_TIME)
            print("\n")

            try:

                url_xpath_main = '//*[@data-cy="title-recipe"]/h2/a'
                contents = self.driver.find_elements(By.XPATH, url_xpath_main)
                # print("MAIN", contents)
                for content in contents:
                    _url_ = content.get_attribute('href')

                    r = requests.get(_url_)
                    original_url = r.url
                    shortened_url = original_url.strip().split('/ref=')[0]
                    if not shortened_url == "https://www.amazon.com/errors/500":
                        print("TRY MAIN: Page number", page_number, ", REQUESTS", shortened_url)

                        urls_list.append(shortened_url)
                        f = open(os.path.join(folder, "temp_" + filename + '.txt'), 'a+')
                        f.write(shortened_url + '\n')
                        f.close()
            except:
                continue

            urls_list = list(set(urls_list))
            prev_url_list = list(set(prev_url_list))

            print("Previous List Length: ", prev_url_list_len)
            print("Current list Length: ", len(urls_list))

            if len(urls_list) >= 1000:
                break

            if prev_url_list_len == len(urls_list) and prev_url_list == urls_list:
                urls_list_counter += 1

                if urls_list_counter > 10:
                    print('Ending the pagination since the products are same for more than 5 pages')
                    break

            prev_url_list = urls_list
            prev_url_list_len = len(urls_list)

            try:

                next_button_class = 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'
                next_button_xpath = "//a[@class='" + next_button_class + "']"
                next_button = self.driver.find_element(By.XPATH,next_button_xpath)
                next_button.click()

                ## Removing the reference from previous page in URL

                updated_category_url = self.driver.current_url.strip().split("&ref=sr_pg")[0]
                self.driver.get(updated_category_url)

                time.sleep(10)
            except:
                break

        print("FINAL URLS LIST LENGTH: ", len(urls_list))

        if len(urls_list) > 0:
            urls_list_df = pd.DataFrame(urls_list, columns=['urls'])
            urls_list_df.to_csv(os.path.join(folder, "FINAL_" + filename + '.csv'), index=False)

        self.driver.close()


if not os.path.exists("02 Product Urls"):
    os.mkdir("02 Product Urls")

data = pd.read_excel("Amazon Categories Links_Colab_v2.xlsx")
data_length = len(data)

for idx in tqdm(range(data_length)):
    print("\n")

    category = data['Category'].iloc[idx]
    sub_category = data['Sub-Category'].iloc[idx]
    url = data['New Link'].iloc[idx]

    file_name = category + "_" + sub_category

    print("Category: ", category)
    print("    Sub-Category: ", sub_category)

    if not os.path.exists(os.path.join("02 Product Urls", "FINAL_" + file_name + '.csv')) and not os.path.exists(os.path.join("02a Product Urls_to COLAB", "FINAL_" + file_name + '.csv')):

        UrlsList(url).list_of_products("02 Product Urls", file_name)
    else:
        print("Skipping the category since the FINAL file exists already!")
