import requests
import time
import random

from package.core.headers import headers
from package import base


def start_tapping(token, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users/start-tapping"
    now = int(time.time() * 1000)
    payload = {"dateStartMs": now}

    try:
        response = requests.post(
            url=url, headers=headers(token), json=payload, proxies=proxies, timeout=20
        )
        data = response.json()["token"]
        return data
    except:
        return None


def save_tap_balance(token, tap_balance, tap_token, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users/save-tap-balance"
    payload = {"tapBalance": tap_balance, "token": tap_token}

    try:
        response = requests.post(
            url=url, headers=headers(token), json=payload, proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def process_tap(token, proxies=None):
    while True:
        tap_balance = random.randint(1000, 2000)
        tap_token = start_tapping(token=token, proxies=proxies)
        if tap_token:
            tap_balance = save_tap_balance(
                token=token,
                tap_balance=tap_balance,
                tap_token=tap_token,
                proxies=proxies,
            )
            if tap_balance:
                balance = tap_balance["balance"]
                energy = tap_balance["energy"]
                base.log(
                    f"{base.white}Auto Tap: {base.green}Sucess {base.white}| {base.green}New balance: {base.white}{balance} - {base.green}Energy left: {base.white}{energy}"
                )
                if energy < 100:
                    base.log(
                        f"{base.white}Auto Tap: {base.red}Limit 100 energy reached. Stop!"
                    )
                    break
            else:
                base.log(f"{base.white}Auto Tap: {base.red}Get tap balance error!")
                break
        else:
            base.log(f"{base.white}Auto Tap: {base.red}Get tap token error!")
            break
