import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
import json
import brotli
import urllib.parse

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


class W3BFLIX:
    def __init__(self):
        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Smart Airdrop {white}W3BFLIX Auto Claimer
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

    def headers(self):
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-cache",
            "Origin": "https://w3bflix.world",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://w3bflix.world/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "X-Api-Key": "vL7wcDNndYZOA5fLxtab33wUAAill6Kk",
        }

    def lucky_draw(self, tele_id):
        url = f"https://api.w3bflix.world/v1/users/{tele_id}/luckydraw"

        headers = self.headers()

        payload = {"type": "ton"}

        response = requests.post(url, headers=headers, json=payload)

        return response

    def videos(self):
        url = f"https://api.w3bflix.world/v1/videos"

        headers = self.headers()

        response = requests.get(url, headers=headers)

        return response

    def watch(self, tele_id, vid_id):
        url = f"https://api.w3bflix.world/v1/video/{vid_id}/user/{tele_id}/watch"

        headers = self.headers()

        response = requests.post(url, headers=headers)

        return response

    def claim(self, tele_id, vid_id, claim_data, query_id):
        url = f"https://api.w3bflix.world/v1/video/{vid_id}/user/{tele_id}/earn/{claim_data}"

        headers = self.headers()

        payload = {"initDataRaw": f"{query_id}"}

        data = json.dumps(payload)

        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"

        response = requests.post(url, headers=headers, data=data)

        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def extract_user_info(self, query_string):
        parsed_query = urllib.parse.parse_qs(query_string)

        user_info = parsed_query.get("user", [None])[0]

        if user_info:
            user_data = json.loads(user_info)
            user_id = user_data.get("id")
            first_name = user_data.get("first_name")
            return user_id, first_name
        else:
            return None, None

    def main(self):
        self.clear_terminal()
        print(self.banner)
        data = open(data_file, "r").read().splitlines()
        num_acc = len(data)
        self.log(self.line)
        self.log(f"{green}Number of account: {white}{num_acc}")
        for no, data in enumerate(data):
            self.log(self.line)
            self.log(f"{green}Account number: {white}{no+1}/{num_acc}")
            tele_id, first_name = self.extract_user_info(query_string=data)
            self.log(
                f"{green}Name: {white}{first_name} - {green}Telegram ID: {white}{tele_id}"
            )

            # Daily Lucky Draw
            self.log(f"{yellow}Trying to claim Daily Lucky Draw...")
            try:
                draw = self.lucky_draw(tele_id=tele_id).json()
                rewards = draw["data"]["rewards"]
                self.log(f"{white}Daily Lucky Draw: {green}Success {rewards} points")
            except:
                self.log(f"{white}Daily Lucky Draw: {red}Not time to claim yet")

            # Videos
            self.log(f"{yellow}Start watching video...")
            try:
                videos = self.videos().json()["data"]
                for video in videos:
                    vid_title = video["Title"]
                    vid_id = video["Vid"]
                    watch = self.watch(tele_id=tele_id, vid_id=vid_id).json()
                    claim_data = watch["data"]["watch"]
                    claim_status = watch["data"]["claimedAt"]
                    self.log(f"{white}{vid_title}: {claim_data}")
                    if claim_status is None:
                        time.sleep(30)
                        claim = self.claim(
                            tele_id=tele_id,
                            vid_id=vid_id,
                            claim_data=claim_data,
                            query_id=data,
                        )
                        if claim.status_code == 200:
                            claim_code = claim.json()["data"]["claimCode"]
                            self.log(f"{white}{vid_title}: {green}Claim successful")
                            self.log(
                                f"{white}{vid_title}: {green}/watch {claim_code}:{claim_data}"
                            )
                        else:
                            self.log(f"{white}{vid_title}: {red}Claim failed")
                    else:
                        self.log(f"{white}{vid_title}: {yellow}Claimed already")
            except Exception as e:
                self.log(f"{red}Get videos info error")

        print()
        self.log(
            f"""{yellow}All accounts have been processed. 
        
            If Auto Claim Bot has not sent message automatically, then you should copy message "/watch ...." and send to W3BFLIX bot manually"""
        )


if __name__ == "__main__":
    try:
        w3bflix = W3BFLIX()
        w3bflix.main()
    except KeyboardInterrupt:
        sys.exit()

# Lucky draw
# URL = "https://api.w3bflix.world/v1/users/7132700237/luckydraw"
# method = "POST"
# payload = {"type": "ton"}
# payload = {"type":"ton","address":"0:0496272b6d269db5d9012d59f836edbf2780a472ef2155298d5fd4ff230716f5"}
# {"type":"ton","address":"0:40676a5eeb3285855609f6a54870f7795b8bed0b323f24e96407d073de0eff8b"}
# Success Output = {"status":"success","data":{"rewards":5,"yields":0.0855}}
# Fail Output = {"status":"success","data":{"wait":42052083}}
