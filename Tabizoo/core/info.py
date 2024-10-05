import requests

from smart_airdrop_claimer import base
from core.headers import headers


def get_info(data, proxies=None):
    url = "https://api.tabibot.com/api/user/v1/profile"

    try:
        response = requests.get(
            url=url, headers=headers(data=data), proxies=proxies, timeout=20
        )
        data = response.json()
        balance = data["data"]["user"]["coins"]
        level = data["data"]["user"]["level"]
        streak = data["data"]["user"]["streak"]

        base.log(
            f"{base.green}Balance: {base.white}{balance:,} - {base.green}Level: {base.white}{level} - {base.green}Streak: {base.white}{streak}"
        )
        return data
    except:
        return None
