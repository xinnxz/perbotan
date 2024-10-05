import requests

from package.core.headers import headers
from package.core.info import balance
from package import base


def stake(token, stake_point, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users/stack-balance"
    payload = {"amount": stake_point}

    try:
        response = requests.post(
            url=url, headers=headers(token), json=payload, proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def process_stake(token, proxies=None):
    stake_point = balance(token=token, proxies=proxies)
    start_stake = stake(token=token, stake_point=stake_point, proxies=proxies)
    try:
        stacked_balance = start_stake["stackedBalance"]
        new_balance = start_stake["balance"]
        base.log(
            f"{base.white}Auto Stake: {base.green}Stake Remaining Points Success | Stacked Balance: {base.white}{stacked_balance} - {base.green}New Balance: {base.white}{new_balance}"
        )
    except:
        base.log(f"{base.white}Auto Stake: {base.red}Error")
