import os
import json
import time
import random
import requests

from ctypes import windll
from datetime import datetime
from text import print_name, clear_console
from colorama import Fore, Style
from typing import Union

windll.kernel32.SetConsoleTitleW("Diamore Hack by Argona")

# {"Account Name":["query","user-agent"]}
def get_data_from_file() -> Union[dict, bool]:
    user_folder = os.path.expanduser("~")
    tokens_file_path = os.path.join(user_folder, "diamore.json")

    if os.path.exists(tokens_file_path):
        with open(tokens_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not data["accounts"]:
                print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "Accounts need to be added!")
                time.sleep(2)
                return False
            accounts_dict = {}
            accounts_names = list(data["accounts"].keys())
            for i in accounts_names:
                account = data["accounts"][i]
                accounts_dict[i] = [account["query"], account["user-agent"]]

            return accounts_dict

    else:
        data = {
            "accounts": {}
        }
        with open(tokens_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print(
                Fore.LIGHTMAGENTA_EX + Style.BRIGHT + f"File not found. A new file has been created at the path: {tokens_file_path}")
            print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "Accounts need to be added!")
            time.sleep(2)
            return False


def get_user(headers: dict, max_attempts: int) -> dict:
    print(Fore.YELLOW + Style.BRIGHT + "Attempting to get user......")
    url = "https://api.diamore.co/user"
    for _ in range(max_attempts):
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            data = response.json()
            time.sleep(2)
            return data
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(2)

    print(Fore.LIGHTRED_EX + "Failed to get user!")
    return {}


def get_upgrades(headers: dict, max_attempts: int) -> dict:
    print(Fore.YELLOW + Style.BRIGHT + "Attempting to get upgrades......")
    url = "https://api.diamore.co/upgrades"
    for _ in range(max_attempts):
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            data = response.json()
            time.sleep(2)
            return data
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(2)

    print(Fore.LIGHTRED_EX + "Failed to get upgrades!")
    return {}


def buy(type_upgrade: str, headers: dict, max_attempts: int) -> bool:
    print(Fore.YELLOW + Style.BRIGHT + "Attempting to buy upgrade......")
    url = "https://api.diamore.co/upgrades/buy"
    body = {"type": type_upgrade}
    for _ in range(max_attempts):
        response = requests.post(url=url, headers=headers, json=body)
        if response.status_code == 201:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            time.sleep(2)
            return True
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(2)

    print(Fore.LIGHTRED_EX + "Failed to buy upgrade!")
    return False


# автоматически улучшает скиллы перед играми если есть поинты, улучшает до 12 лвл силу тапа и длительность игры
# (дальше не выгодно)
def improvements(headers: dict):
    print(Fore.YELLOW + Style.BRIGHT + "Attempting to upgrade tap and duration......")
    while True:
        user = get_user(headers, 3)
        if user:
            upgrades = get_upgrades(headers, 3)
            if upgrades:
                balance = float(user["balance"])
                tapPower_price = float(upgrades["tapPower"][1]["price"])
                tapDuration_price = float(upgrades["tapDuration"][1]["price"])
                tapPower_level = float(upgrades["tapPower"][0]["level"])
                tapDuration_level = float(upgrades["tapDuration"][0]["level"])
                if tapPower_level >= 12 and tapDuration_level >= 12:
                    print(Fore.LIGHTMAGENTA_EX + "Skills are pumped up to 12 levels or more")
                    time.sleep(2)
                    return
                if balance >= tapPower_price + tapDuration_price:
                    buy("tapPower", headers, 3)
                    buy("tapDuration", headers, 3)
                    print(Fore.LIGHTGREEN_EX + "Successful!")
                    time.sleep(1.5)
                else:
                    print(Fore.LIGHTMAGENTA_EX + "Not enough points!")
                    time.sleep(2)
                    return
            else:
                print(Fore.LIGHTRED_EX + "Failed to get upgrades")
                time.sleep(2)
                return
        else:
            print(Fore.LIGHTRED_EX + "Failed to get user")
            time.sleep(2)
            return


# {"total":5, "available":0}
def get_ads(headers: dict, max_attempts: int) -> dict:
    print(Fore.YELLOW + Style.BRIGHT + "Attempting to get ads count......")
    url = "https://api.diamore.co/ads"
    for _ in range(max_attempts):
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            ads = response.json()
            time.sleep(2)
            return ads
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(2)

    print(Fore.LIGHTRED_EX + "Failed to get ads count!")
    return {}


