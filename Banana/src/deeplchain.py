import os
import time
import json
from colorama import *
from datetime import datetime

mrh = Fore.LIGHTRED_EX
pth = Fore.LIGHTWHITE_EX
hju = Fore.LIGHTGREEN_EX
kng = Fore.LIGHTYELLOW_EX
bru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
htm = Fore.LIGHTBLACK_EX

last_log_message = None

def log(message, **kwargs):
    global last_log_message
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flush = kwargs.pop('flush', False)
    end = kwargs.pop('end', '\n')
    if message != last_log_message:
        print(f"{htm}[{current_time}] {message}", flush=flush, end=end)
        last_log_message = message

def log_error(message):
    with open('last.log', 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR - {message}\n")

def countdown_timer(seconds):
    while seconds > 0:
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        print(f"{pth}please wait until {h:02}:{m:02}:{s:02}", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print(" " * 40, flush=True, end="\r")
    
def _banner():
    banner = r"""
 ██╗████████╗███████╗     ██╗ █████╗ ██╗    ██╗
 ██║╚══██╔══╝██╔════╝     ██║██╔══██╗██║    ██║
 ██║   ██║   ███████╗     ██║███████║██║ █╗ ██║
 ██║   ██║   ╚════██║██   ██║██╔══██║██║███╗██║
 ██║   ██║   ███████║╚█████╔╝██║  ██║╚███╔███╔╝
 ╚═╝   ╚═╝   ╚══════╝ ╚════╝ ╚═╝  ╚═╝ ╚══╝╚══╝  """ 
    print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
    print(hju + f" Banana by Carv Bot")
    print(mrh + f" FREE TO USE = Join us on {pth}t.me/DEEPLCHAIN")
    print(mrh + f" before start please '{hju}git pull{mrh}' to update bot")
    print(f"{pth}~" * 60)

def load_config():
    with open('config.json') as f:
        return json.load(f)

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')