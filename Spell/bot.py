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


class Spell:
    def __init__(self):
        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Smart Airdrop {white}Spell Wallet Auto Claimer
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

    def headers(self, auth_data):
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"{auth_data}",
            "Origin": "https://wallet.spell.club",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://wallet.spell.club/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }

    def user_info(self, auth_data):
        url = f"https://wallet-api.spell.club/user"

        headers = self.headers(auth_data=auth_data)

        response = requests.get(url, headers=headers)

        return response

    def claim(self, auth_data):
        url = f"https://wallet-api.spell.club/claim"

        headers = self.headers(auth_data=auth_data)

        response = requests.post(url, headers=headers)

        return response

    def check_quest(self, auth_data):
        url = f"https://wallet-api.spell.club/quests?limit=20&page=0"

        headers = self.headers(auth_data=auth_data)

        response = requests.get(url, headers=headers)

        return response

    def claim_quest(self, auth_data, quest_id):
        url = f"https://wallet-api.spell.club/quest/{quest_id}/claim"

        headers = self.headers(auth_data=auth_data)

        response = requests.post(url, headers=headers)

        return response

    def check_step(self, auth_data, quest_id):
        url = f"https://wallet-api.spell.club/quest/{quest_id}"

        headers = self.headers(auth_data=auth_data)

        response = requests.get(url, headers=headers)

        return response

    def complete_step(self, auth_data, step_id):
        url = f"https://wallet-api.spell.club/quest/step/{step_id}/complete"

        headers = self.headers(auth_data=auth_data)

        response = requests.post(url, headers=headers)

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
            for no, auth_data in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")

                # Get user info
                try:
                    user_info = self.user_info(auth_data=auth_data).json()
                    balance = user_info["balance"]
                    self.log(f"{green}Balance: {white}{balance/10**6}")
                except Exception as e:
                    self.log(f"{red}Get user info error!!!")

                # Claim
                try:
                    self.log(f"{yellow}Trying to claim...")
                    claim = self.claim(auth_data=auth_data)
                    if claim.status_code == 200:
                        self.log(f"{green}Claim successful!")
                        try:
                            user_info = self.user_info(auth_data=auth_data).json()
                            balance = user_info["balance"]
                            self.log(f"{green}Current balance: {white}{balance/10**6}")
                        except Exception as e:
                            self.log(f"{red}Get user info error!!!")
                    else:
                        self.log(f"{yellow}Not time to claim yet!")
                except Exception as e:
                    self.log(f"{red}Claim error!!!")

                # Quest
                try:
                    self.log(f"{yellow}Checking quests...")
                    check_quest = self.check_quest(auth_data=auth_data).json()
                    for quest in check_quest:
                        quest_name = quest["name"]
                        quest_id = quest["id"]
                        quest_status = quest["is_claimed"]
                        if quest_status:
                            self.log(
                                f"{white}Quest ID: {quest_id} - Name: {quest_name} - Status: {green}Completed"
                            )
                        else:
                            self.log(
                                f"{yellow}Checking incompeted quests and doing tasks..."
                            )
                            try:
                                check_step = self.check_step(
                                    auth_data=auth_data, quest_id=quest_id
                                ).json()
                                steps = check_step["steps"]
                                for step in steps:
                                    step_name = step["name"]
                                    step_id = step["id"]
                                    step_status = step["is_passed"]
                                    if step_status:
                                        self.log(
                                            f"{white}Quest ID: {quest_id} - Step: {step_id} - Name: {step_name} - Status: {green}Completed"
                                        )
                                    else:
                                        complete_step = self.complete_step(
                                            auth_data=auth_data, step_id=step_id
                                        )
                                        if complete_step.status_code == 200:
                                            self.log(
                                                f"{white}Quest ID: {quest_id} - Step: {step_id} - Name: {step_name} - Status: {green}Done {red}(except Join Telegram group/channel step)"
                                            )
                                        else:
                                            self.log(
                                                f"{white}Quest ID: {quest_id} - Step: {step_id} - Name: {step_name} - Status: {red}Incompleted"
                                            )
                            except Exception as e:
                                self.log(f"{red}Check incompleted quest error!!!")

                            try:
                                self.log(f"{yellow}Trying to claim quests...")
                                claim_quest = self.claim_quest(
                                    auth_data=auth_data, quest_id=quest_id
                                )
                                if claim_quest.status_code == 200:
                                    self.log(
                                        f"{white}Quest ID: {quest_id} - Step: {step_id} - Name: {step_name} - Status: {green}Claimed"
                                    )
                                else:
                                    self.log(
                                        f"{white}Quest ID: {quest_id} - Step: {step_id} - Name: {step_name} - Status: {red}Incompleted (please Join Telegram group/channel by yourself)"
                                    )
                            except Exception as e:
                                self.log(f"{red}Claim quest error!!!")
                except Exception as e:
                    self.log(f"{red}Check quest error!!!")

            print()
            wait_time = 30 * 60
            self.log(f"{yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        spell = Spell()
        spell.main()
    except KeyboardInterrupt:
        sys.exit()
