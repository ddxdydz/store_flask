import requests

from api.api_test.get_last_id import get_last_id

BASE_URL = 'http://127.0.0.1:8000/api/categories'
API_KEY = {'apikey': 'AA61BEF91'}


def get_list():  # Пример запроса для получения списка категорий
    response = requests.get(BASE_URL, headers=API_KEY)
    print(f"get - status_code: {response.status_code}, json: {response.json()}")


def post():  # Пример запроса для создания новой категории
    new_category_data = {'name': 'Электроника'}
    response = requests.post(BASE_URL, json=new_category_data, headers=API_KEY)
    print(f"pst - status_code: {response.status_code}, json: {response.json()}")
    return response.json()["category_id"]


def get_one(category_id=None):  # Пример запроса для получения информации о конкретной категории
    if category_id is None:
        category_id = get_last_id(BASE_URL, API_KEY, "categories")
    response = requests.get(f'{BASE_URL}/{category_id}', headers=API_KEY)
    print(f"get - status_code: {response.status_code}, json: {response.json()}")


def put(category_id=None):  # Пример запроса для обновления категории
    if category_id is None:
        category_id = get_last_id(BASE_URL, API_KEY, "categories")
    update_category_data = {'name': 'Бытовая техника'}
    response = requests.put(f'{BASE_URL}/{category_id}', json=update_category_data, headers=API_KEY)
    print(f"put - status_code: {response.status_code}, json: {response.json()}")


def delete(category_id=None):  # Пример запроса для удаления категории
    if category_id is None:
        category_id = get_last_id(BASE_URL, API_KEY, "categories")
    response = requests.delete(f'{BASE_URL}/{category_id}', headers=API_KEY)
    print(f"del - status_code: {response.status_code}, json: {response.json()}")


if __name__ == "__main__":
    get_list()
    output_id = post()
    get_one(output_id)
    put(output_id)
    delete(output_id)
