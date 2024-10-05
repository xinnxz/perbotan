import requests

from smart_airdrop_claimer import base
from core.headers import headers


def check_in(data, proxies=None):
    url = "https://api.tabibot.com/api/user/v1/check-in"

    try:
        response = requests.post(
            url=url, headers=headers(data=data), proxies=proxies, timeout=20
        )
        data = response.json()
        status = data["data"]["check_in_status"]
        return status
    except:
        return None


def process_check_in(data, proxies=None):
    check_in_status = check_in(data=data, proxies=proxies)
    if check_in_status == 1:
        base.log(f"{base.white}Auto Check-in: {base.green}Success")
    elif check_in_status == 2:
        base.log(f"{base.white}Auto Check-in: {base.red}Checked in already")
    else:
        base.log(f"{base.white}Auto Check-in: {base.red}Fail")


def get_mine_project(data, proxies=None):
    url = "https://api.tabibot.com/api/task/v1/project/mine"

    try:
        response = requests.get(
            url=url, headers=headers(data=data), proxies=proxies, timeout=20
        )
        data = response.json()
        project_list = data["data"]
        return project_list
    except:
        return None


def get_project_task(data, project_tag, proxies=None):
    url = f"https://api.tabibot.com/api/task/v1/mine?project_tag={project_tag}"

    try:
        response = requests.get(
            url=url, headers=headers(data=data), proxies=proxies, timeout=20
        )
        data = response.json()
        task_list = data["data"]["list"]
        return task_list
    except:
        return None


def do_task(data, task_tag, proxies=None):
    url = f"https://api.tabibot.com/api/task/v1/verify/task"
    payload = {"task_tag": task_tag}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["data"]["verify"]
        return status
    except:
        return None


def do_project(data, project_tag, proxies=None):
    url = f"https://api.tabibot.com/api/task/v1/verify/project"
    payload = {"project_tag": project_tag}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["data"]["verify"]
        return status
    except:
        return None


def process_do_project_task(data, proxies=None):
    project_list = get_mine_project(data=data, proxies=proxies)
    if project_list:
        for project in project_list:
            project_tag = project["project_tag"]
            project_name = project["project_name"]
            project_status = project["user_project_status"]
            if project_status == 1:
                base.log(
                    f"{base.white}Project: {base.yellow}{project_name} - {base.white}Status: {base.green}Completed"
                )
            else:
                task_list = get_project_task(
                    data=data, project_tag=project_tag, proxies=proxies
                )
                for task in task_list:
                    task_tag = task["task_tag"]
                    task_name = task["task_name"]
                    task_status = task["user_task_status"]
                    if task_status == 1:
                        base.log(
                            f"{base.white}Project: {base.yellow}{project_name} - {base.white}Task: {base.yellow}{task_name} - {base.white}Status: {base.green}Completed"
                        )
                    else:
                        do_task_status = do_task(
                            data=data, task_tag=task_tag, proxies=proxies
                        )
                        if do_task_status:
                            base.log(
                                f"{base.white}Project: {base.yellow}{project_name} - {base.white}Task: {base.yellow}{task_name} - {base.white}Status: {base.green}Completed"
                            )
                        else:
                            base.log(
                                f"{base.white}Project: {base.yellow}{project_name} - {base.white}Task: {base.yellow}{task_name} - {base.white}Status: {base.red}Incomplete"
                            )

                do_project_status = do_project(
                    data=data, project_tag=project_tag, proxies=proxies
                )
                if do_project_status:
                    base.log(
                        f"{base.white}Project: {base.yellow}{project_name} - {base.white}Status: {base.green}Completed"
                    )
                else:
                    base.log(
                        f"{base.white}Project: {base.yellow}{project_name} - {base.white}Status: {base.red}Incomplete"
                    )
    else:
        base.log(f"{base.white}Auto Task: {base.red}Get project list error")


def get_normal_task(data, proxies=None):
    url = "https://api.tabibot.com/api/task/v1/list"

    try:
        response = requests.get(
            url=url, headers=headers(data=data), proxies=proxies, timeout=20
        )
        data = response.json()
        project_list = data["data"]
        return project_list
    except:
        return None


def process_do_normal_task(data, proxies=None):
    project_list = get_normal_task(data=data, proxies=proxies)
    if project_list:
        for project in project_list:
            task_list = project["task_list"]
            for task in task_list:
                task_tag = task["task_tag"]
                task_name = task["task_name"]
                task_status = task["user_task_status"]
                if task_status == 1:
                    base.log(
                        f"{base.white}Task: {base.yellow}{task_name} - {base.white}Status: {base.green}Completed"
                    )
                else:
                    do_task_status = do_task(
                        data=data, task_tag=task_tag, proxies=proxies
                    )
                    if do_task_status:
                        base.log(
                            f"{base.white}Task: {base.yellow}{task_name} - {base.white}Status: {base.green}Completed"
                        )
                    else:
                        base.log(
                            f"{base.white}Task: {base.yellow}{task_name} - {base.white}Status: {base.red}Incomplete"
                        )
    else:
        base.log(f"{base.white}Auto Task: {base.red}Get project list error")
