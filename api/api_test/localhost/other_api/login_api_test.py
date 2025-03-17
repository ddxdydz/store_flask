import requests

API_KEY = {'apikey': 'AA61BEF91'}
BASE_URL = 'http://127.0.0.1:8000/api/check_authorization_data'


def correct_login_test():
    response1 = requests.post(
        BASE_URL,
        headers=API_KEY, json={"email": "user1@mail.ru", "password": "pw"}
    )
    if response1.status_code != 200:
        print(f"Ошибка: {response1.status_code} - {response1.text}")
        return
    print(response1.json()['result'] is True)


def wrong_login_test():
    response1 = requests.post(
        BASE_URL,
        headers=API_KEY, json={"email": "user1@mail.ru", "password": "pw11"}
    )
    if response1.status_code != 200:
        print(f"Ошибка: {response1.status_code} - {response1.text}")
        return
    print(response1.json()['result'] is False)


if __name__ == "__main__":
    correct_login_test()
    wrong_login_test()
