import os
import sys
from colorama import *
import json
from datetime import datetime
import requests
from requests.auth import HTTPProxyAuth

init(autoreset=True)


class Base:
    def __init__(self):
        # Initialize colorama styles
        self.red = Fore.LIGHTRED_EX
        self.yellow = Fore.LIGHTYELLOW_EX
        self.green = Fore.LIGHTGREEN_EX
        self.black = Fore.LIGHTBLACK_EX
        self.blue = Fore.LIGHTBLUE_EX
        self.white = Fore.LIGHTWHITE_EX
        self.reset = Style.RESET_ALL

    def file_path(self, file_name: str):
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Get the parent directory of the script directory
        parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

        # Join the parent directory with the file name to form the full file path
        file_path = os.path.join(parent_dir, file_name)

        return file_path

    def create_line(self, length: int):
        # Create line based on length
        line = self.white + "~" * length
        return line

    def create_banner(self, game_name: str):
        # Create banner with game name
        banner = f"""
        {self.blue}Smart Airdrop {self.white}{game_name} Auto Claimer
        t.me/smartairdrop2120
        
        """
        return banner

    def get_config(self, config_file: str, config_name: str):
        # Get config from config file
        config_status = (
            json.load(open(config_file, "r")).get(config_name, "false").lower()
            == "true"
        )
        return config_status

    def clear_terminal(self):
        # For Windows
        if os.name == "nt":
            _ = os.system("cls")
        # For macOS and Linux
        else:
            _ = os.system("clear")

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{self.black}[{now}]{self.reset} {msg}{self.reset}")

    # Handle proxy version
    def format_proxy(self, proxy_info):
        return {"http": f"{proxy_info}", "https": f"{proxy_info}"}

    def check_ip(self, proxy_info):
        url = "https://api.ipify.org?format=json"

        proxies = self.format_proxy(proxy_info=proxy_info)

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
            actual_ip = response.json().get("ip")
            self.log(f"{self.green}Actual IP Address: {self.white}{actual_ip}")
            return actual_ip
        except requests.exceptions.RequestException as e:
            self.log(f"{self.red}IP check failed: {self.white}{e}")
            return None

    def parse_proxy_info(self, proxy_info):
        try:
            stripped_url = proxy_info.split("://", 1)[-1]
            credentials, endpoint = stripped_url.split("@", 1)
            user_name, password = credentials.split(":", 1)
            ip, port = endpoint.split(":", 1)
            self.log(f"{self.green}Input IP Address: {self.white}{ip}")
            return {"user_name": user_name, "pass": password, "ip": ip, "port": port}
        except:
            self.log(
                f"{self.red}Check proxy format: {self.white}http://user:pass@ip:port"
            )
            return None


base = Base()
