import requests
import random

from smart_airdrop_claimer import base
from core.headers import headers


def claim_ref(token, proxies=None):
    url = "https://api.mmbump.pro/v1/friends/claim"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        claimed = int(data["sum"])
        return claimed
    except:
        return 0


def process_claim_ref(token, proxies=None):
    claimed = claim_ref(token=token, proxies=proxies)
    if claimed > 0:
        base.log(f"{base.white}Auto Claim Ref: {base.green}Claimed {claimed:,} points")
    else:
        base.log(f"{base.white}Auto Claim Ref: {base.red}No point from ref")


def farming(token, proxies=None):
    url = "https://api.mmbump.pro/v1/farming"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), json={}, proxies=proxies, timeout=20
        )
        data = response.json()
        balance = data["balance"]
        base.log(f"{base.green}Balance: {base.white}{balance:,}")
        return data
    except:
        return None


def start_farming(token, proxies=None):
    url = "https://api.mmbump.pro/v1/farming/start"
    payload = {"status": "inProgress"}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["status"]
        return status
    except:
        return None


def finish_farming(token, tap, proxies=None):
    url = "https://api.mmbump.pro/v1/farming/finish"
    payload = {"tapCount": tap}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["code"]
        return status
    except:
        return None


def process_farming(token, proxies=None):
    tap = random.randint(1000000, 2000000)
    finish_status = finish_farming(token=token, tap=tap, proxies=proxies)
    if finish_status == 431:
        base.log(f"{base.white}Auto Farm: {base.red}Not time to claim yet")
    elif finish_status == 403:
        base.log(f"{base.white}Auto Farm: {base.yellow}Waiting to start farming")
        start_status = start_farming(token=token, proxies=proxies)
        if start_status == "inProgress":
            base.log(f"{base.white}Auto Farm: {base.green}Start farming success")
        else:
            base.log(f"{base.white}Auto Farm: {base.red}Start farming fail")
    else:
        base.log(f"{base.white}Auto Farm: {base.green}Claim success")
        start_status = start_farming(token=token, proxies=proxies)
        if start_status == "inProgress":
            base.log(f"{base.white}Auto Farm: {base.green}Start farming success")
        else:
            base.log(f"{base.white}Auto Farm: {base.red}Start farming fail")
