import requests

def perekryostok(cat_id):

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'auth': "Bearer Token",
        'content-type': 'application/json',
        'origin': 'https://www.perekrestok.ru',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    json_data = {
        'page': 1,
        'perPage': 48,
        'orderBy': 'price',
        'orderDirection': 'asc',
        'filter': {
            'category': 122,
            'onlyWithProductReviews': False,
        },
        'withBestProductReviews': False,
    }

    url = "https://www.perekrestok.ru/api/customer/1.4.1.0/catalog/product/grouped-feed"

    with requests.Session() as session:
        ses = session.post(url=url, headers=headers, json=json_data)

    items = ses.json()["content"]["items"]

    srt_lst = []

    for item in items:
        if item["group"]["id"] == cat_id:
            products = item["products"]
            for product in products:

                price = product["priceTag"]["price"]/100

                name = product["title"]

                srt_lst.append([price, name])
            break

    return srt_lst

def main():
    for row in perekryostok(75):
        print(row)

if __name__=="__main__":
    main()
