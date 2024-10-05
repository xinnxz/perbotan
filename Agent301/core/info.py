import requests

from smart_airdrop_claimer import base
from core.headers import headers


def get_info(data, proxies=None):
    url = "https://api.agent301.org/getMe"
    payload = {"referrer_id": 0}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        balance = data["result"]["balance"]
        ticket = data["result"]["tickets"]

        base.log(
            f"{base.green}Balance: {base.white}{balance:,} - {base.green}Available ticket: {base.white}{ticket:,}"
        )

        return ticket
    except:
        return None
