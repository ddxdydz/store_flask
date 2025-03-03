import requests

# BASE_URL = 'https://zil10.pythonanywhere.com/api/orders'
BASE_URL = 'http://127.0.0.1:8000/api/order_entries'
API_KEY = {'apikey': 'AA61BEF91'}

# Пример запроса для получения списка заказов
response_get_all_orders = requests.get(BASE_URL, headers=API_KEY)
if response_get_all_orders.status_code == 200:
    print('Список заказов:', response_get_all_orders.json())
else:
    print('Ошибка при получении списка заказов:', response_get_all_orders.status_code)
next_id = max(response_get_all_orders.json()["orders"], key=lambda elem: elem["id"])["id"] + 1

# Пример запроса для создания нового заказа
new_order_data = {
    'user_id': 1,
    'description': 'Заказ на новый телефон'
}
response_post_order = requests.post(BASE_URL, json=new_order_data, headers=API_KEY)
if response_post_order.status_code == 200:
    print('Заказ создан:', response_post_order.json())
else:
    print('Ошибка при создании заказа:', response_post_order.status_code)

# Пример запроса для получения информации о конкретном заказе
order_id_to_get = next_id
response_get_order = requests.get(f'{BASE_URL}/{order_id_to_get}', headers=API_KEY)
if response_get_order.status_code == 200:
    print('Полученный заказ:', response_get_order.json())
else:
    print('Ошибка при получении заказа:', response_get_order.status_code)

# Пример запроса для обновления заказа
order_id_to_update = next_id
update_order_data = {
    'user_id': 1,
    'description': 'Обновленный заказ на новый телефон'
}
response_update_order = requests.put(f'{BASE_URL}/{order_id_to_update}', json=update_order_data, headers=API_KEY)
if response_update_order.status_code == 200:
    print('Заказ обновлен:', response_update_order.json())
else:
    print('Ошибка при обновлении заказа:', response_update_order.status_code)

# Пример запроса для удаления заказа
order_id_to_delete = next_id
response_delete_order = requests.delete(f'{BASE_URL}/{order_id_to_delete}', headers=API_KEY)
if response_delete_order.status_code == 200:
    print('Заказ удален:', response_delete_order.json())
else:
    print('Ошибка при удалении заказа:', response_delete_order.status_code)
