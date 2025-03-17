import requests

BASE_URL = 'http://127.0.0.1:8000/api/cart_entries'
API_KEY = {'apikey': 'AA61BEF91'}
new_cart_entry_data = {
    'user_id': 1,
    'product_id': 20
}


def get_list():  # Пример запроса для получения всех записей корзины
    response = requests.get(BASE_URL, headers=API_KEY)
    print(f"get - status_code: {response.status_code}, json: {response.json()}")


def post():  # Пример запроса для добавления новой записи в корзину
    response = requests.post(BASE_URL, json=new_cart_entry_data, headers=API_KEY)
    print(f"pst - status_code: {response.status_code}, json: {response.json()}")


def get_one():  # Пример запроса для получения информации о конкретной записи в корзине
    user_id_to_get = new_cart_entry_data["user_id"]
    product_id_to_get = new_cart_entry_data["product_id"]
    response = requests.get(f'{BASE_URL}/{user_id_to_get}/{product_id_to_get}', headers=API_KEY)
    print(f"get - status_code: {response.status_code}, json: {response.json()}")


def put():  # Пример запроса для обновления записи в корзине
    user_id_to_update = new_cart_entry_data["user_id"]
    product_id_to_update = new_cart_entry_data["product_id"]
    update_cart_entry_data = {'count': 5}
    response = requests.put(f'{BASE_URL}/{user_id_to_update}/{product_id_to_update}',
                            json=update_cart_entry_data, headers=API_KEY)
    print(f"put - status_code: {response.status_code}, json: {response.json()}")


def delete():  # Пример запроса для удаления записи из корзины
    user_id_to_delete = new_cart_entry_data["user_id"]
    product_id_to_delete = new_cart_entry_data["product_id"]
    response = requests.delete(f'{BASE_URL}/{user_id_to_delete}/{product_id_to_delete}', headers=API_KEY)
    print(f"del - status_code: {response.status_code}, json: {response.json()}")


if __name__ == "__main__":
    get_list()
    post()
    get_one()
    put()
    delete()
