import requests

from smart_airdrop_claimer import base
from core.headers import headers


def get_task(token, proxies=None):
    url = "https://backend.babydogepawsbot.com/channels"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        channels = data["channels"]
        return channels
    except:
        return None


def claim_task(token, channel_id, proxies=None):
    url = "https://backend.babydogepawsbot.com/channels-resolve"
    payload = {"channel_id": channel_id}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        return data
    except:
        return None


def process_do_task(token, proxies=None):
    channels = get_task(token=token, proxies=proxies)
    if channels:
        for channel in channels:
            channel_id = channel["id"]
            channel_title = channel["title"]
            is_resolved = channel["is_resolved"]
            if not is_resolved:
                claim = claim_task(token=token, channel_id=channel_id, proxies=proxies)
                if claim:
                    claim_status = claim["is_reward"]
                    if claim_status:
                        base.log(f"{base.white}{channel_title}: {base.green}Completed")
                    else:
                        base.log(
                            f"{base.white}{channel_title}: {base.red}Incomplete (please do by yourself or wait for task updated)"
                        )
                else:
                    base.log(f"{base.white}{channel_title}: {base.red}Claim error")
            else:
                base.log(f"{base.white}{channel_title}: {base.green}Completed")
    else:
        base.log(f"{base.white}Auto Do Task: {base.red}Get task info error")
