import aiohttp
from bs4 import BeautifulSoup
from time import time
import json
import asyncio
from fake_useragent import UserAgent

SEMAPHORE = asyncio.Semaphore(1)

async def fetch(session, url, headers):

    async with SEMAPHORE:
        try:

            async with session.get(url=url, headers=headers) as response:
                return await response.text()

        except aiohttp.ClientError as e:

            print(f"Ошибка запроса {e}")
            return None

async def parse_catalogs(html, url):

    soup = BeautifulSoup(html, "lxml")

    categories_urls = []

    for cat_url in soup.find("div", class_="customScrollbar scrollblock scrollblock--thick").find("ul", class_="menu-wrapper menu-type-1").find_all("li"):

        if cat_url.find("ul"):

            for cat in cat_url.find("ul"):

                try:
                    categories_urls.append(url + cat.find("a")["href"])
                except:
                    continue

    return categories_urls

async def get_pagination(html):

    soup = BeautifulSoup(html, "lxml")

    pagination = int(soup.find("div", class_="nums").find_all("a")[-1].text) if soup.find("div", class_="nums") else 0

    return pagination

async def parse_products(html, url):

    soup = BeautifulSoup(html, "lxml")

    products_list = []

    products = soup.find("div", class_="top_wrapper items_wrapper catalog_block_template").find_all("div", class_="col-lg-3 col-md-4 col-sm-6 col-xs-6 col-xxs-12 item item-parent catalog-block-view__item js-notice-block item_block")

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

        products_list.append(
            {
                "name": name,
                "price": price,
                "product_url": url + product_url
            }
        )
    return products_list


async def save_json(data):

    with open(r"D:\testsforpy\test3async.json", "w+", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

async def main():

    link = "https://latuno.ru"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "User-Agent": UserAgent().random
    }

    start_time = time()

    async with aiohttp.ClientSession() as session:

        html = await fetch(session, link, headers)

        if html is None:
            return

        catalogs = await parse_catalogs(html, link)

        products_data = []

        for catalog in catalogs:

            html = await fetch(session, catalog, headers)

            if html is None:
                continue

            pagination = await get_pagination(html)

            tasks = [asyncio.create_task(fetch(session, catalog + f"?PAGEN_1={page}", headers)) for page in range(1, pagination + 1)]

            pages = await asyncio.gather(*tasks)

            for page in pages:

                if page is None:
                    continue

                products = await parse_products(page, link)
                products_data.extend(products)

        await save_json(products_data)

    print(time() - start_time)

    print("Finish")

if __name__ == "__main__":
    asyncio.run(main())