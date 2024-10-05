import requests

from smart_airdrop_claimer import base
from core.headers import headers


def get_task(data, proxies=None):
    url = "https://api.agent301.org/getTasks"
    payload = {}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        task_list = data["result"]["data"]

        return task_list
    except:
        return None


def do_task(data, task_type, proxies=None):
    url = "https://api.agent301.org/completeTask"
    payload = {"type": task_type}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["result"]["is_completed"]

        return status
    except:
        return None


def process_do_task(data, proxies=None):
    task_list = get_task(data=data, proxies=proxies)
    if task_list:
        for task in task_list:
            task_type = task["type"]
            task_name = task["title"]
            task_status = task["is_claimed"]
            if task_status:
                base.log(f"{base.white}{task_name}: {base.green}Completed")
            else:
                if task_type == "video":
                    count = task["count"]
                    max_count = task["max_count"]
                    for i in range(max_count - count):
                        do_task_status = do_task(
                            data=data, task_type=task_type, proxies=proxies
                        )
                        if do_task_status:
                            base.log(f"{base.white}{task_name}: {base.green}Success")
                        else:
                            base.log(f"{base.white}{task_name}: {base.red}Incomplete")
                else:
                    do_task_status = do_task(
                        data=data, task_type=task_type, proxies=proxies
                    )
                    if do_task_status:
                        base.log(f"{base.white}{task_name}: {base.green}Success")
                    else:
                        base.log(f"{base.white}{task_name}: {base.red}Incomplete")
    else:
        base.log(f"{base.white}Auto Do Task: {base.red}Task list not found!")


def get_wheel_task(data, proxies=None):
    url = "https://api.agent301.org/wheel/load"
    payload = {}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        task_list = data["result"]["tasks"]

        return task_list
    except:
        return None


def do_wheel_task(data, type, proxies=None):
    url = "https://api.agent301.org/wheel/task"
    payload = {"type": type}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["ok"]

        return status
    except:
        return None


def process_do_wheel_task(data, proxies=None):
    wheel_task = get_wheel_task(data=data, proxies=proxies)
    if wheel_task:
        for type in wheel_task.keys():
            while True:
                do_wheel_task_status = do_wheel_task(
                    data=data, type=type, proxies=proxies
                )
                if do_wheel_task_status:
                    base.log(
                        f"{base.white}Auto Do Wheel Task: {base.yellow}Check status | {base.white}Type: {base.yellow}{type} - {base.white}Status: {base.green}Success"
                    )
                else:
                    base.log(
                        f"{base.white}Auto Do Wheel Task: {base.yellow}Check status | {base.white}Type: {base.yellow}{type} - {base.white}Status: {base.red}Not available"
                    )
                    break
    else:
        base.log(f"{base.white}Auto Do Wheel Task: {base.red}Task list not found!")
