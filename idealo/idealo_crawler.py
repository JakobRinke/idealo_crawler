# selenium 4.0
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from undetected_chromedriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from idealo.idealo_item import IdealoItemHead
from idealo.return_thread import ReturnThread
import time
from selenium.webdriver.chrome.options import Options
import json
import traceback

IDEALO_URL = "https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={}"
IDEALO_SEARCH_URL = "https://www.idealo.de/csr/api/v2/modules/searchResult?categoryId={0}&locale=de_DE&pageIndex={1}"


class IdealoCategoryCrawler ():

    def __init__(self, categoryID=-1, categoryName=""):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-oopr-debug-crash-dump")
        options.add_argument("--no-crash-upload")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-low-res-tiling")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
    
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
   
        if categoryID != -1:
            self.categoryID = categoryID
        else:
            self.driver.get(IDEALO_URL.format(categoryName))
            self.categoryID = self.driver.current_url.split(".html")[0].split("/")[-1]
            print(self.categoryID)
        self.page_index = 0
        self.itemcache = []
        self.get_next_chunk()

    def __iter__(self):
        self.page_index = 0
        self.itemcache = []
        return self

    def get_next_chunk(self):
        self.itemcache = []
        try:
            self.driver.get(IDEALO_SEARCH_URL.format(self.categoryID, self.page_index))
            src = self.driver.page_source
            try:
                data = json.loads(src, strict=False)
            except:
                data = json.loads(self.driver.find_element(By.TAG_NAME, "pre").text, strict=False)
            jsonItems = data["items"]
            for item in jsonItems:
                self.itemcache.append(IdealoItemHead(item["title"], item["offerInfo"]["formattedPrice"], item["href"], item["id"]))
            self.page_index += 1
        except:
            self.end()

    def end(self):
        self.driver.quit()
        self.itemcache = []
        raise StopIteration    
    

    def __next__(self):     
        if len(self.itemcache) == 0:
            self.get_next_chunk()
            return next(self)
        else:
            return self.itemcache.pop().get_real_item(self.driver)
    

            
def load_articles(n:int, category:str):
    items = []
    try:
        crawler = IdealoCategoryCrawler(categoryID=category)
    except Exception as e:
        print(e)
        return items
    for i in range(n):
        try:
            items.append(next(crawler))
        except StopIteration:
            print("StopIteration")
            break
    return items

def single_threaded_category_search(category:str, onItem):
    items = []
    try:
        crawler = IdealoCategoryCrawler(categoryID=category)
    except Exception as e:
        #print(e)
        # print stack trace
        # traceback.print_exc()

        return items
    for item in crawler:
        onItem(item, crawler.driver)
        items.append(item)
    return items


def multi_threaded_category_search(categories:list, onItem):
    threads = []
    for category in categories:
        t = ReturnThread(target=single_threaded_category_search, args=(category, onItem))
        threads.append(t)
        t.start()
    return [item for t in threads for item in t.join()]


if __name__ == "__main__":
    itemnumber = 70
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
    threads = []
    start_time = time.time()
    for category in category_ids:
        t = ReturnThread(target=load_articles, args=(itemnumber, category))
        threads.append(t)
        t.start()

    k = 0
    for t in threads:
        k += len(t.join() or [])
    
    print("Total time: ", time.time() - start_time)
    print("Items Per Second: ", k / (time.time() - start_time))




