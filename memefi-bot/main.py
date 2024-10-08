import sys

from utils.core import main
from utils.helpers import print_banner, log, mrh

if __name__ == "__main__":
    while True:
        try:
            print_banner()
            main()
        except KeyboardInterrupt:
            print()
            log(mrh + f"Successfully logged out of the bot\n")
            sys.exit()
