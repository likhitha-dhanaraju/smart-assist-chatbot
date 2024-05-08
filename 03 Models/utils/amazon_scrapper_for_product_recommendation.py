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


def main(url, proxies, headers):

    r = requests.get(url, headers=headers, proxies=proxies)
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

    pv_item['product_overview'] = table_features_list(response)

    product_details_json = get_product_details_upper(response)
    product_details_json.update(get_attribute_extraction(response))
    pv_item['product_details'] = product_details_json

    return pv_item


def amazon_scrapping(url, proxies, headers):

    product_data = main(url, proxies, headers)

    return product_data
