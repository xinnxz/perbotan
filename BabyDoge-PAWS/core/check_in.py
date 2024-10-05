import requests

from smart_airdrop_claimer import base
from core.headers import headers


def daily_bonus(token, proxies=None):
    url = "https://backend.babydogepawsbot.com/getDailyBonuses"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def claim_daily_bonus(token, proxies=None):
    url = "https://backend.babydogepawsbot.com/pickDailyBonus"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def process_check_in(token, proxies=None):
    get_daily_bonus = daily_bonus(token=token, proxies=proxies)
    if get_daily_bonus:
        has_available = get_daily_bonus["has_available"]
        if has_available:
            claim = claim_daily_bonus(token=token, proxies=proxies)
            if claim:
                base.log(f"{base.white}Auto Check-in: {base.green}Success")
            else:
                base.log(f"{base.white}Auto Check-in: {base.red}Claim fail")
        else:
            base.log(f"{base.white}Auto Check-in: {base.red}Claimed")
    else:
        base.log(f"{base.white}Auto Check-in: {base.red}Get claim status error")
