import requests
import aiohttp
from bs4 import BeautifulSoup
from time import time
import json
import asyncio
from fake_useragent import UserAgent

def get_dictionary(url, headers):
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    categories_urls = [[subcat["href"] for subcat in cat.find_all("a")] for cat in soup.find("div", class_="customScrollbar scrollblock scrollblock--thick").find("ul").find_all("ul")]
    categories_names = [cat.text for cat in [cat_name.find("span", class_="name option-font-bold") for cat_name in soup.find("div", class_="customScrollbar scrollblock scrollblock--thick").find("ul").find_all("li")] if cat]
    dictionary = {k: v for k, v in zip(categories_names, categories_urls)}
    return dictionary

def get_page(link, url, headers):
    return await pagination

get product_data():

async def main():
    link = "https://latuno.ru"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "User-Agent": UserAgent().random
    }

    start_time = time()
    tasks = []
    dictionary = get_dictionary(link, headers)

    for category in dictionary.keys():
        for urls in category:
            tasks.append(asyncio.create_task())
    await asyncio.gather(*tasks)


    print(time() - start_time)

    print("Finish")

if __name__ == "__main__":
    asyncio.run(main())