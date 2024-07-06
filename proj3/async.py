import aiofiles
from bs4 import BeautifulSoup
import fake_useragent
from time import time
import json
import asyncio
import aiohttp

async def get_data(url, headers):
    products_data = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), "lxml")

            categories_urls = [[subcat["href"] for subcat in cat.find_all("a")] for cat in soup.find("div", class_="customScrollbar scrollblock scrollblock--thick").find("ul").find_all("ul")]
            categories_names = [cat.text for cat in [cat_name.find("span", class_="name option-font-bold") for cat_name in soup.find("div",class_="customScrollbar scrollblock scrollblock--thick").find("ul").find_all("li")] if cat]
            dictionary = {k: v for k, v in zip(categories_names, categories_urls)}

            for key in dictionary:
                for value in dictionary[key]:
                    page_url = url + value + "filter/in_stock-is-y/apply/"
                    async with session.get(url=page_url, headers=headers) as page_response:

                        page_soup = BeautifulSoup(await page_response.text(), "lxml")
                        pagination = int(page_soup.find("div", class_="nums").find_all("a")[-1].text) if page_soup.find("div", class_="nums") else 0

                        for page in range(1, pagination + 1):

                            real_url_cat = url + value + f"filter/in_stock-is-y/apply/?PAGEN_1={page}"

                            async with session.get(url=real_url_cat, headers=headers) as products_response:

                                print(real_url_cat)
                                print()
                                print(products_response)

                                products_soup = BeautifulSoup(await products_response.text(), "lxml")
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

    return products_data

async def main():
    url = "https://latuno.ru"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "User-Agent": fake_useragent.UserAgent().random
    }

    start_time = time()

    async with aiofiles.open(r"D:\testsforpy\test3async.json", "w+", encoding="utf-8") as file:
        json.dump(await get_data(url=url, headers=headers), file, indent=4, ensure_ascii=False)

    print(time() - start_time)

    print("Finish")

if __name__ == "__main__":
    asyncio.run(main())