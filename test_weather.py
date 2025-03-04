import pytest
import requests
from main_weather import get_weather, get_github_user , get_random_cat_image   
from config import CAT_API_KEY

def test_get_weather(mocker):
   mock_get = mocker.patch('main_weather.requests.get')

   # Создаем мок-ответ для успешного запроса
   mock_get.return_value.status_code = 200
   mock_get.return_value.json.return_value = {
       'weather': [{'description': 'clear sky'}],
       'main_weather': {'temp': 282.55}
   }

   api_key = 'CAT_API_KEY'
   city = 'London'
   weather_data = get_weather(api_key, city)

   assert weather_data == {
       'weather': [{'description': 'clear sky'}],
       'main_weather': {'temp': 282.55}
   }

def test_get_weather_with_errors(mocker):
   mock_get = mocker.patch('main_weather.requests.get')

   # Создаем мок-ответ для неуспешного запроса
   mock_get.return_value.status_code = 404

   api_key = 'CAT_API_KEY'
   city = 'London'
   weather_data = get_weather(api_key, city)

   assert weather_data is None

def test_get_github_user(mocker):
   mock_get = mocker.patch('main_weather.requests.get')
   mock_get.return_value.status_code = 200
   mock_get.return_value.json.return_value = {
    'login' : 'KarkachevYV',
    'id' : 46364058,
    'name' : 'Karkach'
   }

   user_data = get_github_user('KarkachevYV')

   assert user_data == {
    'login' : 'KarkachevYV',
    'id' : 46364058,
    'name' : 'Karkach'
   }


def test_get_random_cat_image_success(mocker):
    mocker.patch('requests.get', return_value=mocker.Mock(json=lambda: [{'url': 'https://example.com/cat.jpg'}]))
    assert get_random_cat_image() == 'https://example.com/cat.jpg'

def test_get_random_cat_image_failure(mocker):
    mocker.patch('requests.get', side_effect=requests.RequestException)
    assert get_random_cat_image() is None

