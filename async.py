import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_catalogs(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Предполагаем, что ссылки на каталоги находятся в элементах с классом 'catalog-link'
    catalog_links = soup.find_all(class_='catalog-link')
    return ['https://latuno.ru' + link['href'] for link in catalog_links if 'href' in link.attrs]

async def parse_pagination(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Предполагаем, что информация о пагинации находится в элементе с классом 'pagination'
    pagination = soup.find(class_='pagination')
    if pagination:
        pages = pagination.find_all('a')
        if pages:
            last_page_link = pages[-2]  # Предполагаем, что предпоследняя ссылка ведет на последнюю страницу
            last_page_number = int(last_page_link.get_text())
            return last_page_number
    return 1  # Если пагинация отсутствует, возвращаем 1 страницу

async def parse_products(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all(class_='product')
    product_list = []
    for product in products:
        name = product.find('h2').get_text()
        price = product.find(class_='price').get_text()
        product_list.append({'name': name, 'price': price})
    return product_list

async def save_to_json(products, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

async def main():
    url = 'https://latuno.ru'
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        catalogs = await parse_catalogs(html)
        all_products = []
        for catalog in catalogs:
            html = await fetch(session, catalog)
            max_pages = await parse_pagination(html)
            tasks = [asyncio.create_task(fetch(session, f"{catalog}?page={page}")) for page in range(1, max_pages + 1)]
            pages = await asyncio.gather(*tasks)
            for page in pages:
                products = await parse_products(page)
                all_products.extend(products)
        await save_to_json(all_products, 'products.json')
        print('Информация о продуктах сохранена в файл "products.json".')

if __name__ == '__main__':
    asyncio.run(main())