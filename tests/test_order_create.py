import allure
import pytest
import requests
from http import HTTPStatus

from urls import Urls
from helpers import create_test_order
from variables import KEY_TRACK


class TestOrderCreate:

    @allure.title("Проверка успешного создания заказа с цветами {color}")
    @pytest.mark.parametrize('color', [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_order_create_with_diff_colors_success(self, color):
        payload = create_test_order(color)
        response = requests.post(Urls.URL_ORDER_CREATE, json=payload)
        assert (response.status_code == HTTPStatus.CREATED and
                KEY_TRACK in response.json())
