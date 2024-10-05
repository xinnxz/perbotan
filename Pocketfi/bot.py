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


class PocketFi:
    def __init__(self):
        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Smart Airdrop {white}PocketFi Auto Claimer
        t.me/smartairdrop2120
        
        """

    # Clear the terminal
    def clear_terminal(self):
        # For Windows
        if os.name == "nt":
            _ = os.system("cls")
        # For macOS and Linux
        else:
            _ = os.system("clear")

    def headers(self, data):
        return {
            "Accept": "application/json, text/plain, */*",
            "Telegramrawdata": f"{data}",
            "Origin": "https://pocketfi.app",
            "Referer": "https://pocketfi.app/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

    def mining_info(self, data):
        url = f"https://gm.pocketfi.org/mining/getUserMining"

        headers = self.headers(data=data)

        response = requests.get(url=url, headers=headers)

        return response

    def claim_mining(self, data):
        url = f"https://gm.pocketfi.org/mining/claimMining"

        headers = self.headers(data=data)

        response = requests.post(url=url, headers=headers)

        return response

    def daily_boost(self, data):
        url = f"https://bot2.pocketfi.org/boost/activateDailyBoost"

        headers = self.headers(data=data)

        response = requests.post(url=url, headers=headers)

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

                # Start bot
                try:
                    get_mining_info = self.mining_info(data=data).json()
                    balance = get_mining_info["userMining"]["gotAmount"]
                    mining_balance = get_mining_info["userMining"]["miningAmount"]

                    self.log(
                        f"{green}Balance: {white}{balance} - {green}Mining Balance: {white}{mining_balance}"
                    )

                    self.log(f"{yellow}Trying to claim...")
                    if mining_balance > 0:
                        claim_mining = self.claim_mining(data=data)
                        if claim_mining.status_code == 200:
                            self.log(f"{white}Claim Mining: {green}Success")
                            balance = claim_mining.json()["userMining"]["gotAmount"]
                            mining_balance = claim_mining.json()["userMining"][
                                "miningAmount"
                            ]

                            self.log(
                                f"{green}Balance: {white}{balance} - {green}Mining Balance: {white}{mining_balance}"
                            )
                        else:
                            self.log(f"{white}Claim Mining: {red}Error")
                    else:
                        self.log(f"{white}Claim Mining: {red}No point to claim")

                    self.log(f"{yellow}Trying to activate daily boost...")
                    activate_boost = self.daily_boost(data=data).json()
                    activate_status = activate_boost["updatedForDay"]
                    if activate_status is not None:
                        self.log(f"{white}Activate Daily Boost: {green}Success")
                    else:
                        self.log(f"{white}Activate Daily Boost: {red}Activated already")

                except Exception as e:
                    self.log(f"{red}Error {e}")

            print()
            wait_time = 60 * 60
            self.log(f"{yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        pocketfi = PocketFi()
        pocketfi.main()
    except KeyboardInterrupt:
        sys.exit()
