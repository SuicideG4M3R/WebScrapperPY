import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests


def scrap_offer(url):
    headers = {'User-Agent': UserAgent().random}
    page = requests.get(url, headers=headers)
    raw_html = BeautifulSoup(page.text, 'html.parser')

    price = raw_html.find('strong', {'data-cy': 'adPageHeaderPrice'}).text
    title = raw_html.find('h1', {'data-cy': 'adPageAdTitle'}).text
    label = raw_html.find('a', {'aria-label': 'Adres'}).text

    tables = raw_html.find('div', {'data-testid': 'ad.top-information.table'}).find('div')
    lst = []

    data = {
        'title': title,
        'price': price,
        'location': label,
    }
    for table in tables:
        for div in table:
            lst.append(div.text)
    clean = [elem for elem in lst if elem.strip() and 'css' not in elem]

    for i in range(len(clean) // 2):
        key = clean[i * 2]
        value = clean[i * 2 + 1]
        data[key] = value
    time.sleep(1)
    return data
