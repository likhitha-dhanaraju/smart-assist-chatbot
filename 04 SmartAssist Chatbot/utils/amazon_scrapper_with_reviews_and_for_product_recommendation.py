import requests
from lxml import html
from bs4 import BeautifulSoup
import re

## Removed the media code in this file

def get_breadcrumbs_text(response):
    breadcrumbs_str_list = []
    breadcrumbs_text_list = response.xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]//li//text()')
    for breadcrumbs_text in breadcrumbs_text_list:
        if breadcrumbs_text.strip() and len(breadcrumbs_text.strip()) > 2:
            breadcrumbs_str_list.append(cleanhtml(breadcrumbs_text.strip()))

    return breadcrumbs_str_list


def cleanhtml(raw_html):
    html = cleanhtml_1(raw_html)
    soup = BeautifulSoup(html, features="lxml")
    text = soup.get_text()
    text = text.replace("\xa0", " ")
    text = text.replace("\n", "")
    return text


def cleanhtml_1(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext


def get_product_details_upper(response):
    description_text_json = {}
    for res in response.xpath('//*[@id="productFactsDesktopExpander"]/div[1]/div'):
        header = res.xpath('div/div[1]/span/span/text()')[0]
        p_text = res.xpath('div/div[2]/span/span/text()')[0]
        description_text_json[cleanhtml(header)] = cleanhtml(p_text)

    return description_text_json


def get_features_list(response):
    features_list = []
    for feat_text in response.xpath('//*[@id="productFactsDesktopExpander"]/div[1]/ul/span/li/span/text()'):
        if feat_text.strip() and len(feat_text) > 1:
            features_list.append(cleanhtml(feat_text).encode("ascii", "ignore").decode())
    print("DESCRIPTION", features_list)
    return features_list


def get_attribute_extraction(response):
    attribute_text_json = {}

    attribute_texts = response.xpath('//*[@id="detailBullets_feature_div"]/ul/li/span/span/text()')
    attribute_texts = [" ".join(attribute_text.encode("ascii", "ignore").decode().replace("\n","").split())
                       for attribute_text in attribute_texts if len(attribute_text.strip()) >= 2]

    for index in range(0, len(attribute_texts), 2):
        try:
            attribute_text_json[str(attribute_texts[index])] = attribute_texts[index + 1]
        except:
            pass
    return attribute_text_json


def get_bullet_feature(response):
    bullet_feats = []
    for bullet_feat_text in response.xpath('//*[@id="feature-bullets"]//li//text()'):
        if bullet_feat_text.strip():
            bullet_feats.append(bullet_feat_text.encode("ascii", "ignore").decode().replace('"', "'"))
    return bullet_feats

def table_features_list(response):
    features_json = {}
    features_text_list = response.xpath('//*[@id="productOverview_feature_div"]//tr/td//text()')
    features_text_list = [feat_text for feat_text in features_text_list if feat_text.strip()]

    for index in range(0, len(features_text_list), 2):
        try:
            features_json[cleanhtml(features_text_list[index])] = cleanhtml(features_text_list[index + 1])
        except:
            pass
    return features_json


def get_review_extraction(response):
    review_data = []
    reviews = response.xpath('.//div[@class="a-section celwidget"]')

    for review in reviews:
        try:
            text = "".join([i.strip() for i in review.xpath('.//span[@data-hook="review-body"]//text()')]).replace("\n",
                                                                                                                   "")
            header = review.xpath('.//a[@data-hook="review-title"]//span[2]//text()')

            if type(header) == list:
                header = header[0]

            review_data.append({"header": header,
                                "text": text
                                })

        except Exception as e:
            continue

    return review_data



def main(url, proxies, headers):

    r = requests.get(url)
    response = html.fromstring(r.content)

    url = r.url.strip().split("/ref=")[0]
    pv_item = {"url": url}
    try:
        pv_item["Title"] = response.xpath('//*[@id="productTitle"]//text()')[0].strip()
    except:
        title_texts = response.xpath('//*[@id="title"]//text()')
        pv_item["Title"] = " ".join([title_txt for title_txt in title_texts if title_txt.strip()])


    pv_item["sku"] = pv_item['url'].split('/dp/')[-1].strip()
    pv_item["categories"] = get_breadcrumbs_text(response)

    if get_features_list(response) != []:
        pv_item["description"] = get_features_list(response)
    else:
        pv_item["description"] = get_bullet_feature(response)

    pv_item["reviews"] = get_review_extraction(response)
    pv_item['product_overview'] = table_features_list(response)

    product_details_json = get_product_details_upper(response)
    product_details_json.update(get_attribute_extraction(response))
    pv_item['product_details'] = product_details_json

    return pv_item


def amazon_scrapping_for_prod_recom(url, proxies, headers):

    product_data = main(url, proxies, headers)

    return product_data

#
# import random
# from fake_useragent import UserAgent
#
# def get_proxies():
#     ua = UserAgent()
#     headers = {'User-Agent': ua.random}
#     url = 'https://free-proxy-list.net/'
#
#     r = requests.get(url, headers=headers)
#     page = BeautifulSoup(r.text, 'html.parser')
#
#     proxies = []
#
#     for proxy in page.find_all('tr'):
#         i = ip = port = 0
#
#         for data in proxy.find_all('td'):
#             if i == 0:
#                 ip = data.get_text()
#             if i == 1:
#                 port = data.get_text()
#             i += 1
#
#         if ip != 0 and port != 0 and '.' in ip:
#             proxies += [{'http': 'http://' + ip + ':' + port}]
#
#     return proxies
#
#
# ua = UserAgent()
#
#
# def get_random_headers():
#     headers = {
#         'authority': 'www.amazon.com',
#         'pragma': 'no-cache',
#         'cache-control': 'no-cache',
#         'dnt': '1',
#         'Connection': 'keep-alive',
#         'upgrade-insecure-requests': '1',
#         'user-agent': ua.random,
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'sec-fetch-site': 'none',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-dest': 'document',
#         'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     }
#
#     return headers
#
# proxies_list = get_proxies()
# proxies = random.choice(proxies_list)
# headers = get_random_headers()
#
# print(amazon_scrapping_for_prod_recom('https://www.amazon.com/Surround-Headphones-Cancelling-Flexible-Earmuffs/dp/B09TB15CTL',
#                                       proxies=proxies, headers=headers))