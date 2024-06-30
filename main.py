from database import connect_to_database, add_to_database, close_connection, check_if_already_in_database
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from listingCounter import get_offers_counter
from pages import get_number_of_pages
from scrap import scrap
from offer import scrap_offer
from url import get_url
print("Max price:")
max_price = input()
print("Min price:")
min_price = input()

headers = {'User-Agent': UserAgent().random}
page = requests.get(get_url(max_price, min_price), headers=headers)
raw_html = BeautifulSoup(page.text, 'html.parser')

counter = get_offers_counter(raw_html)
pages = get_number_of_pages(raw_html)

links_to_scrap = [scrap(raw_html)]


print(f'\n'
      f'Found pages: {pages}\n'
      f'Found Offers: {counter}\n'
      f'\n')

print(f'Page number 1 scrapped\n')

if pages > 1:
    for page in range(2, pages + 1):
        single_offer = requests.get(get_url(max_price, min_price, page=page), headers=headers)
        single_offer_raw_html = BeautifulSoup(single_offer.text, 'html.parser')
        links_to_scrap.append(scrap(single_offer_raw_html))
        print(f'Page number {page} scrapped\n')

print(f'Scrapped pages --> {len(links_to_scrap)}\n'
      f'Scrapped Offers --> {sum(len(page) for page in links_to_scrap)}\n')

session, House = connect_to_database()
for page in links_to_scrap:
    for offer in page:
        server = check_if_already_in_database(session, House, offer)
        if server:
            print(f'Already in database: {server.url}')
        else:
            try:
                data = scrap_offer(offer)
                add_to_database(session, House, offer, *data.values())
            except Exception as e:
                print(f'Error: {e}')
                print(f'Offer: {offer}\n')
                close_connection(session)
                raise Exception('main.py 55')
close_connection(session)
