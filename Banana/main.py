import sys
import json
from colorama import *
from src.core import Banana, config
from requests.exceptions import RequestException
from src.deeplchain import log,log_error, countdown_timer, mrh, htm, bru, kng, pth, hju, _banner, _clear, load_config

init(autoreset=True)
config = load_config()

def process_token(banana, token, current_index, total_accounts): 
    try:
        use_proxy = config.get('use_proxy', False)
        user_info = banana.get_user_info(token)
        data = user_info['data']
        if isinstance(data, str): 
            data = json.loads(data)
        
        if use_proxy and banana.proxies:
            proxy = banana.get_current_proxy()
            if proxy:
                proxy_url = proxy.get('http', '')
                if '@' in proxy_url: 
                    host_port = proxy_url.split('@')[-1] 
                else:
                    host_port = proxy_url.split('//')[-1] 
            else:
                host_port = 'No proxy'
        else:
            host_port = 'No proxy' 
        
        username = data.get('username', 'Unknown')
        total_usdt = data.get('usdt', 0)
        total_peel = data.get('peel', 0)
        click_count = data.get('max_click_count', 0)
        speedup_count = data.get('speedup_count', 0)
        total_banana = data.get('banana_count', 0)
        
        log(hju + f"Account: {pth}{current_index}/{total_accounts}")
        log(hju + f"Using proxy: {pth}{host_port}") 
        log(htm + "~" * 38)
        
        if use_proxy and banana.proxies:
            banana.proxy_index = (banana.proxy_index + 1) % len(banana.proxies)

        log(bru + f"Logged in as {pth}{username}")
        log(hju + f"Balance: {pth}{total_peel} {kng}PEEL {hju}| {pth}{total_usdt} {hju}USDT")
        log(hju + f"Click limit: {pth}{click_count} {hju}| BaBoost: {pth}{speedup_count}") 
        log(hju + f"You have a total {pth}{total_banana} {kng}Banana")

        banana.get_lottery(token)
        banana.banana_list(token)
        banana.do_speedup(token)

        log(htm + "~" * 38)
        countdown_timer(config["delay_account"])
    except RequestException as e:
        log(mrh + f"Something wrong please check {hju}last.log {mrh}file!")
        log_error(f"{str(e)}")

def load_tokens():
    try:
        with open('tokens.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_tokens(tokens):
    with open('tokens.json', 'w') as file:
        json.dump(tokens, file, indent=4)

def main():
    _clear()
    _banner()
    banana = Banana()
    remaining_times = []

    try:
        with open('query.txt', 'r') as file:
            queries = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        log(mrh + "No query.txt file found.")
        return

    total_accounts = len(queries)
    tokens = load_tokens()

    for current_index, query in enumerate(queries):
        user_id = banana.extract_user_id(query)
        existing_token = tokens.get(user_id, [])

        if existing_token:
            token_to_use = existing_token[0]
        else:
            new_token = banana.login(query)
            if new_token:
                if user_id in tokens:
                    tokens[user_id].append(new_token)
                else:
                    tokens[user_id] = [new_token]
                save_tokens(tokens)
                token_to_use = new_token
            else:
                log(f"Failed to get token for user ID {user_id}")
                continue

        process_token(banana, token_to_use, current_index + 1, total_accounts)
        remaining_time = banana.get_lottery(token_to_use, silent=True)
        if remaining_time > 0:
            remaining_times.append(remaining_time)

    if remaining_times:
        shortest_time = min(remaining_times)
        countdown_timer(shortest_time)  
    else:
        countdown_timer(3800)

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            log(mrh + f"Something wrong please check {hju}last.log {mrh}file!")
            log_error(f"{str(e)}")
            log(f"{pth}~" * 38)
            countdown_timer(5)
        except KeyboardInterrupt:
            log(mrh + "Progress terminated by user")
            sys.exit(0)