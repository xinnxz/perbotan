import requests

from package.core.headers import headers
from package import base


def get_claimable_ref(token, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users/get-claimable-ref"

    try:
        response = requests.get(
            url=url, headers=headers(token), proxies=proxies, timeout=20
        )
        data = response.json()
        bonus = data["pendingBonus"]
        return bonus
    except:
        return None


def claim_ref(token, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users/claim-refs-mining"

    try:
        response = requests.get(
            url=url, headers=headers(token), proxies=proxies, timeout=20
        )
        data = response.json()
        status = data["success"]
        return status
    except:
        return None


def process_claim_ref(token, proxies=None):
    bonus = get_claimable_ref(token=token, proxies=proxies)
    if bonus is not None:
        if bonus > 0:
            claim_status = claim_ref(token=token, proxies=proxies)
            if claim_status:
                base.log(
                    f"{base.white}Auto Claim Ref: {base.green}Success | Added {bonus} points"
                )
            else:
                base.log(f"{base.white}Auto Claim Ref: {base.red}Not time to claim")
        else:
            base.log(f"{base.white}Auto Claim Ref: {base.red}No point to claim")
    else:
        base.log(f"{base.white}Auto Claim Ref: {base.red}Get claimable bonus error")
