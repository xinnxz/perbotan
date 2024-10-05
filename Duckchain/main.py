import sys

from src.core import main
from src.deeplchain import _banner, _clear, log,hju,pth,mrh

if __name__ == "__main__":
    _clear()
    _banner()
    log(hju + f"Please wait, starting your bot...")
    log(pth + "~" * 38)
    while True:
        try:
            main()
        except KeyboardInterrupt:
            log(mrh + f"Successfully logged out of the bot\n")
            sys.exit()
