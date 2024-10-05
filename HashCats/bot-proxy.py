import sys

sys.dont_write_bytecode = True

from package import base
from package.core.info import users, miner, balance
from package.core.earn import process_claim_daily_task, process_claim_social_tasks
from package.core.ref import process_claim_ref
from package.core.tapper import process_tap
from package.core.cards import process_buy_card
from package.core.stake import process_stake

import time
import json
import brotli


class HashCats:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data-proxy.json")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = base.create_banner(game_name="HashCats")

        # Get config
        self.auto_claim_daily_reward = base.get_config(
            config_file=self.config_file, config_name="auto-claim-daily-reward"
        )

        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_claim_ref = base.get_config(
            config_file=self.config_file, config_name="auto-claim-ref"
        )

        self.auto_tap = base.get_config(
            config_file=self.config_file, config_name="auto-tap"
        )

        self.auto_buy_card = base.get_config(
            config_file=self.config_file, config_name="auto-buy-card"
        )

        self.auto_stake = base.get_config(
            config_file=self.config_file, config_name="auto-stake"
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
                token = account["acc_info"]
                proxy_info = account["proxy_info"]
                parsed_proxy_info = base.parse_proxy_info(proxy_info)
                if parsed_proxy_info is None:
                    break

                actual_ip = base.check_ip(proxy_info=proxy_info)

                proxies = base.format_proxy(proxy_info=proxy_info)

                try:
                    # Get user info
                    mined_coins = users(token=token, proxies=proxies)
                    name, level, tap, energy_per_tap, energy = miner(
                        token=token, proxies=proxies
                    )
                    current_balance = balance(token=token, proxies=proxies)

                    base.log(
                        f"{base.green}Miner: {base.white}{name} - {base.green}Level: {base.white}{level} - {base.green}Tap: {base.white}{tap} - {base.green}Energy per Tap: {base.white}{energy_per_tap} - {base.green}Energy: {base.white}{energy}"
                    )
                    base.log(f"{base.green}Mined Coins: {base.white}{mined_coins}")
                    base.log(f"{base.green}Balance: {base.white}{current_balance}")

                    # Claim daily reward
                    if self.auto_claim_daily_reward:
                        base.log(
                            f"{base.yellow}Auto Claim Daily Reward: {base.green}ON"
                        )
                        process_claim_daily_task(token=token, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Claim Daily Reward: {base.red}OFF")

                    # Do task
                    if self.auto_do_task:
                        base.log(f"{base.yellow}Auto Do Task: {base.green}ON")
                        process_claim_social_tasks(token=token, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Do Task: {base.red}OFF")

                    # Claim ref
                    if self.auto_claim_ref:
                        base.log(f"{base.yellow}Auto Claim Ref: {base.green}ON")
                        process_claim_ref(token=token, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Claim Ref: {base.red}OFF")

                    # Tapping
                    if self.auto_tap:
                        base.log(f"{base.yellow}Auto Tap: {base.green}ON")
                        process_tap(token=token, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Tap: {base.red}OFF")

                    # Buy cards
                    if self.auto_buy_card:
                        base.log(f"{base.yellow}Auto Buy Card: {base.green}ON")
                        process_buy_card(token=token, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Buy Card: {base.red}OFF")

                    # Stake
                    if self.auto_stake:
                        base.log(f"{base.yellow}Auto Stake: {base.green}ON")
                        process_stake(token=token, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Stake: {base.red}OFF")

                except Exception as e:
                    base.log(f"{base.red}Error: {base.white}{e}")

            print()
            wait_time = 30 * 60
            base.log(f"{base.yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        hashcats = HashCats()
        hashcats.main()
    except KeyboardInterrupt:
        sys.exit()
