import pytest
import requests
import random
import json
import string
import pytest

USERNAME = "TestUserName4"
USER_URL = "http://bzteltestapi.pythonanywhere.com/users"


@pytest.fixture()
def change_password_back_after_test():
    yield
    payload = json.dumps({
        "username": USERNAME,
        "old_password": "newpassword",
        "password1": "testpassword123!",
        "password2": "testpassword123!"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    requests.request("PUT", USER_URL, headers=headers, data=payload)


class TestUSerCreation:
    RANDOM_STRING = string.ascii_letters + string.digits  # Для генерации случайных строк

    def test_user_creation_is_successful(self):
        """Проверка создания пользователя"""
        payload = json.dumps({
            "username": USERNAME,
            "password1": "testpassword123!",
            "password2": "testpassword123!"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", USER_URL, headers=headers, data=payload)
        response_body = response.json()

        assert response.status_code == 201
        assert response_body.get('result') == f"New user {USERNAME} successfully created"

    def test_user_exists(self):
        payload = json.dumps({
            "username": USERNAME,
            "password1": "testpassword123!",
            "password2": "testpassword123!"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", USER_URL, headers=headers, data=payload)
        response_body = response.json()

        assert response.status_code == 400
        assert response_body.get('message') == "User Already exist"

    def test_password_length_more_than_permissible(self):
        random_password_21 = ''.join(random.choice(self.RANDOM_STRING) for _ in range(21))

        payload = json.dumps({
            "username": USERNAME,
            "password1": random_password_21,
            "password2": random_password_21
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", USER_URL, headers=headers, data=payload)
        response_body = response.json()
        assert response.status_code == 400
        assert response_body.get('message') == "Password to long. Max length is 20 chars"

    def test_password_length_less_than_permissible(self):
        random_password_5 = ''.join(random.choice(self.RANDOM_STRING) for _ in range(5))

        payload = json.dumps({
            "username": USERNAME,
            "password1": random_password_5,
            "password2": random_password_5
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", USER_URL, headers=headers, data=payload)
        response_body = response.json()
        assert response.status_code == 400
        assert response_body.get('message') == "Password to short. Min length is 6 chars"

    def test_password_check_work(self):
        payload = json.dumps({
            "username": USERNAME,
            "password1": "testpassword123!",
            "password2": "testpassword"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", USER_URL, headers=headers, data=payload)
        response_body = response.json()
        assert response.status_code == 400
        assert response_body.get('message') == "Passwords does not match"

    def test_password_change_work(self, change_password_back_after_test):
        payload = json.dumps({
            "username": USERNAME,
            "old_password": "testpassword123!",
            "password1": "newpassword",
            "password2": "newpassword"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("PUT", USER_URL, headers=headers, data=payload)
        response_body = response.json()
        assert response.status_code == 202
        assert response_body.get('result') == "Password successfully updated!"
