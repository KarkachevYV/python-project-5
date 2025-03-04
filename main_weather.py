import requests

def get_weather(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_github_user(username):
    url = f'https://github.com/KarkachYV/{username}'
    response = requests.get(url)
    if response.status_code == 200:
       return response.json()
    else:
       return None
    
def get_random_cat_image():
    try:
        return requests.get("https://api.thecatapi.com/v1/images/search").json()[0]['url']
    except (requests.RequestException, IndexError, KeyError):
        return None
