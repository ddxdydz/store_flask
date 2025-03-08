import requests

BASE_URL = 'http://127.0.0.1:8000/api/categories'
API_KEY = {'apikey': 'AA61BEF91'}

# Пример запроса для получения списка категорий
response_get_all_categories = requests.get(BASE_URL, headers=API_KEY)
if response_get_all_categories.status_code == 200:
    print('Список категорий:', response_get_all_categories.json())
else:
    print('Ошибка при получении списка категорий:', response_get_all_categories.status_code)
next_id = max(response_get_all_categories.json()["categories"], key=lambda elem: elem["id"])["id"] + 1

# Пример запроса для создания новой категории
new_category_data = {
    'name': 'Электроника'
}
response_post_category = requests.post(BASE_URL, json=new_category_data, headers=API_KEY)
if response_post_category.status_code == 200:
    print('Категория создана:', response_post_category.json())
else:
    print('Ошибка при создании категории:', response_post_category.status_code)

# Пример запроса для получения информации о конкретной категории
category_id_to_get = next_id
response_get_category = requests.get(f'{BASE_URL}/{category_id_to_get}', headers=API_KEY)
if response_get_category.status_code == 200:
    print('Полученная категория:', response_get_category.json())
else:
    print('Ошибка при получении категории:', response_get_category.status_code)

# Пример запроса для обновления категории
category_id_to_update = next_id
update_category_data = {
    'name': 'Бытовая техника'
}
response_update_category = requests.put(f'{BASE_URL}/{category_id_to_update}', json=update_category_data, headers=API_KEY)
if response_update_category.status_code == 200:
    print('Категория обновлена:', response_update_category.json())
else:
    print('Ошибка при обновлении категории:', response_update_category.status_code)

# Пример запроса для удаления категории
category_id_to_delete = next_id
response_delete_category = requests.delete(f'{BASE_URL}/{category_id_to_delete}', headers=API_KEY)
if response_delete_category.status_code == 200:
    print('Категория удалена:', response_delete_category.json())
else:
    print('Ошибка при удалении категории:', response_delete_category.status_code)
