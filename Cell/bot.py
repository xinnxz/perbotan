import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
import json

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


class CELL:
    def __init__(self):
        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Smart Airdrop {white}CELL Wallet Auto Claimer
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
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"{auth_data}",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "cellcoin.org",
            "Origin": "https://cell-frontend.s3.us-east-1.amazonaws.com",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://cell-frontend.s3.us-east-1.amazonaws.com/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }

    def user_info(self, auth_data):
        url = f"https://cellcoin.org/users/session"

        headers = self.headers(auth_data=auth_data)

        response = requests.get(url, headers=headers)

        return response

    def claim_sotrage(self, auth_data):
        url = f"https://cellcoin.org/cells/claim_storage"

        headers = self.headers(auth_data=auth_data)

        response = requests.post(url, headers=headers)

        return response

    def submit_click(self, auth_data, num_click):
        url = f"https://cellcoin.org/cells/submit_clicks"

        headers = self.headers(auth_data=auth_data)

        payload = {"clicks_amount": num_click}

        data = json.dumps(payload)

        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def main(self):
        self.clear_terminal()
        print(self.banner)
        data = open(data_file, "r").read().splitlines()
        num_acc = len(data)
        self.log(self.line)
        self.log(f"{green}Numer of account: {white}{num_acc}")
        while True:
            for no, auth_data in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")
                try:
                    user_info = self.user_info(auth_data=auth_data).json()
                    user_name = user_info["user"]["username"]
                    first_name = user_info["user"]["first_name"]
                    balance = user_info["cell"]["balance"]
                    self.log(f"{green}Account Info: {white}{first_name} - {user_name}")
                    self.log(f"{green}Balance: {white}{balance/10**6}")
                except Exception as e:
                    self.log(f"{red}Get user info error!!!")

                try:
                    self.log(f"{yellow}Claiming...")
                    claim_storage = self.claim_sotrage(auth_data=auth_data).json()
                    balance = claim_storage["cell"]["balance"]
                    self.log(f"{green}Balance after Claim: {white}{balance/10**6}")
                except Exception as e:
                    self.log(f"{red}Claim too early!!!")

                try:
                    self.log(f"{yellow}Tapping to earn...")
                    submit_click = self.submit_click(
                        auth_data=auth_data, num_click=5
                    ).json()
                    click_left = submit_click["cell"]["energy_amount"]
                    final_click = self.submit_click(
                        auth_data=auth_data, num_click=click_left
                    ).json()
                    balance = final_click["cell"]["balance"]
                    self.log(f"{green}Balance after Click: {white}{balance/10**6}")
                except Exception as e:
                    self.log(f"{red}Click error!!!")

            print()
            wait_time = 30 * 60
            self.log(f"{yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        cell = CELL()
        cell.main()
    except KeyboardInterrupt:
        sys.exit()
