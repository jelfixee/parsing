
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

def get_data(url, headers, retry=5):

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
            products_catalog_url_response = requests.get(url=products_catalog_url, headers=headers)
            products_catalog_url_soup = BeautifulSoup(products_catalog_url_response.text, "lxml")

            products = products_catalog_url_soup.find("div", class_="products").find_all("article", class_="product")
            products_urls = [url + product.find("a")["href"] for product in products]

            for product_url in products_urls:
                try:
                    product_url_response = requests.get(url=product_url, headers=headers)
                    print(f"[+] {product_url} {product_url_response.status_code}")
                except Exception as ex:
                    if retry:
                        print(f"[INFO] retry={retry} => {product_url}")
                    else:
                        raise
                else:
                    product_url_soup = BeautifulSoup(product_url_response.text, "lxml")

                    try:
                        name = product_url_soup.find("h1").text.strip()
                    except:
                        name = "Нет названия"
                    try:
                        price = int("".join([symbol for symbol in product_url_soup.find("div", class_="price new").text.strip() if symbol.isdigit()]))
                    except:
                        price = "Нет цены"
                    try:
                        description = product_url_soup.find("div", class_="bx_item_description").text.strip().replace("\n","")
                    except:
                        description = "Нет описания"

                    products_data.append(
                        {
                            "name": name,
                            "price": price,
                            "description": description,
                            "product_url": product_url
                        }
                    )

    with open(r"D:\testsforpy\test2.json", "w+", encoding="utf-8") as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)

def main():
    get_data(url, headers)
    print("Finish")
    finish_time = time.time() - start_time
    print(finish_time)

if __name__=="__main__":
    main()