import requests
import random

from smart_airdrop_claimer import base
from core.headers import headers


def mine(token, count, proxies=None):
    url = "https://backend.babydogepawsbot.com/mine"
    payload = {"count": count}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()["user"]
        balance = data["balance"]
        energy = data["energy"]
        base.log(
            f"{base.green}Balance: {base.white}{balance:,} - {base.green}Available Energy: {base.white}{energy:,}"
        )
        return energy
    except:
        return None


def process_tap(token, proxies=None):
    while True:
        try:
            count = random.randint(200, 500)
            energy = mine(token=token, count=count, proxies=proxies)
            if energy < 100:
                base.log(
                    f"{base.white}Auto Tap: {base.red}Limit 100 energy reached. Stop!"
                )
                break
        except Exception as e:
            base.log(f"{base.white}Auto Tap: {base.red}Error - {e}")
            break
