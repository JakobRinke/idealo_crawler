import requests
try:
    from item_filter.amz_headers import get_header
except:
    from amz_headers import get_header
import time

AMAZON_FEE_URL = "https://sellercentral.amazon.de/rcpublic/getfees?countryCode=DE&locale=de-DE"
AMAZON_PRICE_URL = "https://sellercentral.amazon.de/rcpublic/getadditionalpronductinfo?countryCode=DE&asin={}&fnsku=&searchType=GENERAL&locale=de-DE"

def get_post_data(item, p=None):
    item_id = item.ean
    if p is not None:
        price = p
    else:
        price = item.avgr30
    return {
        "countryCode": "DE",
        "programIdList": ["Core", "MFN"],
        "itemInfo": {
            "afnPriceStr": str(price),
            "asin": item_id,
            "currency": "EUR",
            "dimensionUnit": "",
            "glProductGroupName": item.get_cat_gl(),
            "isNewDefined": False,
            "mfnPriceStr":  str(price),
            "mfnShippingPriceStr": "0",
            "packageHeight": "0",
            "packageLength": "0",
            "packageWeight": "0",
            "packageWidth": "0",
            "weightUnit": ""
        }
    }


def get_amazon_fees_json(item, p):
    resp = requests.post(AMAZON_FEE_URL, json=get_post_data( item, p), headers=get_header())
    return resp.json()

def get_shipping_fees(item, idealo_price, p):
    try:
        fees = get_amazon_fees_json( item, p)
    except Exception as e:
        return 1000000
    brutto_price = idealo_price / 1.19
    amazonPrgrm = fees['data']['programFeeResultMap']["Core"]
    costs = brutto_price
    costs += amazonPrgrm["otherCost"]["vatAmount"]["amount"]
    # Peak time: From Okt - Dez
    is_peak_time = time.localtime().tm_mon in [10, 11, 12]
    if is_peak_time:
        costs += amazonPrgrm["perUnitStorageFee"]["total"]["amount"]
    else:
        try:
            costs += amazonPrgrm["perUnitNonPeakStorageFee"]["total"]["amount"]
        except:
            costs += amazonPrgrm["perUnitStorageFee"]["total"]["amount"]

    mfn = fees['data']['programFeeResultMap']["MFN"]["otherFeeInfoMap"]
    for k, v in mfn.items():
        costs += v["total"]["amount"]
    try:
        costs += amazonPrgrm["otherFeeInfoMap"]["FulfillmentFee"]["total"]["amount"]
    except: 
        pass

    return costs




if __name__ == '__main__':
    product = AmazonProduct("https://www.amazon.de/dp/B08HJXV1P1", 214.2)
    print(get_shipping_fees(product, 214.2))