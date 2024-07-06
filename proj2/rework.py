
                ### TODO: Сделать код асинхронным

import requests
from bs4 import BeautifulSoup
from math import ceil
import json
import time

start_time = time.time()

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

url = "https://rebelstore.ru"

def get_data(url, headers):

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    catalogs = [cat["href"] for cat in soup.find("div", class_="mait-cat-wrap").find_all("a")]

    products_data = []
    catalogs_urls = []

    for catalog in catalogs:
        catalogs_urls.append(url + catalog)

    for catalog_url in catalogs_urls:
        cat_response = requests.get(url=catalog_url, headers=headers)
        cat_soup = BeautifulSoup(cat_response.text, "lxml")
        products_num = int(cat_soup.find("div", class_="pagination").find("div").text.strip().split("    ")[-1])
        pages = ceil(products_num / 24)

        for page in range(1, pages + 1):
            products_catalog_url = catalog_url + f"?0=A&1=r&2=r&3=a&4=y&?PAGEN_1={page}"
            products_catalog_response = requests.get(url=products_catalog_url, headers=headers)
            products_catalog_soup = BeautifulSoup(products_catalog_response.text, "lxml")
            products = products_catalog_soup.find("div", class_="products").find_all("article", class_="product")

            for product in products:
                try:
                    name = product.find("div", class_="title").find("a").text.strip()
                except:
                    name = "Нет названия"
                try:
                    price = int("".join([symbol for symbol in product.find("div", class_="summary").find("div", class_="price new").text.strip() if symbol.isdigit()]))
                except:
                    price = "Нет цены"
                try:
                    manufacturer =  product.find("div", class_="manufacturer").text.strip()
                except:
                    manufacturer = "Нет бренда"
                try:
                    product_url = url + product.find("div", class_="title").find("a")["href"]
                except:
                    product_url = "Нет ссылки"

                data = {
                        "name": name,
                        "manufacturer": manufacturer,
                        "price": price,
                        "product_url": product_url
                    }

                if data not in products_data:
                    products_data.append(data)
                else:
                    continue

    with open(r"D:\testsforpy\test1.json", "w+", encoding="utf-8") as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)

def main():
    get_data(url, headers)
    print("Finish")
    finish_time = time.time() - start_time
    print(finish_time)

if __name__=="__main__":
    main()