import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests


def get_html(url):
    headers = {'User-Agent': UserAgent().random}
    page = requests.get(url, headers=headers, stream=True, timeout=5)
    time.sleep(1)
    return BeautifulSoup(page.text, 'html.parser')


def scrap_offer(url):
    raw_html = get_html(url)
    tables = []
    counter = 0
    max_attempts = 10

    # Tries to download tables from the website
    # (There was problem with GET requests,
    # sometimes did not return full website content despite setting different timeouts/time.sleep's)

    while not tables and counter < max_attempts:
        print(counter)
        try:
            tables = raw_html.find('div', {'data-cy': 'ad.top-information.table'}).find('div')
        except AttributeError:
            counter += 1
            raw_html = get_html(url)

    if not tables:
        raise ConnectionError(f"Can't download content offer.py 28")
    else:
        price = raw_html.find('strong', {'data-cy': 'adPageHeaderPrice'}).text
        title = raw_html.find('h1', {'data-cy': 'adPageAdTitle'}).text
        label = raw_html.find('a', {'aria-label': 'Adres'}).text

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
    return data
