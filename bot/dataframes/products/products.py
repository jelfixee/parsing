import pandas as pd
from bot.app.config.config import stores
import time
from datetime import datetime
import schedule
import os


def retry(store, link, attemps=5, delay=3):
    while attemps:
        try:
            response = store["func"](link)
            return response


        except Exception as e:
            print(f"[INFO] retry = {attemps} => {link} | {store["name"]} | {e}")

            if attemps:
                time.sleep(delay)
                attemps -= 1

            else:
                raise


def collect_data():
    try:
        df = pd.read_csv("data.csv")

    except FileNotFoundError:
        columns = ["title", "item_category", "price", "date", "store"]
        df = pd.DataFrame(columns=columns)

    current_t = datetime.now().strftime("%d.%m.%Y")

    for store in stores:

        for item_category, link in store["items"].items():

            try:
                response = retry(store, link)

                for pare in response:

                    store_name = store["name"]
                    price = pare[0]
                    title = pare[1]
                    settled_df = df.set_index("title")

                    if title in df.title.unique() and price != settled_df.loc["title"].price:
                        settled_df.loc[title, "price"] = price
                        settled_df.loc[title, "date"] = current_t
                        df = settled_df.reset_index()

                    elif title in df.title.unique() and price == settled_df.loc[title].price:
                        continue

                    else:
                        df = df._append({"item_category": item_category, "price": price, "title": title, "date": current_t, "store": store_name}, ignore_index=True)


            except:
                continue

    try:
        os.remove("data.csv")
        df.to_csv('exdata.csv', index=False)
        os.rename("exdata.csv", "data.csv")


    except:
        df.to_csv('data.csv', index=False)


if __name__ == "__main__":
    collect_data()
    # schedule.every().day.at("04:00").do(collect_data)
    print("System has been launched")

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
