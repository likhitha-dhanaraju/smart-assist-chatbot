import requests
import json
from lxml import html
from bs4 import BeautifulSoup
import re


def modify_url(url):
    url = url.strip()
    if url.startswith('/'):
        modify_url = "https://www.amazon.in" + url
    elif url.startswith('//'):
        modify_url = "https:" + url
    else:
        modify_url = url
    return modify_url


def get_product_details(response):
    product_detail_json = {}
    for product_detail in response.xpath('//*[@id="detailBullets_feature_div"]//li'):
        try:
            key = product_detail.xpath('span[1]/span[1]/text()')[0].strip().split('\n')[0].strip()
            value = product_detail.xpath('span[1]/span[2]/text()')[0].strip()
            product_detail_json[key] = value
        except:
            pass

    return product_detail_json


def get_media(response, media_json_data):
    media_json = {}

    # media_href_list = response.xpath('//*[@class="ig-thumb-image"]//img/@src')
    try:
        media_href_list = response.xpath(
            '//*[@id="imageBlockThumbs"]//img/@src | //*[@id="altImages"]//li//img/@src')
        _ = media_href_list[0]
    except:
        media_href_list = response.xpath('//*[@id="altImages"]//li//img/@src')

    # print(response.xpath('//*[@class="ig-thumb-image"]'))
    media_href_list = [media_href for media_href in media_href_list
                       if not (media_href.endswith('.gif') or "play-icon" in media_href)
                       ]
    for order, media_href in enumerate(media_href_list, start=1):
        img_url = "/".join(media_href.split('/')[:-1]) + "/" + media_href.split('/')[-1].split('._')[0] + "." + \
                  media_href.split('/')[-1].split('._')[-1].split('.')[-1]

        media_json['img_url ' + str(order)] = img_url

    if not media_json:
        variant_names = media_json_data['colorToAsin'].keys()
        total_image_urls = []

        for variant in variant_names:
            image_urls = [img['large'] for img in media_json_data['colorImages'][variant]]
            total_image_urls += image_urls

        media_json = {'img_url': total_image_urls}


    return media_json


def get_bindings(response, media_json_data):
    variants_product_url = []

    binding_text_list = response.xpath('//*/div[@id="variation_color_name"]//li')

    if len(binding_text_list) == 1:
        binding_txt = binding_text_list.xpath('//*/span[@class="a-button-inner"]//a//span//text()')[0]
        try:
            selling_price_text = response.xpath('//*/div[@id="soldByThirdParty"]//span/text()')[0]
            selling_price_text = selling_price_text.replace('₹\xa0', '').strip()
            selling_price_text = float(selling_price_text)
        except:
            try:
                selling_price_text = response.xpath('//*[@class="a-price a-text-price"]//span//text()')
                selling_price_text = selling_price_text.replace('$\xa0', '').strip()
                selling_price_text = float(selling_price_text)

            except:
                selling_price_text = "-"

        binding_txt = binding_txt
        selling_price_text = selling_price_text

        variant_data = [{'product_1':
                             {'name': binding_txt,
                              'variant_url': "",
                              'selling_price': selling_price_text
                              }
                         }]

    elif len(binding_text_list) == 0:
        binding_txt = ""
        try:
            selling_price_text = response.xpath('//*/div[@id="soldByThirdParty"]//span/text()')[0]
            selling_price_text = selling_price_text.replace('$\xa0', '').strip()
            selling_price_text = float(selling_price_text)
        except:
            try:
                selling_price_text = " ".join(binding_text_list.xpath(
                    '//*/span[@class="a-button-inner"]/a/span//text()'))
                selling_price_text = selling_price_text.split("from")[-1].strip()
                selling_price_text = selling_price_text.replace('$\xa0', '').strip()
                selling_price_text = float(selling_price_text)
            except:
                try:
                    selling_price_text = " ".join(response.xpath('//*[@id="priceblock_ourprice"]//text()'))
                    selling_price_text = selling_price_text.replace('₹\xa0', '').strip()
                except:
                    selling_price_text = "-"

        binding_txt = binding_txt
        selling_price_text = selling_price_text

        variant_data = [{'product_1':
                             {'name': binding_txt,
                              'variant_url': "-",
                              'selling_price': selling_price_text
                              }
                         }]

    else:

        variant_data = []

        for order in range(len(binding_text_list)):

            try:
                variant_url = response.xpath('//*/div[@id="variation_color_name"]//li['
                                             + str(order + 1)
                                             + ']//@data-dp-url')[0]

                variant_url = modify_url(variant_url)

                binding_txt = response.xpath('//*/div[@id="variation_color_name"]//li['
                                             + str(order + 1)
                                             + ']//@title')[0]
                binding_txt = binding_txt.replace("Click to select ", "")

                selling_price_text = [i for i in response.xpath('//*/div[@id="variation_color_name"]//li['
                                                                + str(order + 1) + ']//text()') if "$" in i][0]

                selling_price_text = selling_price_text.replace('$\xa0', '').strip()

                variant_data.append({'product_' + str(order + 1):
                                         {'name': binding_txt,
                                          'variant_url': variant_url,
                                          'selling_price': selling_price_text
                                          }
                                     })

            except:

                variant_data = [{"product_" + str(i + 1): {"name": key, "variant_url": "-", "selling_price": "-"}}
                            for i, key in enumerate(media_json_data['colorToAsin'].keys())]

    return variant_data


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


