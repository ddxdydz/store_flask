import requests

BASE_URL = 'http://127.0.0.1:8000/api/reviews'
API_KEY = {'apikey': 'AA61BEF91'}

# Пример запроса для получения списка отзывов
response_get_all_reviews = requests.get(BASE_URL, headers=API_KEY)
if response_get_all_reviews.status_code == 200:
    print('Список отзывов:', response_get_all_reviews.json())
else:
    print('Ошибка при получении списка отзывов:', response_get_all_reviews.status_code)
next_id = max(response_get_all_reviews.json()["reviews"], key=lambda elem: elem["id"])["id"] + 1

# Пример запроса для создания нового отзыва
new_review_data = {
    'user_id': 1,
    'product_id': 2,
    'score': 5,
    'about': 'Отличный продукт!'
}
response_post_review = requests.post(BASE_URL, json=new_review_data, headers=API_KEY)
if response_post_review.status_code == 200:
    print('Отзыв создан:', response_post_review.json())
else:
    print('Ошибка при создании отзыва:', response_post_review.status_code)

# Пример запроса для получения информации о конкретном отзыве
review_id_to_get = next_id
response_get_review = requests.get(f'{BASE_URL}/{review_id_to_get}', headers=API_KEY)
if response_get_review.status_code == 200:
    print('Полученный отзыв:', response_get_review.json())
else:
    print('Ошибка при получении отзыва:', response_get_review.status_code)

# Пример запроса для обновления отзыва
review_id_to_update = next_id
update_review_data = {
    'score': 4,
    'about': 'Хороший продукт, но есть недочеты.'
}
response_update_review = requests.put(f'{BASE_URL}/{review_id_to_update}', json=update_review_data, headers=API_KEY)
if response_update_review.status_code == 200:
    print('Отзыв обновлен:', response_update_review.json())
else:
    print('Ошибка при обновлении отзыва:', response_update_review.status_code)

# Пример запроса для удаления отзыва
review_id_to_delete = next_id
response_delete_review = requests.delete(f'{BASE_URL}/{review_id_to_delete}', headers=API_KEY)
if response_delete_review.status_code == 200:
    print('Отзыв удален:', response_delete_review.json())
else:
    print('Ошибка при удалении отзыва:', response_delete_review.status_code)
