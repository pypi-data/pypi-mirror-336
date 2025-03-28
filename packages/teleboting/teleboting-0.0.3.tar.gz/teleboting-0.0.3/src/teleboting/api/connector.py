from requests import request
from http import HTTPMethod
import os
import hashlib
import random
import string


def generate_csrf_token():
    # Generate a random string
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    # Get the user's session ID (you can customize this part based on your application)
    session_id = "1234567890"  # Placeholder session ID

    # Combine the random string and session ID to create the CSRF token
    csrf_token = hashlib.sha256((random_string + session_id).encode()).hexdigest()

    return csrf_token


API_URL = os.environ['API_URL']


class ApiConnector:
    BASE_URL = API_URL

    @classmethod
    def __request(
            cls,
            path: str,
            method: HTTPMethod,
            data: dict = None,
            user_tg_id: int = None,
            params=None
    ):
        if params is None:
            params = {}
        csrf_token = generate_csrf_token()

        headers = {
            'X-CSRFTOKEN': csrf_token
        }
        if user_tg_id:
            headers['X-USER-TG-ID'] = str(user_tg_id)
        if data and isinstance(data, str):
            headers['Content-Type'] = 'application/json'
        response = request(
            method=method,
            url=cls.BASE_URL + path,
            data=data,
            headers=headers,
            params=params
        )
        return response

    @classmethod
    def get(cls, *args, **kwargs):
        return cls.__request(*args, method=HTTPMethod.GET, **kwargs)

    @classmethod
    def post(cls, *args, **kwargs):
        return cls.__request(*args, method=HTTPMethod.POST, **kwargs)
