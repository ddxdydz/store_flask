import requests

from api.api_test.get_last_id import get_last_id

BASE_URL = 'http://127.0.0.1:8000/api/products'
API_KEY = {'apikey': 'AA61BEF91'}


def get_list():  # Пример запроса для получения списка продуктов
    response = requests.get(BASE_URL, headers=API_KEY)
    print(f"get - status_code: {response.status_code}, json: {response.json()}")


def post():  # Пример запроса для создания нового продукта
    new_product_data = {
        'user_id': 1,
        'category_id': 2,
        'name': 'Новый продукт',
        'short_description': 'Краткое описание',
        'long_description': 'Длинное описание',
        'specifications': 'Спецификации продукта',
        'promo': 'Промо информация',
        'price': 299.99
    }
    response = requests.post(BASE_URL, json=new_product_data, headers=API_KEY)
    print(f"pst - status_code: {response.status_code}, json: {response.json()}")
    return response.json()["product_id"]


def get_one(product_id=None):  # Пример запроса для получения информации о конкретном продукте
    if product_id is None:
        product_id = get_last_id(BASE_URL, API_KEY, "products")
    response = requests.get(f'{BASE_URL}/{product_id}', headers=API_KEY)
    print(f"get - status_code: {response.status_code}, json: {response.json()}")


def put(product_id=None):  # Пример запроса для обновления продукта
    if product_id is None:
        product_id = get_last_id(BASE_URL, API_KEY, "products")
    update_data = {
        'category_id': 3,
        'name': 'Обновленный продукт',
        'short_description': 'Обновленное краткое описание',
        'long_description': 'Обновленное длинное описание',
        'specifications': 'Обновленные спецификации',
        'promo': 'Обновленная промо информация',
        'price': 349.99,
        'price_title': 'Обновленная цена'
    }
    response = requests.put(f'{BASE_URL}/{product_id}', json=update_data, headers=API_KEY)
    print(f"put - status_code: {response.status_code}, json: {response.json()}")


def delete(product_id=None):  # Пример запроса для удаления продукта
    if product_id is None:
        product_id = get_last_id(BASE_URL, API_KEY, "products")
    response = requests.delete(f'{BASE_URL}/{product_id}', headers=API_KEY)
    print(f"del - status_code: {response.status_code}, json: {response.json()}")


if __name__ == "__main__":
    get_list()
    output_id = post()
    get_one(output_id)
    put(output_id)
    delete(output_id)
