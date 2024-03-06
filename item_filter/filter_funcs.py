from idealo.idealo_item import IdealoShopItem
from item_filter.amazon_product import AmazonProduct

def check_amazon(item: IdealoShopItem):
    return item.amazon_offer is not None

def check_best(item: IdealoShopItem):
    while item.best_offer is None or item.best_offer.price is None or item.best_offer.price == 0 or item.best_offer.redirectLink == None or check_blacklist(item):
        try:
            item.best_offer = item.offers.pop()
        except:
            return False
    return True

MIN_AMAZON_RATIO = 1.15
def check_price_ratio(item: IdealoShopItem):
    return item.amazon_offer.price / item.best_offer.price >= MIN_AMAZON_RATIO

MIN_PRICE = 20
def check_min_price(item: IdealoShopItem):
    return item.best_offer.price > MIN_PRICE

MAX_PRICE = 4000
def check_max_price(item: IdealoShopItem):
    return item.best_offer.price < MAX_PRICE

def check_blacklist(item: IdealoShopItem):
    for b in BLACKLIST:
        if b in item.name.lower():
            return False
    return True

def check_shop_blacklist(item: IdealoShopItem):
    for b in SHOP_BLACKLIST:
        if b.lower() in item.best_offer.shopName.lower() or b.lower() in item.best_offer.redirectLink.lower():
            return False
    return True

MIN_AMAZON_WIN_RATIO = 0.1
def check_profitablity(item: IdealoShopItem):
    marge = get_marge(item)
    return marge / item.amazon_offer.price >= MIN_AMAZON_WIN_RATIO

def get_marge(item: IdealoShopItem):
    amz = item.get_amazon_item()
    if amz is None:
        return -1
    # return item.amazon_product.get_avgr30(item.amazon_offer.price) - amz.get_cost(item.best_offer.price)
    return item.amazon_offer.price - amz.get_cost(item.best_offer.price)


MIN_RATING = 10
MIN_RATING_IF_NO_BSR = 30
MIN_BSR = 50000
def check_selling_amount(item: IdealoShopItem):
    amazon_product = item.get_amazon_item()
    if amazon_product.get_bsr() == -1:
        return amazon_product.get_rating_count() > MIN_RATING_IF_NO_BSR
    return amazon_product.get_bsr() < MIN_BSR

MIN_RATING = 4
def get_min_rating_val(item: IdealoShopItem):
    amazon_product = item.get_amazon_item()
    return amazon_product.get_rating() >= MIN_RATING


with open("marken_blacklist.txt", "r") as f:
    BLACKLIST = f.read().split("\n")
    BLACKLIST = [x.lower().strip() for x in BLACKLIST]

with open("shop_blacklist.txt", "r") as f:
    SHOP_BLACKLIST = f.read().split("\n")
    SHOP_BLACKLIST = [x.lower().strip() for x in SHOP_BLACKLIST]