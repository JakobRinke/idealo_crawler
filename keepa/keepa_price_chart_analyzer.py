try:
    from keepa import amz_headers as amz_headers
except:
    import amz_headers
from io import BytesIO
import time
import requests
import numpy as np 
from PIL import Image
import pytesseract

RELATIVE_HEIGHT = 1800
WIF = 4
IMG_URL = "https://graph.keepa.com/pricehistory.png?asin={}&domain=de&amazon=0&range=30&width=120&height=1800&type=1"

RANGE_IMG_URL = "https://graph.keepa.com/pricehistory.png?asin={}&domain=de&amazon=0&range=30&width=120&height=1800&type=0"

def get_keepa_img(asin:str):
    r = requests.get(IMG_URL.format(asin), headers=amz_headers.get_header())
    try:
        img_arr = np.array(Image.open(BytesIO(r.content)))
        return img_arr[:, :, 1]
    except:
        return []

def to_int(s):
    # filter out non-numeric characters
    s = ''.join(filter(str.isdigit, s))
    if (s == ""):
        return -1
    return int(s)

def get_bottom_index(asin:str):
    r = requests.get(RANGE_IMG_URL.format(asin), headers=amz_headers.get_header())
    img_arr = np.array(Image.open(BytesIO(r.content)))
    start_x = 10
    end_x = 30
    start_y = 1758
    end_y = 1768
    for i in range(50):
        if img_arr[start_y-5, i][0] != 255:
            end_x = i
            break
    subimg = img_arr[start_y:end_y, start_x:end_x]

    # Image.fromarray(subimg).show()
    s = pytesseract.image_to_string(subimg, config='--psm 6')
    return to_int(s)



def get_30_day_history(asin:str, current_price:float):
    img = get_keepa_img(asin)
    if len(img) == 0:
        return None
    history = []
    for i in range(30):
            for j in range(RELATIVE_HEIGHT):
                if img[j, i*WIF+WIF-1] != 255:
                    history.append(RELATIVE_HEIGHT - j)
                    break
            else:
                if len(history) > 0:
                    history.append(history[-1])

    bottom = get_bottom_index(asin)

    if bottom == -1:
        return [-1]

    relative_factor =  (current_price - bottom) / history[-1]
    # Logarithmic scaling
    history = [x * relative_factor + bottom for x in history]
    return history

def get_30_day_avg(asin:str, current_price:float):
    history = get_30_day_history(asin, current_price)
    if history is None:
        return None
    return np.mean(history)



if __name__ == "__main__":
    print(get_30_day_avg("B0CV52JHNR", 2270))
    print(get_30_day_avg("B09T1P2B7J", 203.75))
