import requests

# BASE_URL = 'https://zil10.pythonanywhere.com/api/card_entries'
BASE_URL = 'http://127.0.0.1:8000/api/card_entries'
API_KEY = {'apikey': 'AA61BEF91'}
new_card_entry_data = {
    'user_id': 1,
    'product_id': 20
}


def get_list():
    # Пример запроса для получения всех записей корзины
    response_get_all_card_entries = requests.get(BASE_URL, headers=API_KEY)
    if response_get_all_card_entries.status_code == 200:
        print('Список записей корзины:', response_get_all_card_entries.json())
    else:
        print('Ошибка при получении списка записей корзины:', response_get_all_card_entries.status_code)


def post():
    # Пример запроса для добавления новой записи в корзину
    response_post_card_entry = requests.post(BASE_URL, json=new_card_entry_data, headers=API_KEY)
    if response_post_card_entry.status_code == 200:
        print('Запись корзины создана:', response_post_card_entry.json())
    else:
        print('Ошибка при создании записи корзины:', response_post_card_entry.status_code)


def get_one():
    # Пример запроса для получения информации о конкретной записи в корзине
    user_id_to_get = new_card_entry_data["user_id"]
    product_id_to_get = new_card_entry_data["product_id"]
    response_get_card_entry = requests.get(f'{BASE_URL}/{user_id_to_get}/{product_id_to_get}', headers=API_KEY)
    if response_get_card_entry.status_code == 200:
        print('Полученная запись корзины:', response_get_card_entry.json())
    else:
        print('Ошибка при получении записи корзины:', response_get_card_entry.status_code)


def put():
    # Пример запроса для обновления записи в корзине
    user_id_to_update = new_card_entry_data["user_id"]
    product_id_to_update = new_card_entry_data["product_id"]
    update_card_entry_data = {
        'count': 5
    }
    response_update_card_entry = requests.put(f'{BASE_URL}/{user_id_to_update}/{product_id_to_update}', json=update_card_entry_data, headers=API_KEY)
    if response_update_card_entry.status_code == 200:
        print('Запись корзины обновлена:', response_update_card_entry.json())
    else:
        print('Ошибка при обновлении записи корзины:', response_update_card_entry.status_code)


def delete():
    # Пример запроса для удаления записи из корзины
    user_id_to_delete = new_card_entry_data["user_id"]
    product_id_to_delete = new_card_entry_data["product_id"]
    response_delete_card_entry = requests.delete(f'{BASE_URL}/{user_id_to_delete}/{product_id_to_delete}', headers=API_KEY)
    if response_delete_card_entry.status_code == 200:
        print('Запись корзины удалена:', response_delete_card_entry.json())
    else:
        print('Ошибка при удалении записи корзины:', response_delete_card_entry.status_code)


if __name__ == "__main__":
    get_list()
    post()
    get_one()
    put()
    delete()
