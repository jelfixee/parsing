import requests

def ashan(cat):

    url = "https://www.auchan.ru/v1/catalog/products?merchantId=1&page=1&perPage=40&orderField=price&orderDirection=asc&deliveryAddressSelected=0"

    json_data = {
        'filter': {
            'category': cat,
            'promo_only': False,
            'active_only': False,
            'cashback_only': False,
        },
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.auchan.ru',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'X-NewRelic-ID': 'undefined',
        'X-Token-CMD': '',
        'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEwMDAwMDAiLCJhcCI6IjMzMjQxMTMiLCJpZCI6ImEzODE1YmRkYjg5Y2ZiOTkiLCJ0ciI6IjdmZjZmZGY4ZGNmMDhlYzUxZWU5MGQ5ZDY5NzlhNDMwIiwidGkiOjE3Mjk0Mzc3MzkxNzF9fQ==',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'traceparent': '00-7ff6fdf8dcf08ec51ee90d9d6979a430-a3815bddb89cfb99-01',
        'tracestate': '1000000@nr=0-1-1000000-3324113-a3815bddb89cfb99----1729437739171',
    }

    response = requests.get(url=url, headers=headers, json=json_data)
    products = response.json()["items"]
    srt_lst = []
    m = 0

    for product in products:

        if not m:
            m = price = float(product["price"]["value"])

        elif m > float(product["price"]["value"]):
            break

        else:
            m = price = float(product["price"]["value"])

        name = product["title"]

        srt_lst.append([price, name])

    return srt_lst
