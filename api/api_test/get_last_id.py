import requests


def get_last_id(url, headers, json_key):
    response_get_all = requests.get(url, headers=headers).json()[json_key]
    if len(response_get_all) == 0:
        return 0
    return max(response_get_all, key=lambda elem: elem["id"])["id"]
