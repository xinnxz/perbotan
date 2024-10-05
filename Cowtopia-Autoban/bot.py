import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
import json
import brotli

red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
black = Fore.LIGHTBLACK_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full paths to the files
data_file = os.path.join(script_dir, "data.txt")
config_file = os.path.join(script_dir, "config.json")


class Cowtopia:
    def __init__(self):
        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Smart Airdrop {white}Cowtopia Auto Claimer
        t.me/smartairdrop2120
        
        """

        self.auto_do_task = (
            json.load(open(config_file, "r")).get("auto-do-task", "false").lower()
            == "true"
        )

        self.auto_buy_factory = (
            json.load(open(config_file, "r")).get("auto-buy-factory", "false").lower()
            == "true"
        )

        self.auto_upgrade_factory = (
            json.load(open(config_file, "r"))
            .get("auto-upgrade-factory", "false")
            .lower()
            == "true"
        )

        self.auto_buy_animal = (
            json.load(open(config_file, "r")).get("auto-buy-animal", "false").lower()
            == "true"
        )

    # Clear the terminal
    def clear_terminal(self):
        # For Windows
        if os.name == "nt":
            _ = os.system("cls")
        # For macOS and Linux
        else:
            _ = os.system("clear")

    def headers(self, token):
        return {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {token}",
            "Origin": "https://cowtopia-prod.tonfarmer.com",
            "Referer": "https://cowtopia-prod.tonfarmer.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

    def get_token(self, data):
        url = f"https://cowtopia-be.tonfarmer.com/auth"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://cowtopia-prod.tonfarmer.com",
            "Referer": "https://cowtopia-prod.tonfarmer.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "X-Tg-Data": f"{data}",
        }

        response = requests.post(url=url, headers=headers)

        return response

    def game_info(self, token):
        url = f"https://cowtopia-be.tonfarmer.com/user/game-info?"

        headers = self.headers(token=token)

        response = requests.get(url=url, headers=headers)

        return response

    def offline_profit(self, token):
        url = f"https://cowtopia-be.tonfarmer.com/user/offline-profit?"

        headers = self.headers(token=token)

        response = requests.get(url=url, headers=headers)

        return response

    def claim_offline_profit(self, token):
        url = f"https://cowtopia-be.tonfarmer.com/user/claim-offline-profit"

        headers = self.headers(token=token)

        data = {"boost": "false"}

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def get_tasks(self, token):
        url = f"https://cowtopia-be.tonfarmer.com/mission"

        headers = self.headers(token=token)

        response = requests.get(url=url, headers=headers)

        return response

    def do_tasks(self, token, mission_key):
        url = f"https://cowtopia-be.tonfarmer.com/mission/check"

        headers = self.headers(token=token)

        data = {"mission_key": mission_key}

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def buy_animal(self, token, factory_id):
        url = f"https://cowtopia-be.tonfarmer.com/factory/buy-animal"

        headers = self.headers(token=token)

        data = {"factory_id": factory_id}

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def buy_factory(self, token):
        url = f"https://cowtopia-be.tonfarmer.com/factory/buy"

        headers = self.headers(token=token)

        data = {}

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def upgrade_factory(self, token):
        url = f"https://cowtopia-be.tonfarmer.com/factory/upgrade-house"

        headers = self.headers(token=token)

        data = {}

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def main(self):
        while True:
            self.clear_terminal()
            print(self.banner)
            data = open(data_file, "r").read().splitlines()
            num_acc = len(data)
            self.log(self.line)
            self.log(f"{green}Numer of account: {white}{num_acc}")
            for no, data in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")

                # Get token
                try:
                    get_token = self.get_token(data=data).json()
                    token = get_token["data"]["access_token"]
                    balance = get_token["data"]["user"]["money"]
                    self.log(f"{green}Balance: {white}{balance:,}")

                    # Offline profit
                    try:
                        self.log(f"{yellow}Checking offline profit...")
                        offline_profit = self.offline_profit(token=token).json()
                        profit = offline_profit["data"]["profit"]
                        if profit > 0:
                            self.log(f"{green}Ready to claim profit: {white}{profit:,}")
                            claim_offline_profit = self.claim_offline_profit(
                                token=token
                            ).json()
                            status = claim_offline_profit["success"]
                            balance = claim_offline_profit["data"]["user"]["money"]
                            if status:
                                self.log(f"{green}New balance: {white}{balance:,}")
                        else:
                            self.log(f"{yellow}No profit to claim")
                    except Exception as e:
                        self.log(f"{red}Check offline profit error!!!")

                    # Do tasks
                    if self.auto_do_task:
                        self.log(f"{yellow}Auto Do Task: {green}ON")
                        try:
                            self.log(f"{yellow}Checking task...")
                            get_tasks = self.get_tasks(token=token).json()
                            task_list = get_tasks["data"]["missions"]
                            for task in task_list:
                                task_name = task["name"]
                                task_key = task["key"]
                                task_status = task["completed"]
                                if not task_status:
                                    do_task = self.do_tasks(
                                        token=token, mission_key=task_key
                                    ).json()
                                    status = do_task["data"]["completed"]
                                    if status:
                                        self.log(
                                            f"{white}{task_name}: {green}Completed"
                                        )
                                    else:
                                        self.log(
                                            f"{white}{task_name}: {red}Uncompleted"
                                        )
                                else:
                                    self.log(f"{white}{task_name}: {green}Completed")
                        except Exception as e:
                            self.log(f"{red}Get tasks error!!!")
                    else:
                        self.log(f"{yellow}Auto Do Task: {red}OFF")

                    # Buy factory
                    if self.auto_buy_factory:
                        self.log(f"{yellow}Auto Buy Factory: {green}ON")
                        try:
                            buy_factory = self.buy_factory(token=token).json()
                            status = buy_factory["success"]
                            if status:
                                self.log(f"{white}Buy Factory: {green}Sucsess")
                            else:
                                self.log(f"{white}Buy Factory: {red}Not enough money")
                        except Exception as e:
                            self.log(f"{red}Buy factory error!!!")
                    else:
                        self.log(f"{yellow}Auto Buy Factory: {red}OFF")

                    # Upgrade factory
                    if self.auto_upgrade_factory:
                        self.log(f"{yellow}Auto Upgrade Factory: {green}ON")
                        try:
                            upgrade_factory = self.upgrade_factory(token=token).json()
                            status = upgrade_factory["success"]
                            if status:
                                self.log(f"{white}Uprade Factory: {green}Sucsess")
                            else:
                                self.log(
                                    f"{white}Uprade Factory: {red}Not enough money"
                                )
                        except Exception as e:
                            self.log(f"{red}Upgrade factory error!!!")
                    else:
                        self.log(f"{yellow}Auto Upgrade Factory: {red}OFF")

                    # Buy animal
                    if self.auto_buy_animal:
                        self.log(f"{yellow}Auto Buy Animal: {green}ON")
                        try:
                            while True:
                                game_info = self.game_info(token=token).json()
                                factories = game_info["data"]["factories"]
                                factories_with_id = [
                                    factory
                                    for factory in factories
                                    if "factory_id" in factory
                                ]
                                factory_with_least_animals = min(
                                    factories_with_id, key=lambda x: x["animal_count"]
                                )
                                factory_id = factory_with_least_animals["factory_id"]
                                animal_count = factory_with_least_animals[
                                    "animal_count"
                                ]
                                animal_cost = factory_with_least_animals["animal_cost"]
                                self.log(
                                    f"Factory with least animal: {factory_id} - Animal count: {animal_count} - Animal cost: {animal_cost}"
                                )
                                buy_animal = self.buy_animal(
                                    token=token, factory_id=factory_id
                                ).json()
                                status = buy_animal["success"]
                                if status:
                                    self.log(f"{white}Buy Animal: {green}Sucsess")
                                    time.sleep(2)
                                else:
                                    self.log(
                                        f"{white}Buy Animal: {red}Not enough money"
                                    )
                                    break
                        except Exception as e:
                            self.log(f"{red}Buy animal error!!!")
                    else:
                        self.log(f"{yellow}Auto Buy Animal: {red}OFF")
                except Exception as e:
                    self.log(f"{red}Get access token error!!!")

            print()
            wait_time = 30 * 60
            self.log(f"{yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        cowtopia = Cowtopia()
        cowtopia.main()
    except KeyboardInterrupt:
        sys.exit()
