import pytest
import requests
import allure
from http import HTTPStatus

from helpers import (register_new_courier_and_return_login_password,
                     delete_courier,
                     pass_for_registered_courier,
                     login_for_registered_courier,
                     generate_login, generate_pass)
from urls import Urls
from variables import (ERROR_MESSAGE_BAD_REQUEST_AUTH,
                       ERROR_MESSAGE_NOT_FOUND,
                       KEY_ID)


class TestCourierLogin:
    @allure.title('Успешная авторизация с валидными данными')
    def test_courier_logged_in_sucсess(self):
        payload = register_new_courier_and_return_login_password()
        response = requests.post(Urls.URL_COURIER_LOGIN,
                                 data={"login": payload[0],
                                       "password": payload[1]})
        assert (response.status_code == HTTPStatus.OK and
                KEY_ID in response.text)
        delete_courier(response.json()["id"])

    @allure.title('Код 400 при авторизации с незаполненным полем логин/пароль')
    @pytest.mark.parametrize('login, password',
                             [{'', pass_for_registered_courier()},
                              {login_for_registered_courier(), ''}])
    def test_auth_with_out_pass_or_login_bad_request_error(self, login,
                                                           password):
        response = requests.post(Urls.URL_COURIER_LOGIN,
                                 data={"login": login, "password": password})
        assert (response.status_code == HTTPStatus.BAD_REQUEST and
                ERROR_MESSAGE_BAD_REQUEST_AUTH in response.text)

    @allure.title('Код 404 при авторизации несуществующим курьером')
    def test_auth_not_exist_courier(self):
        payload = {"login": generate_login, "password": generate_pass}
        response = requests.post(Urls.URL_COURIER_LOGIN, data=payload)
        assert (response.status_code == HTTPStatus.NOT_FOUND and
                ERROR_MESSAGE_NOT_FOUND in response.text)
