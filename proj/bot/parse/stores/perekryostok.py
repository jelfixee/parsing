import requests

def perekryostok(cat_id):

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'auth': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJFRlBVcWRLamZTVG9vR09POWRpLURKQk4zWkgyaUxlcE5yWTF3dXgyNHFvIn0.eyJleHAiOjE3MzAxMjg3NDAsImlhdCI6MTczMDEyODM4MCwiYXV0aF90aW1lIjoxNzMwMTI4Mzc4LCJqdGkiOiJkNjcxNDA2ZC0xNzAyLTQ3MmYtYTc3Yi03ZTZmYzM5YjdiZTYiLCJpc3MiOiJodHRwczovL2lkLng1LnJ1L2F1dGgvcmVhbG1zL3Nzb3g1aWQiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiZjo2NmI5YWQ2MC00Y2I0LTRlZTEtYjlhMC0wNTI4ZmRlYWMyYjE6MzQxNTE4MjUiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ0Y3hfd2ViIiwic2Vzc2lvbl9zdGF0ZSI6ImIzMTc4NDc5LWU1NGYtNGVhZS1hNDY3LTRmYzBlMjYxZTkyZiIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBvZmZsaW5lX2FjY2VzcyBwcm9maWxlIGVtYWlsIiwic2lkIjoiYjMxNzg0NzktZTU0Zi00ZWFlLWE0NjctNGZjMGUyNjFlOTJmIiwic291cmNlX2RldGFpbCI6IndlYiIsInBlcm1pc3Npb25NYXJrZXRpbmciOiJOIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoi0JLQu9Cw0LTQuNGB0LvQsNCyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiNzk4MTcxNjU3MzEiLCJjaXBfaWQiOiJJRFguMzQxNTE4MjUiLCJnaXZlbl9uYW1lIjoi0JLQu9Cw0LTQuNGB0LvQsNCyIiwiZW1haWwiOiJtdmxhZDE3MzE3M0BnbWFpbC5jb20iLCJ4NWlkIjoiMzQxNTE4MjUifQ.KgEC2hotrdea5rLcdAsO_PS9WihowX3xSjGozYw_9-COo3kMnp9IlHpFppQJYdZ_YtbCL3WavAKxWxgBY-yc2yAGhHjyG0Knez9yVPa_DAvC1nyi8709h383KEU5VKHua3u-bWae4NUvAGzWxvKpdoV-cXNOdwPqfi88Ez3JTxUpSABft_tQ-_RC9q4hMYEWI1wXgB6PDDtQsGw5GQKIAzMdLOwYaUfRTZod8C1whrIoZh0vAYnv_6iyup0rNd3BzC0gJ8da9E4c3__7M-_bEDm6aPV0E9cTGVtYjEmAKwblkaY8gifr9QqIwrXlK-gdIfRtU6kRIVCozrS7_lAM5w',
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