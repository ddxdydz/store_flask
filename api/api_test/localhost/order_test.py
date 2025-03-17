import requests

from api.api_test.get_last_id import get_last_id

BASE_URL = 'http://127.0.0.1:8000/api/order_entries'
API_KEY = {'apikey': 'AA61BEF91'}


def get_list():  # Пример запроса для получения списка заказов
    response = requests.get(BASE_URL, headers=API_KEY)
    print(f"get - status_code: {response.status_code}, json: {response.json()}")


def post():  # Пример запроса для создания нового заказа
    new_order_data = {
        'user_id': 1,
        'description': 'Заказ на новый телефон'
    }
    response = requests.post(BASE_URL, json=new_order_data, headers=API_KEY)
    print(f"pst - status_code: {response.status_code}, json: {response.json()}")
    return response.json()["order_id"]


def get_one(order_id=None):  # Пример запроса для получения информации о конкретном заказе
    if order_id is None:
        order_id = get_last_id(BASE_URL, API_KEY, "orders")
    response = requests.get(f'{BASE_URL}/{order_id}', headers=API_KEY)
    print(f"get - status_code: {response.status_code}, json: {response.json()}")


def put(order_id=None):  # Пример запроса для обновления заказа
    if order_id is None:
        order_id = get_last_id(BASE_URL, API_KEY, "orders")
    update_order_data = {
        'user_id': 1,
        'description': 'Обновленный заказ на новый телефон'
    }
    response = requests.put(f'{BASE_URL}/{order_id}', json=update_order_data, headers=API_KEY)
    print(f"put - status_code: {response.status_code}, json: {response.json()}")


def delete(order_id=None):  # Пример запроса для удаления заказа
    if order_id is None:
        order_id = get_last_id(BASE_URL, API_KEY, "orders")
    response = requests.delete(f'{BASE_URL}/{order_id}', headers=API_KEY)
    print(f"del - status_code: {response.status_code}, json: {response.json()}")


if __name__ == "__main__":
    get_list()
    output_id = post()
    get_one(output_id)
    put(output_id)
    delete(output_id)
