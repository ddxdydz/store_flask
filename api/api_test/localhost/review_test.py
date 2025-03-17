import requests

from api.api_test.get_last_id import get_last_id

BASE_URL = 'http://127.0.0.1:8000/api/reviews'
API_KEY = {'apikey': 'AA61BEF91'}


def get_list():  # Пример запроса для получения списка отзывов
    response = requests.get(BASE_URL, headers=API_KEY)
    print(f"get - status_code: {response.status_code}, json: {response.json()}")


def post():  # Пример запроса для создания нового отзыва
    new_review_data = {
        'user_id': 1,
        'product_id': 2,
        'score': 5,
        'about': 'Отличный'
    }
    response = requests.post(BASE_URL, json=new_review_data, headers=API_KEY)
    print(f"pst - status_code: {response.status_code}, json: {response.json()}")
    return response.json()["review_id"]


def get_one(review_id=None):  # Пример запроса для получения информации о конкретном отзыве
    if review_id is None:
        review_id = get_last_id(BASE_URL, API_KEY, "reviews")
    response = requests.get(f'{BASE_URL}/{review_id}', headers=API_KEY)
    print(f"get - status_code: {response.status_code}, json: {response.json()}")


def put(review_id=None):  # Пример запроса для обновления отзыва
    if review_id is None:
        review_id = get_last_id(BASE_URL, API_KEY, "reviews")
    update_review_data = {
            'score': 4,
            'about': 'Хороший'
    }
    response = requests.put(f'{BASE_URL}/{review_id}', json=update_review_data, headers=API_KEY)
    print(f"put - status_code: {response.status_code}, json: {response.json()}")


def delete(review_id=None):  # Пример запроса для удаления отзыва
    if review_id is None:
        review_id = get_last_id(BASE_URL, API_KEY, "reviews")
    response = requests.delete(f'{BASE_URL}/{review_id}', headers=API_KEY)
    print(f"del - status_code: {response.status_code}, json: {response.json()}")


if __name__ == "__main__":
    get_list()
    output_id = post()
    get_one(output_id)
    put(output_id)
    delete(output_id)
