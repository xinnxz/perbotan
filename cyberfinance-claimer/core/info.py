import requests

from smart_airdrop_claimer import base
from core.headers import headers


def game_data(token, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/game/mining/gamedata"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        balance = data["message"]["userData"]["balance"]
        balance = int(float(balance))
        return balance
    except:
        return None
