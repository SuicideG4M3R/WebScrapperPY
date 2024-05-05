def get_number_of_pages(html):
    max_pages = 1
    try:
        number_of_pages = html.find('ul', {'data-testid': 'frontend.search.base-pagination.nexus-pagination'}).find_all(
            'li')
        active_page = []
        for pages in number_of_pages:
            if pages.text.isdigit():
                active_page.append(int(pages.text))
        max_pages = max(active_page)
    except AttributeError:
        return max_pages
    return max_pages
