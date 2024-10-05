import requests

from smart_airdrop_claimer import base
from core.headers import headers
from core.info import get_info


def get_mining_info(data, proxies=None):
    url = "https://api.tabibot.com/api/mining/v1/info"

    try:
        response = requests.get(
            url=url, headers=headers(data=data), proxies=proxies, timeout=20
        )
        data = response.json()
        rate = data["data"]["mining_data"]["rate"]
        referral_rate = data["data"]["mining_data"]["referral_rate"]
        top_limit = data["data"]["mining_data"]["top_limit"]
        current = data["data"]["mining_data"]["current"]

        base.log(
            f"{base.green}Mining Rate: {base.white}{rate:,} - {base.green}Refferal Bonus: {base.white}{referral_rate:,} - {base.green}Limit: {base.white}{top_limit:,} - {base.green}Mined: {base.white}{current:,}"
        )
        return data
    except:
        return None


def claim(data, proxies=None):
    url = "https://api.tabibot.com/api/mining/v1/claim"

    try:
        response = requests.post(
            url=url, headers=headers(data=data), proxies=proxies, timeout=20
        )
        data = response.json()
        status = data["data"]
        return status
    except:
        return None


def process_claim(data, proxies=None):
    get_mining_info(data=data, proxies=proxies)
    claim_status = claim(data=data, proxies=proxies)
    if claim_status:
        base.log(f"{base.white}Auto Claim: {base.green}Success")
        get_info(data=data, proxies=proxies)
    else:
        base.log(f"{base.white}Auto Claim: {base.red}Not time to claim yet")
