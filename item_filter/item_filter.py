from idealo.idealo_item import IdealoShopItem
from item_filter.filter_funcs import *

defaul_filter_funcs = [
    check_amazon, 
    check_best,
    check_price_ratio, 
    check_min_price,
    check_max_price,
    check_blacklist,
    check_word_blacklist,
    get_min_rating_val,
    check_selling_amount,
    check_profitablity_2,
    check_profitablity
]

def get_filter_val(item: IdealoShopItem, filter_funcs:list=defaul_filter_funcs):
    for f in filter_funcs:
        if not f(item):
            return False
    return True
