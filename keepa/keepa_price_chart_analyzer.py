try:
    from item_filter import amz_headers as amz_headers
except:
    import amz_headers
from io import BytesIO
import requests
import numpy as np 
from PIL import Image


RELATIVE_HEIGHT = 300
WIDTH_FACTOR = 3
IMG_URL = "https://graph.keepa.com/pricehistory.png?asin={}&domain=de&amazon=0&range=30&width={w}&height={r}&type=1"

def get_keepa_img(asin:str):
    r = requests.get(IMG_URL.format(asin, r=RELATIVE_HEIGHT, w=WIDTH_FACTOR*30), headers=amz_headers.get_header())
    img_arr = np.array(Image.open(BytesIO(r.content)))
    return img_arr[:, :, 1]

def get_30_day_history(asin:str, current_price:float):
    img = get_keepa_img(asin)
    history = []
    for i in range(30):
        for k in range(WIDTH_FACTOR):
            w = []
            for j in range(RELATIVE_HEIGHT):
                if img[j, i*WIDTH_FACTOR + k] != 255:
                    w.append(RELATIVE_HEIGHT-j)
                    break
            if len(w) != 0:
                history.append(np.mean(w))

    relative_factor =  current_price / history[-1]
    # Logarithmic scaling
    history = [x * relative_factor for x in history]
    return history

def get_30_day_avg(asin:str, current_price:float):
    history = get_30_day_history(asin, current_price)
    return np.mean(history)



if __name__ == "__main__":
    # Test with multiple height accuracies
    # for i in range(100, 1000, 50):
    #      RELATIVE_HEIGHT = i
    #      print("Acc: ", i ," - ", get_30_day_avg("B0B11V46FF", 14.86))
    
    print(get_30_day_avg("1802537058",  2.89))


   # print(get_30_day_avg("B0B11V46FF", 14.86))
