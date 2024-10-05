import requests

from smart_airdrop_claimer import base
from core.headers import headers
from core.info import get_info


def tap(token, taps, proxies=None):
    url = "https://api-clicker.ageofmars.io/v1/clicker/taps"
    payload = {"taps": taps}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        available_taps = data["data"]["availableTaps"]
        return available_taps
    except:
        return None


def start_collector(token, proxies=None):
    url = "https://api-clicker.ageofmars.io/v1/collector/start"
    payload = {}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["success"]
        return status
    except:
        return None


def claim_collector(token, proxies=None):
    url = "https://api-clicker.ageofmars.io/v1/collector/claim"
    payload = {}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["success"]
        return status
    except:
        return None


def process_tap(token, proxies=None):
    while True:
        collector_status, available_taps = get_info(token=token, proxies=proxies)

        if collector_status == "in_work":
            base.log(
                f"{base.white}Collector Status: {base.yellow}In Work - Not time to claim yet"
            )
            break
        elif collector_status == "completed":
            base.log(
                f"{base.white}Collector Status: {base.yellow}Completed - Waiting to claim"
            )
            claim_status = claim_collector(token=token, proxies=proxies)
            if claim_status:
                base.log(f"{base.white}Auto Claim: {base.green}Success")
            else:
                base.log(f"{base.white}Auto Claim: {base.red}Fail")
        elif collector_status == "pending":
            base.log(
                f"{base.white}Collector Status: {base.yellow}Pending - Waiting to tap and start collector"
            )
            while True:
                tap_left = tap(token=token, taps=available_taps, proxies=proxies)
                if tap_left > 0:
                    pass
                else:
                    base.log(f"{base.white}Auto Tap: {base.green}Success")
                    start_status = start_collector(token=token, proxies=proxies)
                    if start_status:
                        base.log(f"{base.white}Start Collector: {base.green}Success")
                        break
                    else:
                        base.log(f"{base.white}Start Collector: {base.red}Fail")
                        break
