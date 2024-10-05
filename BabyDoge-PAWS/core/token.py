import requests

from smart_airdrop_claimer import base
from core.headers import headers


def get_token(data, proxies=None):
    url = "https://backend.babydogepawsbot.com/authorize"

    try:
        response = requests.post(
            url=url, headers=headers(), data=data, proxies=proxies, timeout=20
        )
        data = response.json()
        balance = data["balance"]
        energy = data["energy"]
        doge_level = data["current_league"]
        profit_per_hour = data["profit_per_hour"]
        earn_per_tap = data["earn_per_tap"]
        token = data["access_token"]

        base.log(
            f"{base.green}Balance: {base.white}{balance:,} - {base.green}Available Energy: {base.white}{energy:,}"
        )
        base.log(
            f"{base.green}Doge Level: {base.white}{doge_level} - {base.green}Profit per Hour: {base.white}{profit_per_hour} - {base.green}Earn per Tap: {base.white}{earn_per_tap}"
        )
        return token
    except:
        return None
