import requests

from api.api_test.get_last_id import get_last_id

BASE_URL = 'http://127.0.0.1:8000/api/users'
API_KEY = {'apikey': 'AA61BEF91'}


def get_list():  # Пример запроса для получения списка пользователей
    response = requests.get(BASE_URL, headers=API_KEY)
    print(f"get - status_code: {response.status_code}, json: {response.json()}")


def post():  # Пример запроса для создания нового пользователя
    new_user_data = {
        'name': 'Новый Пользователь',
        'email': 'newuser@example.com',
        'password': 'securepassword',
        'role_id': 1,
        'balance': 100.0,
        'about': 'Информация о новом пользователе'
    }
    response = requests.post(BASE_URL, json=new_user_data, headers=API_KEY)
    print(f"pst - status_code: {response.status_code}, json: {response.json()}")
    return response.json()["user_id"]


def get_one(user_id=None):  # Пример запроса для обновления пользователя
    if user_id is None:
        user_id = get_last_id(BASE_URL, API_KEY, "users")
    update_data = {
        'password': 'new_password',
        'role_id': 2,
        'balance': 150.0,
        'about': 'Обновленная информация о пользователе'
    }
    response = requests.put(f'{BASE_URL}/{user_id}', json=update_data, headers=API_KEY)
    print(f"get - status_code: {response.status_code}, json: {response.json()}")


def put(user_id=None):  # Пример запроса для получения информации о конкретном пользователе
    if user_id is None:
        user_id = get_last_id(BASE_URL, API_KEY, "users")
    response = requests.get(f'{BASE_URL}/{user_id}', headers=API_KEY)
    print(f"put - status_code: {response.status_code}, json: {response.json()}")


def delete(user_id=None):  # Пример запроса для удаления пользователя
    if user_id is None:
        user_id = get_last_id(BASE_URL, API_KEY, "users")
    response = requests.delete(f'{BASE_URL}/{user_id}', headers=API_KEY)
    print(f"del - status_code: {response.status_code}, json: {response.json()}")


if __name__ == "__main__":
    get_list()
    output_id = post()
    get_one(output_id)
    put(output_id)
    delete(output_id)