def get_review_extraction(response):
    review_data = []
    reviews = response.xpath('.//div[@class="a-section celwidget"]')

    for review in reviews:
        try:
            text = "".join([i.strip() for i in review.xpath('.//span[@data-hook="review-body"]//text()')]).replace("\n",
                                                                                                                   "")
            header = review.xpath('.//a[@data-hook="review-title"]//span[2]//text()')[0]
            stars = review.xpath('.//i[@data-hook="review-star-rating"]//text()')[0]
            stars = float(stars.replace(" out of 5 stars", ""))
            date = review.xpath('.//span[@data-hook="review-date"]//text()')[0]

            review_data.append({"header": header,
                                "text": text,
                                "stars": stars,
                                "date": date
                                })
        except:
            continue

    return review_data

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


def main(url):

    r = requests.get(url)

    # if r.status_code != 200:
    #     MB_SYSTEMMODAL = 0x00001000
    #     ctypes.windll.user32.MessageBoxW(0, "No Data Received",  "WEB SCRAPING ALERT", MB_SYSTEMMODAL)

    response = html.fromstring(r.content)

    json_xpath = '//*[@id="imageBlockVariations_feature_div"]/script/text()'

    media_json_string = response.xpath(json_xpath)[0].strip().split("jQuery.parseJSON(\'")[-1].strip().split("');")[0]
    media_json_data = json.loads(media_json_string)

    pv_item = {"url": url}
    try:
        pv_item["Title"] = response.xpath('//*[@id="productTitle"]//text()')[0].strip()
    except:
        title_texts = response.xpath('//*[@id="title"]//text()')
        pv_item["Title"] = " ".join([title_txt for title_txt in title_texts if title_txt.strip()])

    authors = response.xpath('//*/a[@class="a-link-normal contributorNameID"]//text()')

    if len(authors):
        pv_item["Authors"] = ", ".join(authors)
    else:
        authors = response.xpath('//*[@id="bylineInfo"]//a//text()')
        pv_item["Authors"] = ", ".join(authors)

    pv_item["variant_data"] = get_bindings(response, media_json_data)
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
    media_json = get_media(response, media_json_data)
    pv_item.update(media_json)

    return pv_item


def amazon_scrapping(url):

    product_data = main(url)

    keys = product_data.keys()

    if 'img_url' not in keys:
        json_xpath = '//*[@id="imageBlockVariations_feature_div"]/script/text()'

        r = requests.get(url)
        response = html.fromstring(r.content)

        media_json_string = response.xpath(json_xpath)

        media_json_string = media_json_string[0].strip().split("jQuery.parseJSON(\'")[-1].strip().split("');")[0]
        media_json_string = media_json_string.encode('utf-8').decode('unicode_escape')
        media_json_data = json.loads(media_json_string)

        variant_names = media_json_data['colorToAsin'].keys()

        total_image_urls = []

        for variant in variant_names:
            image_urls = [img['large'] for img in media_json_data['colorImages'][variant]]
            total_image_urls += image_urls

        total_image_urls_dict = {'img_url': total_image_urls}

        product_data.update(total_image_urls_dict)

    return product_data
