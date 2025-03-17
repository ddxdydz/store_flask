import requests
import io

API_KEY = {'apikey': 'AA61BEF91'}


def img_test():
    get_img_response = requests.get(
        'http://127.0.0.1:8000/api/get_img',
        headers=API_KEY, json={"path": "static/imgs/uploaded/1741412127726.jpg"}
    )
    if get_img_response.status_code != 200:
        print(f"Ошибка при получении изображения: {get_img_response.status_code} - {get_img_response.text}")
        return

    img_bytes = io.BytesIO(get_img_response.content)
    img_bytes.seek(0)

    send_img_response = requests.post(
        'http://127.0.0.1:8000/api/send_img',
        headers=API_KEY, files={'file': (f'1741409824428.jpg', img_bytes, 'image/jpeg')}
    )
    if send_img_response.status_code != 200:
        print(f"Ошибка при отправке изображения: {send_img_response.status_code} - {send_img_response.text}")
        return

    print(send_img_response.json())


if __name__ == "__main__":
    img_test()
