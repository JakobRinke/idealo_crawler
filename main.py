import time
import idealo.idealo_crawler as idealo_crawler
from idealo.idealo_item import IdealoShopItem
import item_filter.item_filter as item_filter
from item_filter.amazon_product import AmazonProduct
import requests
import os
import google_writer

item_cache = []
def onItem(item:IdealoShopItem, driver):
    if item_filter.get_filter_val(item) and item.name not in item_cache:
        item_cache.append(item.name)
        print(item)
        #to_csv(item)
        add_to_writer(item)

def to_csv(item:IdealoShopItem, file="output.csv"):
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("Name, Buy Price, Current Amazon Price, 30 day Average,BSR, Rating Count,Amazon Link, Idealo Link, Marge, Marge %\n")
    with open(file, "a") as f:
        name = item.name
        buy_price = item.best_offer.price
        cur_amazon_price = item.amazon_offer.price
        avgr30 = item.get_amazon_item().get_avgr30(item.driver)
        bsr = item.get_amazon_item().get_bsr()
        rating_count = item.get_amazon_item().get_rating_count()
        amazon_link = item.amazon_offer.redirectLink
        idealo_link = item.idealo_listing
        marge = item_filter.get_marge(item)
        marge_percent = marge / item.amazon_offer.price * 100
        f.write(f"{name},{buy_price},{cur_amazon_price},{avgr30},{bsr},{rating_count},\"{amazon_link}\",\"{idealo_link}\",{marge},{marge_percent}\n")


def add_to_writer(item:IdealoShopItem):
    name = item.name
    buy_price = item.best_offer.price
    cur_amazon_price = item.amazon_offer.price
    avgr30 = item.get_amazon_item().get_avgr30(item.driver)
    bsr = item.get_amazon_item().get_bsr()
    rating_count = item.get_amazon_item().get_rating_count()
    amazon_link = item.amazon_offer.redirectLink
    idealo_link = item.idealo_listing
    marge = item_filter.get_marge(item)
    marge_percent = marge / item.amazon_offer.price * 100
    data = [name, buy_price, cur_amazon_price, avgr30, bsr, rating_count, amazon_link, idealo_link, marge, marge_percent]
    google_writer.add_to_sheet(data)

        


if __name__ == "__main__":
    category_ids = [
        30311,
        3626,
        4033,
        3686,
        3326,
        3932,
        2400,
        7032
    ]
    t = time.time()
    items = idealo_crawler.multi_threaded_category_search(category_ids, onItem)
    print("Fetched ", len(items), " items in ", time.time() - t, " seconds")