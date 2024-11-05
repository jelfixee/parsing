import requests
from bs4 import BeautifulSoup as bs

def okei(cat):

    url = 'https://www.okeydostavka.ru/webapp/wcs/stores/servlet/ProductListingView'

    cookies = {
        'spid': '1728073950007_93e919916f4dea9090b5f133025904ab_m1l1a9k71m19cbck',
        'WC_SESSION_ESTABLISHED': 'true',
        'WC_AUTHENTICATION_-1002': '-1002%2CzZHlyRjQcgWKqNcfDjyX4iZ02zjcQoyDurbFiQxFNVk%3D',
        '_ga': 'GA1.1.1587796706.1728073953',
        '_ym_uid': '1695646725534549903',
        '_ym_d': '1728073953',
        'isNative': '1',
        'storeGroup': 'msk1',
        'ffcId': '13151',
        'WC_USERACTIVITY_-1002': '-1002%2C10151%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C1877362032%2Cver_null%2CFiV6Js0qKXjqpS4KxY83MRWICuTU2u2kOsV1Y1hiUnW3iqj8SZxy5C3u3zGbIyN1t4qZzE873oOZfb62C88Ygz0VUhifRk5Zp0hz88HCMpha6QP0BQzy0VTpWGVeZYpVmALvEBGGlsRoj6se%2B7Z%2FLNdK1kPC90Rh%2FCZ6bnP74plFG8Hduhay1RZaa4bVBbcgrWYpJeKg76oiyoMkB9naZ0TSJy9kMJ1WmPy%2Bz79LL2FrJhHGcukNV6lWYqn4LAgx',
        'WC_GENERIC_ACTIVITYDATA': '[7462334018%3Atrue%3Afalse%3A0%3AzZ%2BXmMjHypIGu80OmZ8VtA%2Bhc7kTR0C2f0HkIQBKRHE%3D][com.ibm.commerce.context.entitlement.EntitlementContext|4000000000000000003%264000000000000000003%26null%26-2000%26null%26null%26null][com.ibm.commerce.context.audit.AuditContext|null][com.ibm.commerce.context.globalization.GlobalizationContext|-20%26RUB%26-20%26RUB][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][com.ibm.commerce.catalog.businesscontext.CatalogContext|10551%26null%26false%26false%26false][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.ExternalCartContext|null][com.ibm.commerce.context.bcsversion.BusinessContextVersionContext|null][CTXSETNAME|Store][com.ibm.commerce.context.base.BaseContext|10151%26-1002%26-1002%26-1][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null]',
        'selectedCity': '%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
        '_ym_isad': '1',
        'solarfri': 'ab844f3bb154a5ee',
        'spsc': '1729945573624_fef6519a19ca9c9e20c19e7b6a8be5fe_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5',
        'JSESSIONID': '00002R96-97hD9XcLrtEBK3gzm0:-1',
        'WC_ACTIVEPOINTER': '-20%2C10151',
        'gtmListKey': 'GTM_LIST_CATALOG',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.okeydostavka.ru',
        'priority': 'u=1, i',
        'referer': "https://www.okeydostavka.ru/msk/",
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'lm': '',
        'ajaxStoreImageDir': '/wcsstore/OKMarketSAS/',
        'searchType': '1000',
        'advancedSearch': '',
        'filterTerm': '',
        'storeId': '10151',
        'manufacturer': '',
        'ddkey': 'ProductListingView_6_-1011_3074457345618259713',
        'sType': 'SimpleSearch',
        'metaData': '',
        'catalogId': '10551',
        'searchTerm': '',
        'resultsPerPage': '72',
        'filterFacet': '',
        'resultCatEntryType': '',
        'gridPosition': '',
        'emsName': '',
        'disableProductCompare': 'true',
        'langId': '-20',
        'facet': '',
        'categoryId': cat,
        'custom_view': 'true',
    }

    data = {
        'contentBeginIndex': '0',
        'productBeginIndex': '0',
        'beginIndex': '0',
        'orderBy': '3',
        'facetId': '',
        'pageView': 'grid',
        'resultType': 'products',
        'orderByContent': '',
        'searchTerm': '',
        'facet': '',
        'facetLimit': '',
        'pageSize': '72',
        'langId': '-20',
        'totalPages': '2.0',
        'requestType': 'filter',
        'objectId': '_6_-1011_3074457345618259713',
        'requesttype': 'ajax',
    }

    with requests.Session() as session:

        ses = session.post(url=url, headers=headers, data=data, params=params, cookies=cookies)

    soup = bs(ses.text, "lxml")

    products = soup.find("div", class_="productListingWidget").find("div", class_="product_listing_container").find_all("div", class_="product ok-theme")

    srt_lst = []

    for product in products:

        name = product.find("div", class_="product-name").find("a").get("title")

        price = product.find("div", class_="mobile-actions").find("div", class_="product-cart").find("a").get("data-price")
        if price:
            srt_lst.append([float(price), name])
        else:
            continue

    return srt_lst