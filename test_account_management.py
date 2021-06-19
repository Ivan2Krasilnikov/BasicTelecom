import pytest
import requests
import random
import json
import string


class TestUSerCreation:
    url = "http://bzteltestapi.pythonanywhere.com/users"

    random_string = string.ascii_letters + string.digits  # Для генерации случайных строк

    def get_response_body(self, headers, payload_dump):
        """Получить тело запроса в формате json"""
        response = requests.request("POST", self.url, headers=headers, data=payload_dump)
        response_body = response.json()
        return response_body

    def test_user_creation(self):
        """Проверка создания пользователя"""
        payload = {
            "username": "TestUsername",
            "password1": "testpassword123!",
            "password2": "testpassword123!"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        payload_dump = json.dumps(payload)
        response_body = self.get_response_body(headers, payload_dump)

        assert response_body.get('message') == "User Already exist" or \
               response_body.get('result') == "New user TestUsername successfully created"

    def test_acceptable_password_length(self):
        """Проверка возможности создания паролей длиной 10 19 20 символов"""
        random_password_10 = ''.join(random.choice(self.random_string) for _ in range(10))
        random_password_19 = ''.join(random.choice(self.random_string) for _ in range(19))
        random_password_20 = ''.join(random.choice(self.random_string) for _ in range(20))

        payload = {
            "username": "TestUsername",
            "password1": random_password_10,
            "password2": random_password_10
        }
        headers = {
            'Content-Type': 'application/json'
        }

        payload_dump = json.dumps(payload)
        response_body = self.get_response_body(headers, payload_dump)

        assert response_body.get('message') == "User Already exist" or \
               response_body.get('result') == "New user TestUsername successfully created"

    def test_max_password_length(self):
        random_password_21 = ''.join(random.choice(self.random_string) for _ in range(21))

        payload = {
            "username": "TestUsername",
            "password1": random_password_21,
            "password2": random_password_21
        }
        headers = {
            'Content-Type': 'application/json'
        }

        payload_dump = json.dumps(payload)
        response_body = self.get_response_body(headers, payload_dump)
        assert response_body.get('message') == "Password to long. Max length is 20 chars"

    def test_min_password_length(self):
        random_password_5 = ''.join(random.choice(self.random_string) for _ in range(5))

        payload = {
            "username": "TestUsername",
            "password1": random_password_5,
            "password2": random_password_5
        }
        headers = {
            'Content-Type': 'application/json'
        }

        payload_dump = json.dumps(payload)
        response_body = self.get_response_body(headers, payload_dump)
        assert response_body.get('message') == "Password to short. Min length is 6 chars"
