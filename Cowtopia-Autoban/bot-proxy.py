import os
import sys
import time
import requests
from requests.auth import HTTPProxyAuth
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
data_file = os.path.join(script_dir, "data-proxy.json")
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

    def proxies(self, proxy_info):
        return {"http": f"{proxy_info}", "https": f"{proxy_info}"}

    def check_ip(self, proxy_info):
        url = "https://api.ipify.org?format=json"

        proxies = self.proxies(proxy_info=proxy_info)

        # Parse the proxy credentials if present
        if "@" in proxy_info:
            proxy_credentials = proxy_info.split("@")[0]
            proxy_user = proxy_credentials.split(":")[1]
            proxy_pass = proxy_credentials.split(":")[2]
            auth = HTTPProxyAuth(proxy_user, proxy_pass)
        else:
            auth = None

        try:
            response = requests.get(url=url, proxies=proxies, auth=auth)
            response.raise_for_status()  # Raises an error for bad status codes
            return response.json().get("ip")
        except requests.exceptions.RequestException as e:
            print(f"IP check failed: {e}")
            return None

    def get_token(self, data, proxy_info):
        url = f"https://cowtopia-be.tonfarmer.com/auth"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://cowtopia-prod.tonfarmer.com",
            "Referer": "https://cowtopia-prod.tonfarmer.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "X-Tg-Data": f"{data}",
        }

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url=url, headers=headers, proxies=proxies)

        return response

    def game_info(self, token, proxy_info):
        url = f"https://cowtopia-be.tonfarmer.com/user/game-info?"

        headers = self.headers(token=token)

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.get(url=url, headers=headers, proxies=proxies)

        return response

    def offline_profit(self, token, proxy_info):
        url = f"https://cowtopia-be.tonfarmer.com/user/offline-profit?"

        headers = self.headers(token=token)

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.get(url=url, headers=headers, proxies=proxies)

        return response

    def claim_offline_profit(self, token, proxy_info):
        url = f"https://cowtopia-be.tonfarmer.com/user/claim-offline-profit"

        headers = self.headers(token=token)

        data = {"boost": "false"}

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url=url, headers=headers, data=data, proxies=proxies)

        return response

    def get_tasks(self, token, proxy_info):
        url = f"https://cowtopia-be.tonfarmer.com/mission"

        headers = self.headers(token=token)

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.get(url=url, headers=headers, proxies=proxies)

        return response

    def do_tasks(self, token, mission_key, proxy_info):
        url = f"https://cowtopia-be.tonfarmer.com/mission/check"

        headers = self.headers(token=token)

        data = {"mission_key": mission_key}

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url=url, headers=headers, data=data, proxies=proxies)

        return response

    def buy_animal(self, token, factory_id, proxy_info):
        url = f"https://cowtopia-be.tonfarmer.com/factory/buy-animal"

        headers = self.headers(token=token)

        data = {"factory_id": factory_id}

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url=url, headers=headers, data=data, proxies=proxies)

        return response

    def buy_factory(self, token, proxy_info):
        url = f"https://cowtopia-be.tonfarmer.com/factory/buy"

        headers = self.headers(token=token)

        data = {}

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url=url, headers=headers, data=data, proxies=proxies)

        return response

    def upgrade_factory(self, token, proxy_info):
        url = f"https://cowtopia-be.tonfarmer.com/factory/upgrade-house"

        headers = self.headers(token=token)

        data = {}

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url=url, headers=headers, data=data, proxies=proxies)

        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def parse_proxy_info(self, proxy_info):
        try:
            stripped_url = proxy_info.split("://", 1)[-1]
            credentials, endpoint = stripped_url.split("@", 1)
            user_name, password = credentials.split(":", 1)
            ip, port = endpoint.split(":", 1)
            return {"user_name": user_name, "pass": password, "ip": ip, "port": port}
        except:
            return None

    def main(self):
        while True:
            self.clear_terminal()
            print(self.banner)
            accounts = json.load(open(data_file, "r"))["accounts"]
            num_acc = len(accounts)
            self.log(self.line)
            self.log(f"{green}Numer of account: {white}{num_acc}")
            for no, account in enumerate(accounts):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")
                data = account["acc_info"]
                proxy_info = account["proxy_info"]
                parsed_proxy_info = self.parse_proxy_info(proxy_info)
                if parsed_proxy_info is None:
                    self.log(
                        f"{red}Check proxy format: {white}http://user:pass@ip:port"
                    )
                    break
                ip_adress = parsed_proxy_info["ip"]
                self.log(f"{green}Input IP Address: {white}{ip_adress}")

                ip = self.check_ip(proxy_info=proxy_info)
                self.log(f"{green}Actual IP Address: {white}{ip}")

                # Get token
                try:
                    get_token = self.get_token(data=data, proxy_info=proxy_info).json()
                    token = get_token["data"]["access_token"]
                    balance = get_token["data"]["user"]["money"]
                    self.log(f"{green}Balance: {white}{balance:,}")

                    # Offline profit
                    try:
                        self.log(f"{yellow}Checking offline profit...")
                        offline_profit = self.offline_profit(
                            token=token, proxy_info=proxy_info
                        ).json()
                        profit = offline_profit["data"]["profit"]
                        if profit > 0:
                            self.log(f"{green}Ready to claim profit: {white}{profit:,}")
                            claim_offline_profit = self.claim_offline_profit(
                                token=token, proxy_info=proxy_info
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
                            get_tasks = self.get_tasks(
                                token=token, proxy_info=proxy_info
                            ).json()
                            task_list = get_tasks["data"]["missions"]
                            for task in task_list:
                                task_name = task["name"]
                                task_key = task["key"]
                                task_status = task["completed"]
                                if not task_status:
                                    do_task = self.do_tasks(
                                        token=token,
                                        mission_key=task_key,
                                        proxy_info=proxy_info,
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
                            buy_factory = self.buy_factory(
                                token=token, proxy_info=proxy_info
                            ).json()
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
                            upgrade_factory = self.upgrade_factory(
                                token=token, proxy_info=proxy_info
                            ).json()
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
                                game_info = self.game_info(
                                    token=token, proxy_info=proxy_info
                                ).json()
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
                                    token=token,
                                    factory_id=factory_id,
                                    proxy_info=proxy_info,
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
