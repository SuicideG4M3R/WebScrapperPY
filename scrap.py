import time


def scrap(html):
    scrapped = []
    listings = html.find('div', {'data-cy': 'search.listing.organic'}).find_all('a', {'data-cy': 'listing-item-link'})
    for item in listings:
        link = item.get('href')
        scrapped.append('https://www.otodom.pl' + link)
    time.sleep(1)
    return scrapped
