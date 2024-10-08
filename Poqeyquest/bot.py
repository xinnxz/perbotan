import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
import json
import brotli
import urllib.parse

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


class PokeyQuest:
    def __init__(self):
        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Smart Airdrop {white}PokeyQuest Auto Claimer
        t.me/smartairdrop2120
        
        """

        self.auto_do_task = (
            json.load(open(config_file, "r")).get("auto-do-task", "false").lower()
            == "true"
        )

        self.auto_upgrade = (
            json.load(open(config_file, "r")).get("auto-upgrade", "false").lower()
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
            "Origin": "https://dapp.pokequest.io",
            "Referer": "https://dapp.pokequest.io/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
        }

    def get_token(self, data):
        url = f"https://api.pokey.quest/auth/login"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://dapp.pokequest.io",
            "Referer": "https://dapp.pokequest.io/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
        }

        data = self.parse_query_id(data=data)

        data = json.dumps(data)

        headers["Content-Length"] = str(len(data))

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def user_info(self, token):
        url = f"https://api.pokey.quest/tap/sync"

        headers = self.headers(token=token)

        response = requests.post(url=url, headers=headers)

        return response

    def get_task(self, token):
        url = f"https://api.pokey.quest/mission/list"

        headers = self.headers(token=token)

        response = requests.get(url=url, headers=headers)

        return response

    def do_task(self, token, mission_id):
        url = f"https://api.pokey.quest/mission/claim"

        headers = self.headers(token=token)

        data = {"mission_id": mission_id}

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def get_friend(self, token):
        url = f"https://api.pokey.quest/referral/list"

        headers = self.headers(token=token)

        response = requests.get(url=url, headers=headers)

        return response

    def claim_friend(self, token, friend_id):
        url = f"https://api.pokey.quest/referral/claim-friend"

        headers = self.headers(token=token)

        data = {"friend_id": friend_id}

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def farm(self, token):
        url = f"https://api.pokey.quest/pokedex/farm"

        headers = self.headers(token=token)

        response = requests.post(url=url, headers=headers)

        return response

    def upgrade(self, token):
        url = f"https://api.pokey.quest/poke/upgrade"

        headers = self.headers(token=token)

        response = requests.post(url=url, headers=headers)

        return response

    def tap(self, token, tap_count):
        url = f"https://api.pokey.quest/tap/tap"

        headers = self.headers(token=token)

        data = {"count": tap_count}

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def parse_query_id(self, data):
        parsed_query = urllib.parse.parse_qs(data)

        final_json = {}

        for key, values in parsed_query.items():
            if key == "user" and values:
                user_json_str = values[0]
                final_json[key] = json.loads(urllib.parse.unquote(user_json_str))
            else:
                final_json[key] = values[0] if values else None

        return final_json

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

                try:
                    # Get token
                    get_token = self.get_token(data=data).json()
                    token = get_token["data"]["token"]

                    # Get user info
                    user_info = self.user_info(token=token).json()
                    level = user_info["data"]["level"]
                    available_taps = user_info["data"]["available_taps"]
                    self.log(
                        f"{green}Level: {white}{level} - {green}Available taps: {white}{available_taps}"
                    )
                    balances = user_info["data"]["balance_coins"]
                    for balance in balances:
                        coin_type = balance["currency_symbol"]
                        coin_balance = balance["balance"]
                        self.log(f"{green}{coin_type} balance: {white}{coin_balance:,}")

                    # Do task
                    if self.auto_do_task:
                        self.log(f"{yellow}Auto Do Task: {green}ON")
                        self.log(f"{yellow}Trying to do tasks...")
                        get_task = self.get_task(token=token).json()
                        tasks = get_task["data"]
                        for task in tasks:
                            task_id = task["id"]
                            task_name = task["title"]
                            do_task = self.do_task(
                                token=token, mission_id=task_id
                            ).json()
                            status = do_task["data"]["success"]
                            if status:
                                self.log(f"{white}{task_name}: {green}Success")
                            else:
                                self.log(
                                    f"{white}{task_name}: {red}Cannot process or Completed"
                                )
                    else:
                        self.log(f"{yellow}Auto Do Task: {red}OFF")

                    # Claim friend
                    self.log(f"{yellow}Trying to claim from friend...")
                    get_friend = self.get_friend(token=token).json()
                    friends = get_friend["data"]["data"]
                    for friend in friends:
                        friend_id = friend["id"]
                        claim_friend = self.claim_friend(
                            token=token, friend_id=friend_id
                        ).json()
                        status = claim_friend["data"]["success"]
                        if status:
                            self.log(f"{white}Friend {friend_id}: {green}Success")
                        else:
                            self.log(f"{white}Friend {friend_id}: {red}Claimed")

                    # Reward from collection
                    self.log(f"{yellow}Trying to get reward from collection...")
                    farm = self.farm(token=token).json()
                    try:
                        gold_reward = farm["data"]["gold_reward"]
                        self.log(f"{green}Gold reward: {white}{gold_reward}")
                    except:
                        self.log(
                            f"{white}Get reward from collection: {red}Not time to claim"
                        )

                    # Upgrade
                    if self.auto_upgrade:
                        self.log(f"{yellow}Auto Upgrade: {green}ON")
                        upgrade = self.upgrade(token=token).json()
                        status = upgrade["error_code"]
                        if status == "OK":
                            level = upgrade["data"]["level"]
                            max_taps = upgrade["data"]["max_taps"]
                            self.log(
                                f"{green}New level: {white}{level} - {green}Max taps: {white}{max_taps}"
                            )
                        elif status == "INSUFFICIENT_BALANCE":
                            self.log(f"{white}Auto Upgrade: {red}Not enough coin")
                        else:
                            self.log(f"{white}Auto Upgrade: {red}Unknown")
                    else:
                        self.log(f"{yellow}Auto Upgrade: {red}OFF")

                    # Tap
                    self.log(f"{yellow}Trying to tap...")
                    while True:
                        tap = self.tap(token=token, tap_count=50).json()
                        level = tap["data"]["level"]
                        available_taps = tap["data"]["available_taps"]
                        self.log(
                            f"{green}Level: {white}{level} - {green}Available taps: {white}{available_taps}"
                        )
                        balances = tap["data"]["balance_coins"]
                        for balance in balances:
                            coin_type = balance["currency_symbol"]
                            coin_balance = balance["balance"]
                            self.log(
                                f"{green}{coin_type} balance: {white}{coin_balance:,}"
                            )
                        if available_taps == 0:
                            break
                except Exception as e:
                    self.log(f"{red}Get token error, try to get new query id!")

            print()
            wait_time = 30 * 60
            self.log(f"{yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        pokey = PokeyQuest()
        pokey.main()
    except KeyboardInterrupt:
        sys.exit()
