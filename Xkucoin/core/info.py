import requests

from smart_airdrop_claimer import base
from core.headers import headers


def get_info(cookie, proxies=None):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/summary?lang=en_US"

    try:
        response = requests.get(
            url=url,
            headers=headers(cookie=cookie),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        balance = data.get("data").get("availableAmount")
        molecule = data.get("data").get("feedPreview").get("molecule")

        base.log(f"{base.green}Balance: {base.white}{balance:,}")

        return molecule
    except:
        return None
