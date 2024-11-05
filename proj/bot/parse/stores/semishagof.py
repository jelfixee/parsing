import requests
from bs4 import BeautifulSoup as bs

def semishagof(url):

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    response = requests.get(url=url, headers=headers)

    soup = bs(response.text, "lxml")

    products = soup.find("div", class_="cat2-list").find_all("div", class_="cat-item")

    srt_lst = []

    for product in products:

        price = product.find("div", class_="price").text.strip(" ₽")

        name = product.find("a", class_="cat-item__title").text

        srt_lst.append([float(price), name])

    return srt_lst

def main():
    url = "https://semishagoff.org/catalog/myasnaya-gastronomiya/"

    for row in semishagof(url):
        print(row)

if __name__=="__main__":
    main()