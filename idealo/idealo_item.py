import time
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By

from item_filter.amazon_product import AmazonProduct

def convert_int(string:str):
    k = int("0" + ''.join(filter(str.isdigit, string.strip().split(" ")[0]))) / 100
    return k 

ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}

ITEM_FIND_URL = "https://www.idealo.de/offerpage/offerlist/product/{0}/start/{1}/sort/default"

class IdealoItemHead:

    def __init__(self, name, diplayPrice, link):
        self.name = name
        self.displayPrice = convert_int(diplayPrice)
        self.link = link
        self.id = link.split("/")[-1].split("_")[0]

    def __str__(self):
        return f"{self.name} - {self.displayPrice}  -> {self.link}"
    
    def get_real_item(self, driver:webdriver.Chrome):
        return IdealoShopItem(driver, self.id, self.name)


class IdealoShopItem:

    def __init__(self, driver:webdriver.Chrome, id:str, name:str):
        self.amazon_product:AmazonProduct = None
        self.driver = driver
        self.offers = []
        self.id = id
        self.name = name
        self.idealo_listing = "https://www.idealo.de/preisvergleich/OffersOfProduct/" + id + ".html"
        for i in range(0, 15 * 2, 15):
            try:
                driver.get(ITEM_FIND_URL.format(id, i))
            except:
                time.sleep(5)
                driver.get(ITEM_FIND_URL.format(id, i))
            self.amazon_offer:IdealoItemOffer = None
            self.best_offer:IdealoItemOffer = None
            for item in driver.find_elements(By.CSS_SELECTOR, ".productOffers-listItem"):
                of = IdealoItemOffer(self, item.get_attribute("outerHTML"))
                if (self.best_offer is None) or (self.best_offer.price==0) or (self.best_offer.price > of.price and of.shopName != "unknown" and of.price > 0):
                    self.best_offer = of
                if self.amazon_offer is None and "amazon" in of.shopName:
                    self.amazon_offer = of
                self.offers.append(of)
            if self.amazon_offer is not None:
                break

                

        # sort offers by price
        self.offers.sort(key=lambda x: x.price)

    def __str__(self):
        output =  "Name: " + str(self.name) + "\n"
        output += "Offers: " + str(len(self.offers)) + "\n"
        output += "Best Offer: " + str(self.best_offer) +  "\n"
        output += "Amazon Offer: " + str(self.amazon_offer) + "\n\n"
        return output 
    
    def get_amazon_item(self):
        if self.amazon_product is not None:
            return self.amazon_product
        if self.amazon_offer is None:
            return None
        if not "amazon.de" in self.amazon_offer.redirectLink:
            try:
                self.driver.get(self.amazon_offer.redirectLink)
                self.amazon_offer.redirectLink = self.driver.current_url
            except:
                return None
        self.amazon_product = AmazonProduct(self.amazon_offer.redirectLink, self.amazon_offer.price, self.driver)
        return self.amazon_product


class IdealoItemOffer:

    def __init__(self, item:IdealoShopItem, html):
        self.item = item
        soup = BeautifulSoup(html, 'html.parser')
        try:
            self.nameInShop = soup.find("span", attrs={"class": "productOffers-listItemTitleInner"}).text
        except:
            self.nameInShop = item.name
        try:
            self.price = convert_int(soup.find("a", attrs={"class": "productOffers-listItemOfferPrice"}).text)
        except:
            self.price = 0
        try:
            self.shopName = soup.find("img", attrs={"class": "productOffers-listItemOfferShopV2LogoImage"}).get("alt").split(" ")[0].lower()
        except:
            self.shopName = "unknown"
        try:
            self.redirectLink = "https://idealo.de" + soup.find("a", attrs={"class": "productOffers-listItemOfferLink"}).get("href")
        except:
            self.redirectLink = "unknown"

    def __str__(self) -> str:
        return "Offer for " + str(self.price) + " on " + self.shopName + "   -  " + self.redirectLink
    
    def __hash__(self) -> int:
        return hash(self.shopName)


