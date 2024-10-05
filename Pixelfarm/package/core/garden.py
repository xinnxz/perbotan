import requests
from package.core.headers import headers
from package import base


def info(token, proxies=None):
    url = f"https://api.pixelfarm.app/user"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def claim(token, proxies=None):
    url = f"https://api.pixelfarm.app/user/claim"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def extract_garden_info(user_info):
    try:
        gem = user_info["data"]["gem_amount"]
        base.log(f"{base.green}GEM: {base.white}{gem}")
        crops = user_info["data"]["crops"]
        for crop in crops:
            tree_type = crop["tree_type"]
            fruit_total = crop["fruit_total"]
            base.log(
                f"{base.green}Tree: {base.white}{tree_type} - {base.green}Fruit: {base.white}{fruit_total}"
            )
    except:
        base.log(f"{base.red}Required info not found!")


def process_claim(token, proxies=None):
    start_claim = claim(token=token, proxies=proxies)
    claim_status = start_claim.get("status_code", 400)
    if claim_status == 200:
        base.log(f"{base.green}Claim successfully")
        user_info = info(token=token, proxies=proxies)
        extract_garden_info(user_info=user_info)
    else:
        base.log(f"{base.green}Claim failed")
