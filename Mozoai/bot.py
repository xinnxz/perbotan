import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
import random
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


class MozoAI:
    def __init__(self):
        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Smart Airdrop {white}MozoAI Auto Claimer
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
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"{data}",
            "Cache-Control": "no-cache",
            "Origin": "https://beta.mozo.xyz",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://beta.mozo.xyz/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }

    def info(self, data):
        url = "https://api.mozo.xyz/v1/ai/tap/info/"

        headers = self.headers(data=data)

        response = requests.get(url=url, headers=headers)

        return response

    def claim(self, data, tap_times, multitap_point):
        url = "https://api.mozo.xyz/v1/ai/tap/claim/"

        headers = self.headers(data=data)

        payload = {
            "point": tap_times * multitap_point,
            "type": "normal",
            "tap_times": tap_times,
        }

        payload = json.dumps(payload)

        headers["Content-Length"] = str(len(payload))
        headers["Content-Type"] = "application/json"

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def turbo_claim(self, data, game_id, tap_times, multitap_point):
        url = "https://api.mozo.xyz/v1/ai/tap/claim/"

        headers = self.headers(data=data)

        payload = {
            "point": tap_times * multitap_point * 3,
            "type": "turbo",
            "tap_times": tap_times,
            "id": game_id,
        }

        payload = json.dumps(payload)

        headers["Content-Length"] = str(len(payload))
        headers["Content-Type"] = "application/json"

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def recover_energy(self, data):
        url = "https://api.mozo.xyz/v1/ai/tap/point/recover/"

        headers = self.headers(data=data)

        response = requests.post(url=url, headers=headers)

        return response

    def lightning_tap(self, data):
        url = "https://api.mozo.xyz/v1/ai/tap/turbo/recover/"

        headers = self.headers(data=data)

        response = requests.post(url=url, headers=headers)

        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def breakdown_seconds(self, wait_time):
        wait_hours = int(wait_time // 3600)
        wait_minutes = int((wait_time % 3600) // 60)
        wait_seconds = int(wait_time % 60)

        return f"{wait_hours:02}:{wait_minutes:02}:{wait_seconds:02}"

    def main(self):
        while True:
            self.clear_terminal()
            print(self.banner)
            data = open(data_file, "r").read().splitlines()
            num_acc = len(data)
            self.log(self.line)
            self.log(f"{green}Numer of account: {white}{num_acc}")
            remain_time_list = []
            for no, data in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")

                # Get info and claim
                try:
                    while True:
                        info = self.info(data=data).json()
                        tap_remain_point = info["data"]["tap_remain_point"]
                        multitap_point = info["data"]["multitap_point"]
                        tap_times = tap_remain_point // multitap_point
                        balance = info["data"]["point"]
                        self.log(f"{green}Balance: {white}{balance}")
                        if tap_times > 0:
                            try:
                                self.log(f"{yellow}Processing normal tap...")
                                claim = self.claim(
                                    data=data,
                                    tap_times=tap_times,
                                    multitap_point=multitap_point,
                                ).json()
                            except Exception as e:
                                self.log(f"{red}Claim error!!!")
                        else:
                            try:
                                self.log(f"{yellow}Trying to recover energy...")
                                recover_energy = self.recover_energy(data=data).json()
                                if recover_energy["err_msg"] == "ok":
                                    self.log(f"{green}Recovery energy successful!")
                                    pass
                                else:
                                    self.log(f"{yellow}No energy left!")
                                    break
                            except Exception as e:
                                self.log(f"{red}Recover energy error!!!")

                except Exception as e:
                    self.log(f"{red}Get info error!!!")

                # Lighning Tap (20s)
                try:
                    while True:
                        self.log(f"{yellow}Trying to play Lightning Tap...")
                        info = self.info(data=data).json()
                        multitap_point = info["data"]["multitap_point"]
                        lightning_tap = self.lightning_tap(data=data).json()
                        if lightning_tap["err_msg"] == "ok":
                            self.log(f"{yellow}Playing Lightning Tap...")
                            game_id = lightning_tap["data"]["id"]
                            self.log(f"{yellow}Play for 20s")
                            time.sleep(20)
                            tap_times = random.randint(150, 200)
                            try:
                                turbo_claim = self.turbo_claim(
                                    data=data,
                                    game_id=game_id,
                                    tap_times=tap_times,
                                    multitap_point=multitap_point,
                                ).json()
                                balance = turbo_claim["data"]["point"]
                                self.log(
                                    f"{green}Balance after Lightning Tap: {white}{balance}"
                                )
                            except Exception as e:
                                self.log(f"{red}Turbo claim error!!!")
                        else:
                            self.log(f"{yellow}No Lightning Tap game ticket!")
                            break
                except Exception as e:
                    self.log(f"{red}Lightning Tap error!!!")

                # Get remain time
                try:
                    info = self.info(data=data).json()
                    balance = info["data"]["point"]
                    recover_remain_time = info["data"]["recover_remain_time"]
                    self.log(f"{green}Current balance: {white}{balance}")
                    self.log(
                        f"{green}Remain time: {white}{self.breakdown_seconds(recover_remain_time)}"
                    )
                    remain_time_list.append(recover_remain_time)
                except Exception as e:
                    self.log(f"{red}Get remain time error!!!")

            print()
            # Wait time
            wait_time = min(remain_time_list, default=15 * 60)
            self.log(f"{yellow}Wait for {self.breakdown_seconds(wait_time)}!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        mozo = MozoAI()
        mozo.main()
    except KeyboardInterrupt:
        sys.exit()
