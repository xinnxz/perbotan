import requests

from package.core.headers import headers
from package import base


def process_claim_daily_task(token, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users/claim-daily-task"
    payload = {}

    try:
        response = requests.post(
            url=url, headers=headers(token), json=payload, proxies=proxies, timeout=20
        )
        data = response.json()
        balance = data["balance"]
        base.log(
            f"{base.white}Auto Claim Daily Reward: {base.green}Success {base.white}| {base.green}New balance: {base.white}{balance}"
        )
    except:
        base.log(f"{base.white}Auto Claim Daily Reward: {base.red}Claimed already")


def social_tasks(token, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users/social-tasks"

    try:
        response = requests.get(
            url=url, headers=headers(token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def claim_social_task(token, task_id, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users/claim-social-task"
    payload = {"taskId": task_id}

    try:
        response = requests.post(
            url=url, headers=headers(token), json=payload, proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def process_claim_social_tasks(token, proxies=None):
    task_list = social_tasks(token=token, proxies=proxies)
    for task in task_list:
        task_id = task["id"]
        task_name = task["text"]
        task_status = task["isCompleted"]
        if task_status:
            base.log(f"{base.white}{task_name}: {base.green}Completed")
        else:
            do_task = claim_social_task(token=token, task_id=task_id)
            try:
                do_task_status = do_task["isClaimed"]
                if do_task_status:
                    base.log(f"{base.white}{task_name}: {base.green}Completed")
            except:
                base.log(f"{base.white}{task_name}: {base.red}Incomplete")
