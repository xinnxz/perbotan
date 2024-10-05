import requests

from package.core.headers import headers


def users(token, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users"

    try:
        response = requests.get(
            url=url, headers=headers(token), proxies=proxies, timeout=20
        )
        data = response.json()["minedCoins"]
        return data
    except:
        return None


def miner(token, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/inventory/user/miner"

    try:
        response = requests.get(
            url=url, headers=headers(token), proxies=proxies, timeout=20
        )
        data = response.json()
        name = data["name"]
        level = data["level"]
        tap = data["tap"]
        energy_per_tap = data["energyPerTap"]
        energy = data["energy"]
        return name, level, tap, energy_per_tap, energy
    except:
        return None


def balance(token, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users/balance"

    try:
        response = requests.get(
            url=url, headers=headers(token), proxies=proxies, timeout=20
        )
        data = response.json()["balance"]
        return data
    except:
        return None


def my_cards(token, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/inventory/user/cards"

    try:
        response = requests.get(
            url=url, headers=headers(token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None
