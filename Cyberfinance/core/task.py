import requests

from smart_airdrop_claimer import base
from core.headers import headers


def get_task(token, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/gametask/all"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        task_list = data["message"]
        return task_list
    except:
        return None


def get_ads(token, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/ads/count"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        ads_count = data["message"]["amountLeftToView"]
        return ads_count
    except:
        return None


def do_task(token, task_id, proxies=None):
    url = f"https://api.cyberfin.xyz/api/v1/gametask/complete/{task_id}"

    try:
        response = requests.patch(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def watch_ads(token, proxies=None):
    url = f"https://api.cyberfin.xyz/api/v1/ads/log"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def process_do_task(token, proxies=None):
    task_list = get_task(token=token, proxies=proxies)

    if task_list:
        for task in task_list:
            task_id = task["uuid"]
            task_name = task["title"]
            is_completed = task["isCompleted"]
            is_active = task["isActive"]
            if is_completed:
                base.log(f"{base.white}{task_name}: {base.green}Completed")
            else:
                if is_active:
                    start_do_task = do_task(
                        token=token, task_id=task_id, proxies=proxies
                    )
                    try:
                        status = start_do_task["code"]
                        if status == 200:
                            base.log(f"{base.white}{task_name}: {base.green}Completed")
                        else:
                            base.log(f"{base.white}{task_name}: {base.red}Incomplete")
                    except:
                        base.log(f"{base.white}{task_name}: {base.red}Incomplete")
                else:
                    base.log(f"{base.white}{task_name}: {base.red}Inactive")
    else:
        base.log(f"{base.white}Auto Do Task: {base.red}Get task list error")


def process_watch_ads(token, proxies=None):
    while True:
        ads_count = get_ads(token=token, proxies=proxies)
        if ads_count > 0:
            start_watch_ads = watch_ads(token=token, proxies=proxies)
            try:
                value = start_watch_ads["message"]["value"]
                base.log(
                    f"{base.white}Auto Watch Ads: {base.green}Sucess | Added {value:,} points"
                )
            except:
                base.log(f"{base.white}Auto Watch Ads: {base.red}Watch ads error")
                break
        else:
            base.log(f"{base.white}Auto Watch Ads: {base.red}No ads to watch")
            break
