import requests

BASE_URL = 'http://127.0.0.1:8000/api/products'
API_KEY = {'apikey': 'AA61BEF91'}

# Пример запроса для получения списка продуктов
response_get_all_products = requests.get(BASE_URL, headers=API_KEY)
if response_get_all_products.status_code == 200:
    print('Список продуктов:', response_get_all_products.json())
else:
    print('Ошибка при получении списка продуктов:', response_get_all_products.status_code)
next_id = max(response_get_all_products.json()["products"], key=lambda elem: elem["id"])["id"] + 1

# Пример запроса для создания нового продукта
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
response_post_product = requests.post(BASE_URL, json=new_product_data, headers=API_KEY)
if response_post_product.status_code == 200:
    print('Продукт создан:', response_post_product.json())
else:
    print('Ошибка при создании продукта:', response_post_product.status_code)

# Пример запроса для получения информации о конкретном продукте
product_id_to_get = next_id
response_get_product = requests.get(f'{BASE_URL}/{product_id_to_get}', headers=API_KEY)
if response_get_product.status_code == 200:
    print('Полученный продукт:', response_get_product.json())
else:
    print('Ошибка при получении продукта:', response_get_product.status_code)

# Пример запроса для обновления продукта
product_id_to_update = next_id
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
response_update_product = requests.put(f'{BASE_URL}/{product_id_to_update}', json=update_data, headers=API_KEY)
if response_update_product.status_code == 200:
    print('Продукт обновлен:', response_update_product.json())
else:
    print('Ошибка при обновлении продукта:', response_update_product.status_code)


# Пример запроса для удаления продукта
product_id_to_delete = next_id
response_delete_product = requests.delete(f'{BASE_URL}/{product_id_to_delete}', headers=API_KEY)
if response_delete_product.status_code == 200:
    print('Продукт удален:', response_delete_product.json())
else:
    print('Ошибка при удалении продукта:', response_delete_product.status_code)