def pass_ads(headers: dict, max_attempts: int) -> bool:
    print(Fore.YELLOW + Style.BRIGHT + "Attempting to watch ads......")
    url = "https://api.diamore.co/ads/watch"
    body = {"type": "adsgram"}
    time.sleep(10)
    for _ in range(max_attempts):
        response = requests.post(url=url, headers=headers, json=body)
        if response.status_code == 201:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            time.sleep(2)
            return True
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(2)

    print(Fore.LIGHTRED_EX + "Failed to watch ads!")
    return False


def visit(headers: dict, max_attempts: int) -> bool:
    print(Fore.YELLOW + Style.BRIGHT + "Attempting to post visit......")
    url = "https://api.diamore.co/user/visit"
    for _ in range(max_attempts):
        response = requests.post(url=url, headers=headers)
        if response.status_code == 201:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            time.sleep(2)
            return True
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(2)

    print(Fore.LIGHTRED_EX + "Failed to post visit!")
    return False


def post_taps(upgrades: dict, headers: dict, max_attempts: int) -> bool:
    if upgrades:
        taps = 28
        taps_power = float(upgrades["tapPower"][1]["value"])
        taps_duration = upgrades["tapDuration"][1]["durationMil"] // 1000
        points = int(taps * taps_power * taps_duration + random.randint(-100, 50))

        print(Fore.YELLOW + Style.BRIGHT + "Attempting to post taps......")
        time.sleep(taps_duration)

        url = "https://api.diamore.co/taps/claim"
        body = {"amount": str(points)}
        for _ in range(max_attempts):
            response = requests.post(url=url, headers=headers, json=body)
            if response.status_code == 201:
                print(Fore.LIGHTGREEN_EX + f"Successful! : {points} points")
                time.sleep(2)
                return True
            else:
                print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
                print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
                print(response.json())
                time.sleep(2)

    print(Fore.LIGHTRED_EX + "Failed to post taps!")
    return False


def get_daily_reward(headers: dict, max_attempts: int) -> bool:
    print(Fore.YELLOW + Style.BRIGHT + "Attempting to get a daily reward......")
    url = "https://api.diamore.co/daily/claim"
    for _ in range(max_attempts):
        response = requests.post(url=url, headers=headers)
        if response.status_code == 201:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            time.sleep(2)
            return True
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(2)

    print(Fore.LIGHTRED_EX + "Failed to get a daily reward!")
    return False


def main():
    try:
        print_name()
        clear_console()
        accounts_dict = get_data_from_file() # {"Account Name":["query","user-agent"]}
        if not accounts_dict:
            return
        accounts_names = list(accounts_dict.keys())

        print(Style.BRIGHT + Fore.LIGHTWHITE_EX + f"Available accounts: {' '.join(accounts_names)}")
        time.sleep(0.5)
        StrExcludedAccounts = input(Fore.LIGHTCYAN_EX + "Which accounts to exclude from the automation list?: ")
        ExcludeAccounts = StrExcludedAccounts.split()
        for i in range(len(accounts_names)):
            try:
                name = accounts_names[i]
                if name in ExcludeAccounts:
                    continue

                headers = {
                    "Authorization": f"Token {accounts_dict[name][0]}",
                    "user-agent": accounts_dict[name][1],
                    "accept": "application/json, text/plain, */*",
                    "origin": "https://app.diamore.co",
                    "referer": "https://app.diamore.co/",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
                }

                print(Fore.BLUE + Style.BRIGHT + f"The account begins: {name}\n")

                visit(headers, 3)
                get_daily_reward(headers, 2)

                improvements(headers)

                upgrade = get_upgrades(headers, 3)
                limit_date = get_user(headers, 3)["limitDate"]
                #проверка на доступность игры
                if (not limit_date) or (datetime.strptime(limit_date, "%Y-%m-%dT%H:%M:%S.%fZ") < datetime.utcnow()):
                    post_taps(upgrade, headers, 3)

                ads = get_ads(headers, 3)
                for _ in range(ads["available"]):
                    if pass_ads(headers, 3):
                        post_taps(upgrade, headers, 3)

                time.sleep(3.5)
                clear_console()
            except Exception as e:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + f"Error: {e}")
                time.sleep(2)
                clear_console()
                continue
    except Exception as e:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + f"Error: {e}")
        time.sleep(5)
        return


if __name__ == '__main__':
    main()
    print(Style.BRIGHT + Fore.LIGHTWHITE_EX + "\nThe automation has been completed successfully!")
    time.sleep(3)
