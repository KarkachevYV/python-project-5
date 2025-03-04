#main_random_img_cat.py
import requests

def get_random_cat_image():
    try:
        return requests.get("https://api.thecatapi.com/v1/images/search").json()[0]['url']
    except (requests.RequestException, IndexError, KeyError):
        return None
