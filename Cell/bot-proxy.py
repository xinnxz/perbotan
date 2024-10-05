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
data_file = os.path.join(script_dir, "data-proxy.json")


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

    def proxies(self, proxy_info):
        return {"http": f"{proxy_info}", "https": f"{proxy_info}"}

    def user_info(self, auth_data, proxy_info):
        url = f"https://cellcoin.org/users/session"

        headers = self.headers(auth_data=auth_data)

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.get(url, headers=headers, proxies=proxies)

        return response

    def claim_sotrage(self, auth_data, proxy_info):
        url = f"https://cellcoin.org/cells/claim_storage"

        headers = self.headers(auth_data=auth_data)

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url, headers=headers, proxies=proxies)

        return response

    def submit_click(self, auth_data, num_click, proxy_info):
        url = f"https://cellcoin.org/cells/submit_clicks"

        headers = self.headers(auth_data=auth_data)

        payload = {"clicks_amount": num_click}

        data = json.dumps(payload)

        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"

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
        self.clear_terminal()
        print(self.banner)
        accounts = json.load(open(data_file, "r"))["accounts"]
        num_acc = len(accounts)
        self.log(self.line)
        self.log(f"{green}Numer of account: {white}{num_acc}")
        while True:
            for no, account in enumerate(accounts):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")
                auth_data = account["acc_info"]
                proxy_info = account["proxy_info"]
                parsed_proxy_info = self.parse_proxy_info(proxy_info)
                if parsed_proxy_info is None:
                    self.log(
                        f"{red}Check proxy format: {white}http://user:pass@ip:port"
                    )
                    break
                ip_adress = parsed_proxy_info["ip"]
                self.log(f"{green}IP Address: {white}{ip_adress}")

                try:
                    user_info = self.user_info(
                        auth_data=auth_data, proxy_info=proxy_info
                    ).json()
                    user_name = user_info["user"]["username"]
                    first_name = user_info["user"]["first_name"]
                    balance = user_info["cell"]["balance"]
                    self.log(f"{green}Account Info: {white}{first_name} - {user_name}")
                    self.log(f"{green}Balance: {white}{balance/10**6}")
                except Exception as e:
                    self.log(f"{red}Get user info error!!!")

                try:
                    self.log(f"{yellow}Claiming...")
                    claim_storage = self.claim_sotrage(
                        auth_data=auth_data, proxy_info=proxy_info
                    ).json()
                    balance = claim_storage["cell"]["balance"]
                    self.log(f"{green}Balance after Claim: {white}{balance/10**6}")
                except Exception as e:
                    self.log(f"{red}Claim too early!!!")

                try:
                    self.log(f"{yellow}Tapping to earn...")
                    submit_click = self.submit_click(
                        auth_data=auth_data, num_click=5, proxy_info=proxy_info
                    ).json()
                    click_left = submit_click["cell"]["energy_amount"]
                    final_click = self.submit_click(
                        auth_data=auth_data, num_click=click_left, proxy_info=proxy_info
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
