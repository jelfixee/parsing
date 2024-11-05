import pandas as pd
from config import stores
import time
from datetime import datetime
import schedule

def collect_data():
    try:
        df = pd.read_csv("data.csv")

    except FileNotFoundError:
        columns = ["title", "item_category", "price", "date", "store"]
        df = pd.DataFrame(columns=columns)

    current_t = datetime.now().strftime("%d.%m.%Y")

    for store in stores:
        for item_category, link in store:

            response = store["func"](link)
            store_name = store["name"]
            price = response[0]
            title = response[1]
            settled_df = df.set_index("title")

            if (title in df.title and price < settled_df.price) or (title in df.title and price > settled_df.price):

                settled_df.loc[title, "price"] = price
                settled_df.loc[title, "date"] = current_t
                df = settled_df.reset_index()

            elif title in df.title and price == settled_df.loc[title].price:
                continue

            else:
                df = df._append({"item_category": item_category, "price": price, "title": title, "date": current_t, "store": store_name})

    df = df.sort_values(by=["item_category", "price"])
    df.to_csv('data.csv', index=False)

if __name__=="__main__":
    schedule.every().day.at("4:00").do(collect_data)
    print("System has been launched")

    while True:
        schedule.run_pending()
        time.sleep(1)