import requests

def pyatyorochka(url):

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'text/plain;charset=UTF-8',
        'origin': 'https://5ka.ru',
        'priority': 'u=1, i',
        'referer': 'https://5ka.ru/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    response = requests.get(url=url, headers=headers)
    json_file = response.json()
    products = json_file["products"]
    srt_lst = []

    for product in products:

        if product["prices"]["discount"]:
            price = product["prices"]["discount"]
        else:
            price = product["prices"]["regular"]

        name = product["name"]

        srt_lst.append([float(price), name])

    return srt_lst