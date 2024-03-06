import requests
try:
    from item_filter.amz_headers import get_header
except:
    from amz_headers import get_header


DIRCET_URL = "https://sellercentral.amazon.de/rcpublic/productmatch?searchKey={}&countryCode=DE&locale=de-DE"

def get_ean(url):
    return url.replace('https://www.amazon.de/dp/','').split('/')[0].split('?')[0]

def get_bsr(soup):
    try:
        return soup['salesRank']
    except:
        return -1

def get_rating_count(soup):
    try:
        return soup['customerReviewsCount']
    except:
        return -1

def get_rating(soup):
    try:
        return soup['customerReviewsRatingValue']
    except:
        return -1

def get_amazon_json(id):
    url = DIRCET_URL.format(id)
    resp = requests.get(url, headers=get_header())
    open("test.html", "w").write(resp.text)
    json = resp.json()
    if (json['succeed'] == False):
        return "{}"
    return json["data"]["otherProducts"]["products"][0]

def get_cat(soup):
    return soup['gl']


if __name__ == '__main__':
    js = get_amazon_json('B09TPPRG8B')
    print(get_bsr(js))
    print(get_rating_count(js))
    print(get_cat(js))

    soup2 = get_amazon_json('B09H1KQ2DH')
    print(get_bsr(soup2))
    print(get_cat(soup2))