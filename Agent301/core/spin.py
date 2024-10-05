import requests
import time

from smart_airdrop_claimer import base
from core.headers import headers
from core.info import get_info


def spin(data, proxies=None):
    url = "https://api.agent301.org/wheel/spin"
    payload = {}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        return data
    except:
        return None


def process_spin_wheel(data, proxies=None):
    while True:
        ticket = get_info(data=data, proxies=proxies)
        if ticket is not None:
            if ticket > 0:
                start_spinning = spin(data=data, proxies=proxies)
                status = start_spinning["ok"]
                if status:
                    reward = start_spinning["result"]["reward"]
                    balance = start_spinning["result"]["balance"]
                    toncoin = start_spinning["result"]["toncoin"]
                    notcoin = start_spinning["result"]["notcoin"]
                    tickets = start_spinning["result"]["tickets"]

                    base.log(
                        f"{base.white}Auto Spin Wheel: {base.green}Sucess | {base.green}Reward: {base.white}{reward} - {base.green}Balance: {base.white}{balance:,} - {base.green}Toncoin: {base.white}{toncoin:,} - {base.green}Notcoin: {base.white}{notcoin:,} - {base.green}Tickets: {base.white}{tickets:,}"
                    )
                    time.sleep(5)
                else:
                    base.log(f"{base.white}Auto Spin Wheel: {base.red}Fail")
                    break
            else:
                base.log(f"{base.white}Auto Spin Wheel: {base.red}No ticket available")
                break
        else:
            base.log(f"{base.white}Auto Spin Wheel: {base.red}Ticket data not found!")
            break
