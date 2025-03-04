import pytest
import requests
from main_random_img_cat import get_random_cat_image  

def test_get_random_cat_image_success(mocker):
    mocker.patch('requests.get', return_value=mocker.Mock(json=lambda: [{'url': 'https://example.com/cat.jpg'}]))
    assert get_random_cat_image() == 'https://example.com/cat.jpg'

def test_get_random_cat_image_failure(mocker):
    mocker.patch('requests.get', side_effect=requests.RequestException)
    assert get_random_cat_image() is None

