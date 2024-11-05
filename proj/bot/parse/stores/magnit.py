import requests

def magnit(cat):

    url = "https://magnit.ru/webgate/v2/goods/search"

    cookies = {
        '_ym_uid': '170802001196085177',
        '_ym_d': '1727451571',
        'nmg_udi': '1DEB82A4-B9A9-8789-D233-BF28F102DF9A',
        'x_device_id': '1DEB82A4-B9A9-8789-D233-BF28F102DF9A',
        'mg_uac': '1',
        'cookies-modal': '1',
        'x_shop_type': 'MM',
        'nmg_sp': 'Y',
        'nmg_sid': '161866',
        'shopId': '161866',
        '_ga_MEJT7QPK6J': 'GS1.1.1727799697.1.0.1727799697.60.0.0',
        '_ga': 'GA1.1.393520055.1727451571',
        '_ym_isad': '1',
        '_ga_L0N0B74HJP': 'GS1.1.1729763335.19.0.1729763335.60.0.0',
        '_ym_visorc': 'b',
        'shopCode': '767694',
    }

    headers = {
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://magnit.ru',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/json',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-app-version': '7.0.0',
        'x-client-name': 'magnit',
        'x-device-id': '1DEB82A4-B9A9-8789-D233-BF28F102DF9A',
        'x-device-platform': 'Web',
        'x-device-tag': 'disabled',
        'x-new-magnit': 'true',
        'x-platform-version': 'Windows Chrome 130',
    }

    json_data = {
        'sort': {
            'order': 'asc',
            'type': 'price',
        },
        'pagination': {
            'limit': 33,
            'offset': 0,
        },
        'categories': [
            cat,
        ],
        'includeAdultGoods': True,
        'storeCode': '767694',
        'storeType': '1',
        'catalogType': '1',
    }

    with requests.Session() as session:

        ses = session.post(url=url, cookies=cookies, headers=headers, json=json_data)

    srt_lst = []

    for product in ses.json()["items"]:
        name = product["name"]
        price = product["price"]/100
        srt_lst.append([price, name])

    return srt_lst
