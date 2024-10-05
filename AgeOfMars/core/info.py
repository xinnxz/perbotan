import requests

from smart_airdrop_claimer import base
from core.headers import headers


def format_balances(balances):
    formatted_items = []
    for key, value in balances.items():
        formatted_key = (
            "".join([" " + char if char.isupper() else char for char in key])
            .title()
            .strip()
        )
        formatted_items.append(
            f"{base.green}{formatted_key}: {base.white}{int(value):,}"
        )

    return " - ".join(formatted_items)


def get_info(token, proxies=None):
    url = "https://api-clicker.ageofmars.io/v1/clicker/info"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        available_taps = data["data"]["availableTaps"]

        balances = data["data"]["balances"]
        base.log(format_balances(balances=balances))

        collector_status = data["data"]["collector"]["status"]

        return collector_status, available_taps
    except:
        return None
