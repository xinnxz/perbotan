import http.client
import json
import time
import threading
import asyncio
import random
from concurrent.futures import ThreadPoolExecutor

# Function to send a request
def send_request(token):
    conn = http.client.HTTPSConnection("api.bfdcoin.org")
    payload = json.dumps({
        "boxType": 1,
        "coinCount": 210
    })
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://bfdcoin.org',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://bfdcoin.org/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    conn.request("POST", "/api?act=collectSpecialBoxCoin", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    if data["code"] == 0 and data["message"] == "Success":
        collect_amount = data["data"]["collectAmount"]
        print(f"Collect amount: {collect_amount}")
    else:
        print("Failed to collect coins")

# Function to get account info
def get_account_info(token, max_workers):
    conn = http.client.HTTPSConnection("api.bfdcoin.org")
    headers = {
        'Content-Type': 'application/json',
        'Token': token,
        'User-Agent': 'Mozilla/5.0'
    }
    conn.request("POST", "/api?act=accountInfo", headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    account_info = data.get('data', {})
    user_level = account_info.get('userLevel')
    total_amount = account_info.get('totalAmount')
    current_amount = account_info.get('currentAmount')

    def format_amount(amount):
        formatted = f"{amount:,}".replace(",", ".")
        if amount >= 1_000_000_000:
            return f"{formatted} ({amount // 1_000_000_000:.1f}B)"
        elif amount >= 1_000_000:
            return f"{formatted} ({amount // 1_000_000:.1f}M)"
        else:
            return formatted

    print(
        f'Account Info {token}\n'
        f'  User Level    : {user_level}\n'
        f'  Tmount        : {format_amount(total_amount)}\n'
        f'  Cmount        : {format_amount(current_amount)}\n'
        f'  Max Workers   : {max_workers}'
    )

# Asynchronous function to run the requests
async def run_requests(executor, token, max_workers):
    loop = asyncio.get_event_loop()
    get_account_info(token, max_workers)
    tasks = [loop.run_in_executor(executor, send_request, token) for _ in range(100)]
    await asyncio.gather(*tasks)

# Function for 1-hour countdown with moving display
def countdown_one_hour():
    total_seconds = 1800
    while total_seconds:
        mins, secs = divmod(total_seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(f'\rCountdown: {timer}', end='')
        time.sleep(1)
        total_seconds -= 1
    print('\nCountdown finished. Restarting process...')

# Main function to set up threading and asyncio
def main():
    with open('data.txt', 'r') as file:
        tokens = [line.strip() for line in file.readlines()]

    for i, token in enumerate(tokens):
        max_workers = random.randint(80, 120)
        print(f"Processing account {i + 1} of {len(tokens)} with {max_workers} workers.")
        executor = ThreadPoolExecutor(max_workers=max_workers)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_requests(executor, token, max_workers))
        print(f"Finished processing account {i + 1} of {len(tokens)}")
        time.sleep(5)  # 5-second delay between accounts
    
    print("All accounts processed. Starting 30-min countdown.")
    countdown_one_hour()
    main()

if __name__ == "__main__":
    main()
