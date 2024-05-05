def get_url(max=2000, min=1, page=0):
    return (f'https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/mazowieckie/warszawa/warszawa/warszawa'
            f'?distanceRadius=0&limit=72&priceMax={max}&priceMin={min}&'
            f'by=DEFAULT&direction=DESC&viewType=listing{f'&page={page}' if page > 1 else ''}')
