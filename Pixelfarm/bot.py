import sys

sys.dont_write_bytecode = True

from package import base
from package.core.token import get_token
from package.core.garden import info, extract_garden_info, process_claim
from package.core.task import process_task

import time
import brotli


class PixelFarm:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = base.create_banner(game_name="Pixel Farm")

        # # Get config
        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

    def main(self):
        while True:
            base.clear_terminal()
            print(self.banner)
            data = open(self.data_file, "r").read().splitlines()
            num_acc = len(data)
            base.log(self.line)
            base.log(f"{base.green}Numer of accounts: {base.white}{num_acc}")

            for no, data in enumerate(data):
                base.log(self.line)
                base.log(f"{base.green}Account number: {base.white}{no+1}/{num_acc}")

                try:
                    # Get token
                    token = get_token(query_id=data)

                    # User info
                    user_info = info(token=token)
                    tele_id = user_info["data"]["telegram_id"]
                    extract_garden_info(user_info=user_info)

                    # Task
                    if self.auto_do_task:
                        base.log(f"{base.yellow}Auto Do Task: {base.green}ON")
                        process_task(tele_id=tele_id, token=token)
                    else:
                        base.log(f"{base.yellow}Auto Do Task: {base.red}OFF")

                    # Claim
                    base.log(f"{base.yellow}Trying to claim...")
                    process_claim(token=token)
                except Exception as e:
                    base.log(f"{base.red}Error: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        pixelfarm = PixelFarm()
        pixelfarm.main()
    except KeyboardInterrupt:
        sys.exit()
