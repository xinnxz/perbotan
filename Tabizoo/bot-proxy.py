import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.info import get_info
from core.task import process_check_in, process_do_project_task, process_do_normal_task
from core.mine import process_claim
from core.upgrade import process_upgrade

import time
import json


class TabiZoo:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data-proxy.json")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = base.create_banner(game_name="TabiZoo")

        # Get config
        self.auto_check_in = base.get_config(
            config_file=self.config_file, config_name="auto-check-in"
        )

        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_claim = base.get_config(
            config_file=self.config_file, config_name="auto-claim"
        )

        self.auto_upgrade = base.get_config(
            config_file=self.config_file, config_name="auto-upgrade"
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
                    # Info
                    get_info(data=data, proxies=proxies)

                    # Check in
                    if self.auto_check_in:
                        base.log(f"{base.yellow}Auto Check-in: {base.green}ON")
                        process_check_in(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Check-in: {base.red}OFF")

                    # Do task
                    if self.auto_do_task:
                        base.log(f"{base.yellow}Auto Do Task: {base.green}ON")
                        process_do_project_task(data=data, proxies=proxies)
                        process_do_normal_task(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Do Task: {base.red}OFF")

                    # Claim
                    if self.auto_claim:
                        base.log(f"{base.yellow}Auto Claim: {base.green}ON")
                        process_claim(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Claim: {base.red}OFF")

                    # Upgrade
                    if self.auto_upgrade:
                        base.log(f"{base.yellow}Auto Upgrade: {base.green}ON")
                        process_upgrade(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Upgrade: {base.red}OFF")

                except Exception as e:
                    base.log(f"{base.red}Error: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        tabi = TabiZoo()
        tabi.main()
    except KeyboardInterrupt:
        sys.exit()
