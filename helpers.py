import requests
import random
import string
from faker import Faker

from urls import Urls

fake = Faker()


def generate_name():
    return fake.first_name()


def generate_login():
    return fake.text(10)


def generate_pass():
    return fake.password()


def genarate_courier_payload():
    fake_name = fake.first_name()
    fake_login = fake.text(10)
    fake_pass = fake.password()
    return {"login": fake_login, "password": fake_pass, "firstName": fake_name}


def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(
        'https://qa-scooter.praktikum-services.ru/api/v1/courier',
        data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass


def login_for_registered_courier():
    payload = register_new_courier_and_return_login_password()
    return payload[0]


def pass_for_registered_courier():
    payload = register_new_courier_and_return_login_password()
    return payload[1]


def delete_courier(courier_id):
    response = requests.delete(
        f"{Urls.URL_COURIER_CREATE}/{courier_id}")
    return response


def login_courier(login, password):
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(Urls.URL_COURIER_LOGIN, data=payload)
    return response


def create_test_order(color):
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "address1": fake.street_address(),
        "metroStation": 4,
        "phone": fake.phone_number(),
        "rentTime": 5,
        "deliveryDate": "2026-02-24",
        "comment": fake.text(10),
        "color": color
    }
