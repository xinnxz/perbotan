import requests

from smart_airdrop_claimer import base
from core.headers import headers


def check_in(token, proxies=None):
    url = "https://api.mmbump.pro/v1/grant-day/claim"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), json={}, proxies=proxies, timeout=20
        )
        data = response.json()
        streak = data["day_grant_day"]
        return streak
    except:
        return None


def process_check_in(token, proxies=None):
    streak = check_in(token=token, proxies=proxies)
    if streak:
        base.log(f"{base.white}Auto Check-in: {base.green}Success | Streak: {streak}")
    else:
        base.log(f"{base.white}Auto Check-in: {base.red}Checked in already")


def get_task(token, proxies=None):
    url = "https://api.mmbump.pro/v1/task-list"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), json={}, proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def do_task(token, task_id, proxies=None):
    url = "https://api.mmbump.pro/v1/task-list/complete"
    payload = {"id": task_id}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["task"]["status"]
        return status
    except:
        return None


def process_do_task(token, proxies=None):
    task_list = get_task(token=token, proxies=proxies)
    for task in task_list:
        task_id = task["id"]
        task_name = task["name"]
        task_status = task["status"]
        if task_status == "granted":
            base.log(f"{base.white}{task_name}: {base.green}Completed")
        elif task_status == "possible":
            do_task_status = do_task(token=token, task_id=task_id, proxies=proxies)
            if do_task_status == "granted":
                base.log(f"{base.white}{task_name}: {base.green}Completed")
            elif do_task_status == "possible":
                base.log(f"{base.white}{task_name}: {base.red}Incomplete")
            else:
                base.log(f"{base.white}{task_name}: {base.red}Inactive")
        else:
            base.log(f"{base.white}{task_name}: {base.red}Unknown status")
