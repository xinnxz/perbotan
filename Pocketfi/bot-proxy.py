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

    def mining_info(self, data, proxy_info):
        url = f"https://gm.pocketfi.org/mining/getUserMining"

        headers = self.headers(data=data)

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.get(url=url, headers=headers, proxies=proxies)

        return response

    def claim_mining(self, data, proxy_info):
        url = f"https://gm.pocketfi.org/mining/claimMining"

        headers = self.headers(data=data)

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url=url, headers=headers, proxies=proxies)

        return response

    def daily_boost(self, data, proxy_info):
        url = f"https://bot2.pocketfi.org/boost/activateDailyBoost"

        headers = self.headers(data=data)

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url=url, headers=headers, proxies=proxies)

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

                # Start bot
                try:
                    get_mining_info = self.mining_info(
                        data=data, proxy_info=proxy_info
                    ).json()
                    balance = get_mining_info["userMining"]["gotAmount"]
                    mining_balance = get_mining_info["userMining"]["miningAmount"]

                    self.log(
                        f"{green}Balance: {white}{balance} - {green}Mining Balance: {white}{mining_balance}"
                    )

                    self.log(f"{yellow}Trying to claim...")
                    if mining_balance > 0:
                        claim_mining = self.claim_mining(
                            data=data, proxy_info=proxy_info
                        )
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
                    activate_boost = self.daily_boost(
                        data=data, proxy_info=proxy_info
                    ).json()
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
