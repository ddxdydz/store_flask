import requests

# BASE_URL = 'https://zil10.pythonanywhere.com/api/users'
BASE_URL = 'http://127.0.0.1:8000/api/users'
API_KEY = {'apikey': 'AA61BEF91'}

# Пример запроса для получения списка пользователей
response_get_all = requests.get(BASE_URL, headers=API_KEY)
if response_get_all.status_code == 200:
    print('Список пользователей:', response_get_all.json())
else:
    print('Ошибка при получении списка пользователей:', response_get_all.status_code)
next_id = max(response_get_all.json()["users"], key=lambda elem: elem["id"])["id"] + 1

# Пример запроса для создания нового пользователя
new_user_data = {
    'name': 'Новый Пользователь',
    'email': 'newuser@example.com',
    'password': 'securepassword',
    'role_id': 1,
    'balance': 100.0,
    'about': 'Информация о новом пользователе'
}
response_post = requests.post(BASE_URL, json=new_user_data, headers=API_KEY)
if response_post.status_code == 200:
    print('Пользователь создан:', response_post.json())
else:
    print('Ошибка при создании пользователя:', response_post.status_code)

# Пример запроса для обновления пользователя
user_id_to_update = 6
update_data = {
    'password': 'new_password',
    'role_id': 2,
    'balance': 150.0,
    'about': 'Обновленная информация о пользователе',
    'profile_img_path': 'path/to/new/image.png'
}
response_update = requests.put(f'{BASE_URL}/{user_id_to_update}', json=update_data, headers=API_KEY)
if response_update.status_code == 200:
    print('Пользователь обновлен:', response_update.json())
else:
    print('Ошибка при обновлении пользователя:', response_update.status_code)

# Пример запроса для получения информации о конкретном пользователе
user_id_to_get = 6
response_get = requests.get(f'{BASE_URL}/{user_id_to_get}', headers=API_KEY)
if response_get.status_code == 200:
    print('Полученный пользователь:', response_get.json())
else:
    print('Ошибка при получении пользователя:', response_get.status_code)

# Пример запроса для удаления пользователя
user_id_to_delete = 6
response_delete = requests.delete(f'{BASE_URL}/{user_id_to_delete}', headers=API_KEY)
if response_delete.status_code == 200:
    print('Пользователь удален:', response_delete.json())
else:
    print('Ошибка при удалении пользователя:', response_delete.status_code)
