import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
import random
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


class ArenaGames:
    def __init__(self):
        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Smart Airdrop {white}ArenaGames Auto Claimer
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
            "At": f"{self.get_id(data)}",
            "Cache-Control": "no-cache",
            "Origin": "https://bot-coin.arenavs.com",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://bot-coin.arenavs.com/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Tg": f"{data}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }

    def user_info(self, data):
        url = "https://bot.arenavs.com/v1/profile"

        headers = self.headers(data=data)

        response = requests.get(url=url, headers=headers)

        return response

    def get_task(self, data):
        url = "https://bot.arenavs.com/v1/profile/tasks?page=1&limit=20"

        headers = self.headers(data=data)

        response = requests.get(url=url, headers=headers)

        return response

    def do_task(self, data, task_id):
        url = f"https://bot.arenavs.com/v1/profile/tasks/{task_id}"

        headers = self.headers(data=data)

        response = requests.post(url=url, headers=headers)

        return response

    def claim_task(self, data, task_id):
        url = f"https://bot.arenavs.com/v1/profile/tasks/{task_id}/claim"

        headers = self.headers(data=data)

        response = requests.post(url=url, headers=headers)

        return response

    def check_status(self, data):
        url = "https://bot.arenavs.com/v1/profile/exp-farm-coin"

        headers = self.headers(data=data)

        response = requests.get(url=url, headers=headers)

        return response

    def farm_coin(self, data):
        url = "https://bot.arenavs.com/v1/profile/farm-coin"

        headers = self.headers(data=data)

        response = requests.post(url=url, headers=headers)

        return response

    def check_ref_coin(self, data):
        url = "https://bot.arenavs.com/v1/profile/refs/coin"

        headers = self.headers(data=data)

        response = requests.get(url=url, headers=headers)

        return response

    def get_ref_coin(self, data):
        url = "https://bot.arenavs.com/v1/profile/get-ref-coin"

        headers = self.headers(data=data)

        response = requests.post(url=url, headers=headers)

        return response

    def attempts_left(self, data):
        url = "https://bot.arenavs.com/v1/game/attempts-left"

        headers = self.headers(data=data)

        response = requests.get(url=url, headers=headers)

        return response

    def start_game(self, data):
        url = "https://bot.arenavs.com/v1/game/start"

        headers = self.headers(data=data)

        response = requests.post(url=url, headers=headers)

        return response

    def stop_game(self, data):
        url = "https://bot.arenavs.com/v1/game/stop"

        headers = self.headers(data=data)

        xp = random.randint(500, 800)
        height = random.randint(15, 25)
        somersault = random.randint(30, 40)

        payload = {
            "xp": xp,
            "height": height,
            "somersault": somersault,
            "time": "60000",
        }

        data = json.dumps(payload)

        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"

        response = requests.post(url=url, headers=headers, data=data)

        return response, xp

    def play_game(self, data):
        self.log(f"{yellow}Playing game...")
        start_game = self.start_game(data=data).json()
        try:
            start_status = start_game["data"]["status"]
            if start_status:
                self.log(f"{white}Play for 60 seconds")
                time.sleep(60)
                stop_game, xp = self.stop_game(data=data)
                stop_status = stop_game.json()["data"]["status"]
                if stop_status:
                    self.log(f"{green}XP earned from Game: {yellow}{xp}")
                else:
                    self.log(f"{red}Stop game failed")
                    return False
            else:
                self.log(f"{red}Start game failed")
                return False
        except:
            stop_game, xp = self.stop_game(data=data)
            stop_status = stop_game.json()["data"]["status"]
            if stop_status:
                self.log(f"{green}XP earned from Game: {yellow}{xp}")
            else:
                self.log(f"{red}Stop game failed")
                return False

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def get_id(self, query_id):
        parsed_query = urllib.parse.parse_qs(query_id)

        user_info = urllib.parse.unquote(parsed_query["user"][0])

        user_dict = json.loads(user_info)

        user_id = user_dict["id"]

        return user_id

    def main(self):
        while True:
            self.clear_terminal()
            print(self.banner)
            data = open(data_file, "r").read().splitlines()
            num_acc = len(data)
            self.log(self.line)
            self.log(f"{green}Numer of account: {white}{num_acc}")
            end_at_list = []
            for no, data in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")

                # Get user info
                try:
                    user_info = self.user_info(data=data).json()
                    user_name = user_info["data"]["first_name"]
                    balance = user_info["data"]["balance"]["$numberDecimal"]
                    end_at = float(user_info["data"]["farmEnd"]) / 1000
                    readable_time = datetime.fromtimestamp(end_at).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    self.log(f"{green}User name: {white}{user_name}")
                    self.log(f"{green}Balance: {white}{round(float(balance), 2)}")
                    self.log(f"{green}Farm end at: {white}{readable_time}")
                    end_at_list.append(end_at)
                except Exception as e:
                    self.log(f"{red}Get user info error!!!")

                # Do tasks
                try:
                    get_task = self.get_task(data=data).json()
                    tasks = get_task["data"]["docs"]
                    task_info = [
                        {
                            "task_id": task["_id"],
                            "task_name": task["title"],
                            "task_status": task["status"],
                        }
                        for task in tasks
                    ]
                    # Filtering tasks based on their status
                    pending_tasks = [
                        task for task in task_info if task["task_status"] == "pending"
                    ]
                    if pending_tasks:
                        for task in pending_tasks:
                            task_id = task["task_id"]
                            task_name = task["task_name"]
                            result = self.do_task(data=data, task_id=task_id).json()[
                                "data"
                            ]["status"]
                            self.log(
                                f"{white}{task_name}: {yellow}Doing task... {white}Result: {yellow}{result}"
                            )

                    completed_tasks = [
                        task for task in task_info if task["task_status"] == "completed"
                    ]
                    if completed_tasks:
                        for task in completed_tasks:
                            task_id = task["task_id"]
                            task_name = task["task_name"]
                            result = self.claim_task(data=data, task_id=task_id).json()[
                                "data"
                            ]["status"]
                            print(
                                f"{white}{task_name}: {yellow}Claiming task... {white}Result: {yellow}{result}"
                            )

                    claim_tasks = [
                        task for task in task_info if task["task_status"] == "claim"
                    ]
                    if claim_tasks:
                        for task in claim_tasks:
                            task_id = task["task_id"]
                            task_name = task["task_name"]
                            self.log(f"{white}{task_name}: {green}Task completed")
                except Exception as e:
                    self.log(f"{red}Get task error!!!")

                # Farm coin
                try:
                    self.log(f"{yellow}Trying to farm coin...")
                    farm_coin = self.farm_coin(data=data)
                    try:
                        if farm_coin.json()["statusCode"] == 400:
                            self.log(f"{yellow}Farm too early!")
                        elif farm_coin.json()["status"] == "ok":
                            self.log(f"{yellow}Farm successful!")
                    except:
                        pass

                    user_info = self.user_info(data=data).json()
                    balance = user_info["data"]["balance"]["$numberDecimal"]
                    self.log(
                        f"{green}Current balance: {white}{round(float(balance), 2)}"
                    )
                except Exception as e:
                    self.log(f"{red}Farm error !!!")

                # Get ref coin
                try:
                    self.log(f"{yellow}Checking coin from refs...")
                    check_ref_coin = self.check_ref_coin(data=data).json()
                    ref_coin = check_ref_coin["data"]["allCoin"]["$numberDecimal"]
                    if float(ref_coin) > 0:
                        self.log(
                            f"{yellow}Getting {round(float(ref_coin), 2)} XP from refs..."
                        )
                        get_ref_coin = self.get_ref_coin(data=data).json()
                        balance = get_ref_coin["data"]["balance"]["$numberDecimal"]
                        self.log(
                            f"{green}Balance after getting XP from refs: {white}{round(float(balance), 2)}"
                        )
                    else:
                        self.log(f"{yellow}No coin from refs!")
                except Exception as e:
                    self.log(f"{red}Farm ref coin error !!!")

                # Play game
                try:
                    while True:
                        attempts_left = self.attempts_left(data=data).json()
                        game_left = attempts_left["data"]["quantity"]
                        self.log(f"{green}Game tickets: {white}{game_left}")
                        if int(game_left) > 0:
                            self.play_game(data=data)
                            user_info = self.user_info(data=data).json()
                            balance = user_info["data"]["balance"]["$numberDecimal"]
                            self.log(
                                f"{green}Balance after Game: {white}{round(float(balance), 2)}"
                            )
                        else:
                            self.log(f"{yellow}No ticket available!")
                            break
                except Exception as e:
                    self.log(f"{red}Get attempts left error!!!")

            print()
            # Wait time
            if end_at_list:
                now = datetime.now().timestamp()
                wait_times = [end_at - now for end_at in end_at_list if end_at > now]
                if wait_times:
                    wait_time = min(wait_times)
                else:
                    wait_time = 15 * 60
            else:
                wait_time = 15 * 60

            wait_hours = int(wait_time // 3600)
            wait_minutes = int((wait_time % 3600) // 60)
            wait_seconds = int(wait_time % 60)

            wait_message_parts = []
            if wait_hours > 0:
                wait_message_parts.append(f"{wait_hours} hours")
            if wait_minutes > 0:
                wait_message_parts.append(f"{wait_minutes} minutes")
            if wait_seconds > 0:
                wait_message_parts.append(f"{wait_seconds} seconds")

            wait_message = ", ".join(wait_message_parts)
            self.log(f"{yellow}Wait for {wait_message}!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        arena = ArenaGames()
        arena.main()
    except KeyboardInterrupt:
        sys.exit()
