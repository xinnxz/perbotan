import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.login import get_cookie
from core.info import get_info
from core.tap import process_tap

import time


class xKuCoin:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = base.create_banner(game_name="xKuCoin")

    def main(self):
        while True:
            base.clear_terminal()
            print(self.banner)
            data = open(self.data_file, "r").read().splitlines()
            num_acc = len(data)
            base.log(self.line)
            base.log(f"{base.green}Number of accounts: {base.white}{num_acc}")

            for no, data in enumerate(data):
                base.log(self.line)
                base.log(f"{base.green}Account number: {base.white}{no+1}/{num_acc}")

                try:
                    cookie = get_cookie(data=data)

                    molecule = get_info(cookie=cookie)

                    process_tap(cookie=cookie, molecule=molecule)

                except Exception as e:
                    base.log(f"{base.red}Error: {base.white}{e}")

            print()
            wait_time = 5 * 60
            base.log(f"{base.yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        coin = xKuCoin()
        coin.main()
    except KeyboardInterrupt:
        sys.exit()
