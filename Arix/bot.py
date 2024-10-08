import os
import sys
import time
import requests
from colorama import *
from datetime import datetime

init(autoreset=True)

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


class ArixDEX:
    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Content-Length": "0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://miner-webapp-pi.vercel.app",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://miner-webapp-pi.vercel.app/",
            "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }

        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Smart Airdrop {white}ArixDEX Auto Claimer
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

    def user_info(self, telegram_id):
        url = f"https://miner-webapp-fz9k.vercel.app/api/user?id={telegram_id}"

        headers = self.headers

        response = requests.get(url, headers=headers)

        return response

    def arix_claimer(self, telegram_id):
        url = f"https://miner-webapp-pi.vercel.app/api/claim?id={telegram_id}"

        headers = self.headers

        response = requests.post(url, headers=headers)

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
            for no, telegram_id in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")
                try:
                    user_info = self.user_info(telegram_id=telegram_id).json()
                    first_name = user_info["first_name"]
                    last_name = user_info["last_name"]
                    user_name = user_info["username"]
                    tele_id = user_info["id"]
                    balance = user_info["balance"]
                    self.log(
                        f"{green}Account Info: {white}{first_name} {last_name} ({user_name} - {tele_id})"
                    )
                    self.log(f"{green}Balance: {white}{balance}")
                except Exception as e:
                    self.log(f"{red}Get user info error!!!")

                try:
                    claim = self.arix_claimer(telegram_id=telegram_id).json()
                    claim_balance = claim["balance"]
                    self.log(f"{green}Balance after Claim: {white}{claim_balance}")
                except Exception as e:
                    self.log(f"{red}Claim error!!!")

            print()
            wait_time = 30 * 60
            self.log(f"{yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        arix = ArixDEX()
        arix.main()
    except KeyboardInterrupt:
        sys.exit()
