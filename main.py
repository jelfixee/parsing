import requests
from bs4 import BeautifulSoup
import fake_useragent
from time import sleep, time
import json

def get_data(url, headers, retry=5):
    products_data = []

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    categories_urls = [[subcat["href"] for subcat in cat.find_all("a")] for cat in soup.find("div", class_="customScrollbar scrollblock scrollblock--thick").find("ul").find_all("ul")]
    categories_names = [cat.text for cat in [cat_name.find("span", class_="name option-font-bold") for cat_name in soup.find("div",class_="customScrollbar scrollblock scrollblock--thick").find("ul").find_all("li")] if cat]
    dictionary = {k: v for k, v in zip(categories_names, categories_urls)}

    for key in dictionary:
        for value in dictionary[key]:
            page_url = url + value + "filter/in_stock-is-y/apply/"

            try:
                page_response = requests.get(url=page_url, headers=headers)
            except:
                if retry:
                    print(f"[INFO] retry={retry} => {page_url}")
                    sleep(3)
                else:
                    raise
            else:
                page_soup = BeautifulSoup(page_response.text, "lxml")
                pagination = int(page_soup.find("div", class_="nums").find_all("a")[-1].text) if page_soup.find("div", class_="nums") else 0

                for page in range(1, pagination + 1):

                    real_url_cat = url + value + f"filter/in_stock-is-y/apply/?PAGEN_1={page}"

                    try:
                        products_response = requests.get(url=real_url_cat, headers=headers)
                    except:
                        if retry:
                            print(f"[INFO] retry={retry} => {real_url_cat}")
                            sleep(3)
                        else:
                            raise
                    else:
                        products_soup = BeautifulSoup(products_response.text, "lxml")
                        products = products_soup.find("div", class_="top_wrapper items_wrapper catalog_block_template").find_all("div", class_="col-lg-3 col-md-4 col-sm-6 col-xs-6 col-xxs-12 item item-parent catalog-block-view__item js-notice-block item_block")

                        for product in products:

                            try:
                                name = product.find("div", class_="item-title").find("a").text.strip()
                            except:
                                name = "Нет названия"
                            try:
                                product_url = product.find("div", class_="item-title").find("a")["href"]
                            except:
                                product_url = "Нет ссылки"
                            try:
                                price = int("".join([i for i in product.find("div", class_="price_value_block values_wrapper").find("span", class_="price_value").text.strip() if i.isdigit()]))
                            except:
                                price = "Нет цены"

                            products_data.append(
                                {
                                    "name": name,
                                    "price": price,
                                    "product_url": url + product_url
                                }
                            )

    with open(r"D:\testsforpy\test3.json", "w+", encoding="utf-8") as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)

def main():
    url = "https://latuno.ru"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "User-Agent": fake_useragent.UserAgent().random
    }

    start_time = time()

    get_data(url, headers)

    print(time() - start_time)

    print("Finish")

if __name__ == "__main__":
    main()