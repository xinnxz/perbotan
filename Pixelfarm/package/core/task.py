import requests
from package.core.headers import headers
from package import base
import json


def get_task(tele_id, proxies=None):
    url = f"https://api.pixelfarm.app/user/{tele_id}/quests"

    try:
        response = requests.get(url=url, headers=headers(), proxies=proxies, timeout=20)
        data = response.json()
        return data
    except:
        return None


def do_task(token, task_id, proxies=None):
    url = f"https://api.pixelfarm.app/user/user-quest"
    new_headers = headers(token=token)
    payload = {"quest_id": f"{task_id}"}
    data = json.dumps(payload)
    new_headers["Content-Length"] = str(len(data))
    new_headers["Content-Type"] = "application/json"

    try:
        response = requests.put(
            url=url,
            headers=new_headers,
            data=data,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        return data
    except:
        return None


def process_task(tele_id, token, proxies=None):
    task_list = get_task(tele_id=tele_id, proxies=proxies)["data"]
    for task in task_list:
        task_name = task["name"]
        task_id = task["quest_id"]
        is_done = task["done_at"]
        if is_done is None:
            complete_task = do_task(token=token, task_id=task_id, proxies=proxies)
            complete_task_status = complete_task.get("status_code", 400)
            if complete_task_status == 200:
                base.log(f"{base.white}{task_name}: {base.green}Completed")
            else:
                base.log(f"{base.white}{task_name}: {base.red}Incomplete")
        else:
            base.log(f"{base.white}{task_name}: {base.green}Completed")
