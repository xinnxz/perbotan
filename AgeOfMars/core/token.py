import requests

from smart_airdrop_claimer import base
from core.headers import headers


def get_token(data, proxies=None):
    url = "https://api-clicker.ageofmars.io/v1/auth/login"
    payload = {"initData": data}

    try:
        response = requests.post(
            url=url, headers=headers(), json=payload, proxies=proxies, timeout=20
        )
        data = response.json()
        token = data["data"]["accessToken"]
        return token
    except:
        return None
