import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.token import get_token
from core.info import game_data
from core.task import process_do_task, process_watch_ads
from core.claim import process_claim
from core.boost import process_buy_boost

import time
import json


class CyberFinanace:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data-proxy.json")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = base.create_banner(game_name="Cyber Finance")

        # Get config
        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_watch_ads = base.get_config(
            config_file=self.config_file, config_name="auto-watch-ads"
        )

        self.auto_claim = base.get_config(
            config_file=self.config_file, config_name="auto-claim"
        )

        self.auto_buy_hammer = base.get_config(
            config_file=self.config_file, config_name="auto-buy-hammer"
        )

    def main(self):
        while True:
            base.clear_terminal()
            print(self.banner)
            accounts = json.load(open(self.data_file, "r"))["accounts"]
            num_acc = len(accounts)
            base.log(self.line)
            base.log(f"{base.green}Numer of accounts: {base.white}{num_acc}")

            for no, account in enumerate(accounts):
                base.log(self.line)
                base.log(f"{base.green}Account number: {base.white}{no+1}/{num_acc}")
                data = account["acc_info"]
                proxy_info = account["proxy_info"]
                parsed_proxy_info = base.parse_proxy_info(proxy_info)
                if parsed_proxy_info is None:
                    break

                actual_ip = base.check_ip(proxy_info=proxy_info)

                proxies = base.format_proxy(proxy_info=proxy_info)

                try:
                    token = get_token(data=data)

                    if token:
                        balance = game_data(token=token, proxies=proxies)
                        base.log(f"{base.green}Balance: {base.white}{balance:,}")

                        # Do task
                        if self.auto_do_task:
                            base.log(f"{base.yellow}Auto Do Task: {base.green}ON")
                            process_do_task(token=token, proxies=proxies)
                        else:
                            base.log(f"{base.yellow}Auto Do Task: {base.red}OFF")

                        # Watch ads
                        if self.auto_watch_ads:
                            base.log(f"{base.yellow}Auto Watch Ads: {base.green}ON")
                            process_watch_ads(token=token, proxies=proxies)
                        else:
                            base.log(f"{base.yellow}Auto Watch Ads: {base.red}OFF")

                        # Claim
                        if self.auto_claim:
                            base.log(f"{base.yellow}Auto Claim: {base.green}ON")
                            process_claim(token=token, proxies=proxies)
                        else:
                            base.log(f"{base.yellow}Auto Claim: {base.red}OFF")

                        # Buy Hammer
                        if self.auto_buy_hammer:
                            base.log(f"{base.yellow}Auto Buy Hammer: {base.green}ON")
                            hammer_limit_price = 10000
                            process_buy_boost(
                                token=token,
                                limit_price=hammer_limit_price,
                                proxies=proxies,
                            )
                        else:
                            base.log(f"{base.yellow}Auto Buy Hammer: {base.red}OFF")

                        balance = game_data(token=token, proxies=proxies)
                        base.log(f"{base.green}Balance: {base.white}{balance:,}")
                    else:
                        base.log(f"{base.red}Token not found! Please get new query id")
                except Exception as e:
                    base.log(f"{base.red}Error: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        cyberfinance = CyberFinanace()
        cyberfinance.main()
    except KeyboardInterrupt:
        sys.exit()
