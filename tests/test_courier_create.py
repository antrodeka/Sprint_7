import pytest
import requests
import allure
from http import HTTPStatus

from helpers import (genarate_courier_payload, generate_login,
                     generate_name, generate_pass, login_courier,
                     delete_courier)
from urls import Urls
from variables import (ERROR_MESSAGE_BAD_REQUEST,
                       ERROR_MESSAGE_CONFLICT,
                       OK_TRUE)


class TestCourierCreate:
    @allure.title('Код 201 при создании курьера '
                  'с валидными логином, паролем')
    def test_create_courier_account_created(self):
        payload = genarate_courier_payload()
        with allure.step("Создаем нового курьера"):
            response = requests.post(Urls.URL_COURIER_CREATE, data=payload)
            response_login = login_courier(payload['login'],
                                           payload['password'])
            cour_id = response_login.text[0]
        with allure.step("Проверяем, что ответ содержит код 201, "
                         "и 'ok': True в тексте ответа"):
            assert (response.status_code == HTTPStatus.CREATED and
                    response.json() == OK_TRUE)
            delete_courier(cour_id)

    @allure.title('Код 409 при повторном создании курьера '
                  'с уже существующими данными')
    def test_create_duplicate_courier(self):
        payload = genarate_courier_payload()
        with allure.step("Создаем нового курьера"):
            requests.post(Urls.URL_COURIER_CREATE, data=payload)
        with allure.step("Создаем курьера повторно"):
            second_response = requests.post(Urls.URL_COURIER_CREATE,
                                            data=payload)
        with allure.step("Проверяем, что получен код 409"):
            assert (second_response.status_code == HTTPStatus.CONFLICT and
                    ERROR_MESSAGE_CONFLICT
                    in second_response.json()['message'])

    @allure.title('Код 400 при создании курьера с одним незаполненным полем')
    @pytest.mark.parametrize('fields', [{'login': '',
                                         'password': generate_pass(),
                                         'firstName': generate_name()},
                             {'login': generate_login(),
                              'password': '',
                              'firstName': generate_name()}
                             ])
    def test_create_courier_with_empty_fields(self, fields):
        with allure.step("Создаем нового курьера, передаем данные"
                         " с одним незаполенным полем"):
            response = requests.post(Urls.URL_COURIER_CREATE, data=fields)
        with allure.step("Проверяем, что пришел код 409"):
            assert (response.status_code == HTTPStatus.BAD_REQUEST and
                    ERROR_MESSAGE_BAD_REQUEST in response.json()['message'])
