import requests

def lenta(cat):

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,fi;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DeviceID': '6416fe53-b312-e964-a230-08288c57684f',
        'Experiments': 'exp_recommendation_cms.false, exp_apigw_purchase.test, exp_lentapay.test, exp_omni_price.test, exp_profile_bell.test, exp_newui_cancel_order.test, exp_newui_history_active_action.test_stars, exp_comment_picker_and_courier.test, exp_general_editing_page.test, exp_cl_omni_support.test, exp_cl_omni_authorization.test, exp_onboarding_sbp.default, exp_fullscreen.test, exp_profile_login.false, exp_new_notifications_show_unauthorized.test, exp_assembly_cost_location.cart, exp_search_bottom.default, exp_onboarding_editing_order.test, exp_cart_new_carousel.default, exp_newui_cart_cancel_editing.test, exp_newui_cart_button.test, exp_new_promov3., exp_sbp_enabled.test, exp_new_my_goods.test, exp_ui_catalog.test, exp_search_out_of_stock.default, exp_profile_settings_email.default, exp_cl_omni_refusalprintreceipts.test, exp_cl_omni_refusalprintcoupons.test, exp_accrual_history.test, exp_personal_recommendations.default, exp_newui_chips.test, exp_loyalty_categories.test, exp_growthbooks_aa.control, exp_test2.true, exp_search_suggestions_popular_sku.default, exp_test3.false',
        'Origin': 'https://lenta.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'SessionToken': '41D2A2D1F050367D5D7D809D944F565F',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'X-Delivery-Mode': 'pickup',
        'X-Device-Brand': '',
        'X-Device-ID': '6416fe53-b312-e964-a230-08288c57684f',
        'X-Device-Name': '',
        'X-Device-OS': 'iOS',
        'X-Device-OS-Version': '12.4.8',
        'X-Domain': 'moscow',
        'X-Organization-ID': '',
        'X-Platform': 'omniweb',
        'X-Retail-Brand': 'lo',
        'baggage': 'sentry-environment=production,sentry-release=web-11.0.412,sentry-public_key=b99355c72549498d9e9075cc3d4006a2,sentry-trace_id=fb0cbd7519c3450db011940e7e06781b,sentry-replay_id=ebdff8f20a93421b80903da9a6aa2e9b,sentry-sample_rate=1,sentry-transaction=%2Fcatalog%2F%3AcategoryId%2F,sentry-sampled=true',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sentry-trace': 'fb0cbd7519c3450db011940e7e06781b-8280b0d41e84f2e8-1',
        'traceparent': '00-eb588ec98004b9a74e1bfe3d34780c2e-7ccd5f56ee0ec55c-01',
        'x-span-id': '7ccd5f56ee0ec55c',
        'x-trace-id': 'eb588ec98004b9a74e1bfe3d34780c2e',
    }

    json_data = {
        'categoryId': cat,
        'limit': 40,
        'offset': 0,
        'sort': {
            'type': 'price',
            'order': 'asc',
        },
        'filters': None,
    }

    with requests.Session() as session:
        ses = session.post('https://lenta.com/api-gateway/v1/catalog/items', headers=headers, json=json_data)

    srt_lst = []

    for product in ses.json()["items"]:

        price = product["prices"]["cost"]/100
        name = product["name"]
        srt_lst.append([price, name])

    return srt_lst