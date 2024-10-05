import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.info import get_info
from core.task import process_do_task, process_do_wheel_task
from core.spin import process_spin_wheel

import time


class Agent:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = base.create_banner(game_name="Agent 301")

        # Get config
        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_do_wheel_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-wheel-task"
        )

        self.auto_spin_wheel = base.get_config(
            config_file=self.config_file, config_name="auto-spin-wheel"
        )

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
                    get_info(data=data)

                    # Do task
                    if self.auto_do_task:
                        base.log(f"{base.yellow}Auto Do Task: {base.green}ON")
                        process_do_task(data=data)
                    else:
                        base.log(f"{base.yellow}Auto Do Task: {base.red}OFF")

                    # Wheel task
                    if self.auto_do_wheel_task:
                        base.log(f"{base.yellow}Auto Do Wheel Task: {base.green}ON")
                        process_do_wheel_task(data=data)
                    else:
                        base.log(f"{base.yellow}Auto Do Wheel Task: {base.red}OFF")

                    # Spin wheel
                    if self.auto_spin_wheel:
                        base.log(f"{base.yellow}Auto Spin Wheel: {base.green}ON")
                        process_spin_wheel(data=data)
                    else:
                        base.log(f"{base.yellow}Auto Spin Wheel: {base.red}OFF")

                except Exception as e:
                    base.log(f"{base.red}Error: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        agent = Agent()
        agent.main()
    except KeyboardInterrupt:
        sys.exit()
