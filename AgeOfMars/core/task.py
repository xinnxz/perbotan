import requests

from smart_airdrop_claimer import base
from core.headers import headers


def daily_bonus(token, proxies=None):
    url = "https://api-clicker.ageofmars.io/v1/daily-bonus"

    try:
        response = requests.get(
            url=url,
            headers=headers(token=token),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["data"]["received"]
        return status
    except:
        return None


def get_task(token, proxies=None):
    url = "https://api-clicker.ageofmars.io/v1/tasks"

    try:
        response = requests.get(
            url=url,
            headers=headers(token=token),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        task_list = data["data"]
        return task_list
    except:
        return None


def claim_daily_bonus(token, proxies=None):
    url = "https://api-clicker.ageofmars.io/v1/daily-bonus/get"

    try:
        response = requests.get(
            url=url,
            headers=headers(token=token),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        result = data["data"]["result"]
        return result
    except:
        return None


def check_task(token, task_id, proxies=None):
    url = f"https://api-clicker.ageofmars.io/v1/tasks/check?id={task_id}"

    try:
        response = requests.get(
            url=url,
            headers=headers(token=token),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["data"]["status"]
        return status
    except:
        return None


def reward_task(token, task_id, proxies=None):
    url = f"https://api-clicker.ageofmars.io/v1/tasks/reward?id={task_id}"

    try:
        response = requests.get(
            url=url,
            headers=headers(token=token),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        result = data["data"]["result"]
        return result
    except:
        return None


def process_claim_daily_bonus(token, proxies=None):
    bonus_status = daily_bonus(token=token, proxies=proxies)
    if bonus_status:
        base.log(f"{base.white}Auto Check-in: {base.red}Claimed")
    else:
        result = claim_daily_bonus(token=token, proxies=proxies)
        if result:
            base.log(f"{base.white}Auto Check-in: {base.green}Success")
        else:
            base.log(f"{base.white}Auto Check-in: {base.red}Fail")


def process_do_task(token, proxies=None):
    tasks = get_task(token=token, proxies=proxies)

    for section in tasks.keys():
        task_list = tasks[section]
        if task_list:
            for task in task_list:
                task_id = task["id"]
                task_name = task["title"]
                task_status = task["status"]
                if task_status == "processed":
                    base.log(f"{base.white}{task_name}: {base.green}Completed")
                elif task_status == "completed":
                    reward_task_result = reward_task(
                        token=token, task_id=task_id, proxies=proxies
                    )
                    if reward_task_result:
                        base.log(f"{base.white}{task_name}: {base.green}Completed")
                    else:
                        base.log(
                            f"{base.white}{task_name}: {base.red}Incomplete - Reward"
                        )
                elif task_status == "pending":
                    do_task_status = check_task(
                        token=token, task_id=task_id, proxies=proxies
                    )
                    if do_task_status == "completed":
                        reward_task_result = reward_task(
                            token=token, task_id=task_id, proxies=proxies
                        )
                        if reward_task_result:
                            base.log(f"{base.white}{task_name}: {base.green}Completed")
                        else:
                            base.log(
                                f"{base.white}{task_name}: {base.red}Incomplete - Reward"
                            )
                    elif do_task_status == "pending":
                        base.log(
                            f"{base.white}{task_name}: {base.red}Incomplete - Checking"
                        )

        else:
            base.log(f"{base.white}Auto Do Task: {base.red}Get task list error")
