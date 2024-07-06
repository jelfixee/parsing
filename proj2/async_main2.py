import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS
from math import ceil
import json
from time import time

start_time = time()

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

url = "https://rebelstore.ru"

async def get_catalog(session, url, headers):
        async with session.get(url=url, headers=headers) as response:
            soup = BS(await response.text(), "lxml")

            cats = [url + catalog for catalog in [cat["href"] for cat in soup.find("div", class_="mait-cat-wrap").find_all("a")]]

            for cat in cats:
                async with session.get(url=cat ,headers=headers) as cat_response:
                    cat_soup = BS(await cat_response.text(), "lxml")

                    pages = ceil(
                        int(cat_soup.find("div", class_="pagination").find("div").text.strip().split("    ")[-1]) / 24)

                    print(pages)


async def main(url, headers):
    tasks = []
    async with aiohttp.ClientSession() as session:
        task = asyncio.create_task(get_catalog(session, url, headers))
        tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main(url, headers))
    finish = time() - start_time
    print(finish)