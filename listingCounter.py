def get_offers_counter(html):
    return html.find('h1', {'data-cy': 'search-listing.heading'}).find_next_sibling().find_next_sibling().text.split(' ')[3]