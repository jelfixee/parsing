import requests
from bs4 import BeautifulSoup as bs

def met(url):

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://online.metro-cc.ru/',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    response = requests.get(url=url, headers=headers)
    soup = bs(response.text, "lxml")
    products = soup.find_all("div", class_="product-card__content")

    srt_lst = []

    for product in products:

        name = product.find("span", class_="product-card-name__text").text.strip()
        parts = product.find("span", class_="product-price__sum")

        if parts.find("span", class_="product-price__sum-penny"):
            price = parts.find("span", class_="product-price__sum-rubles").text + parts.find("span", class_="product-price__sum-penny").text
        else:
            price = parts.find("span", class_="product-price__sum-rubles").text

        srt_lst.append([float(price), name])

    return srt_lst