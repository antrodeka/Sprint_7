import requests
import allure
from http import HTTPStatus

from urls import Urls


class TestOrderList:
    @allure.title(
            "Список заказов возвращается с типом данных словарь со списком")
    def test_get_order_list_success(self):
        response = requests.get(Urls.URL_GET_ORDERS_LIST)
        data = response.json()
        orders = data["orders"]
        assert (response.status_code == HTTPStatus.OK and
                isinstance(data, dict) and isinstance(orders, list))
