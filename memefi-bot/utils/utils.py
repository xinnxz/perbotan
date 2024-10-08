import json
import time
import base64
import random
import http.client
from colorama import *
from urllib.parse import unquote
from utils.headers import headers_set
from utils.helpers import log,mrh,hju,kng,pth,bru,htm, reset, generate_random_nonce, _number, read_config
from utils.queries import QUERY_BOOSTER, QUERY_GAME_CONFIG, QUERY_USER, QUERY_NEXT_BOSS, MUTATION_GAME_PROCESS_TAPS_BATCH, QUERY_COMBO
        
config = read_config()
proxy_file = ('proxy.txt')
query_file = ('query_id.txt')
url = "https://api-gw-tg.memefi.club/graphql"

def load_proxies():
    with open(proxy_file, 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    return proxies

proxies = load_proxies()

def safe_post(url, headers, json_payload):
    retries = 5
    timeout = 5 
    for attempt in range(retries):
        try:
            if proxies:
                proxy = random.choice(proxies)
                if '@' in proxy:
                    user_pass, proxy_ip = proxy.split('@')
                    proxy_auth = base64.b64encode(user_pass.encode()).decode()
                else:
                    proxy_ip = proxy
                    proxy_auth = None

                conn = http.client.HTTPSConnection(proxy_ip, timeout=timeout)
                if proxy_auth:
                    conn.set_tunnel(url, 443, headers={"Proxy-Authorization": f"Basic {proxy_auth}"})
                else:
                    conn.set_tunnel(url, 443)
            else:
                conn = http.client.HTTPSConnection(url, timeout=timeout)
            
            payload = json.dumps(json_payload)
            conn.request("POST", "/graphql", payload, headers)
            res = conn.getresponse()
            response_data = res.read().decode("utf-8")
            if res.status == 200:
                return json.loads(response_data) 
            else:
                log(mrh + f"Failed with status {pth}{res.status}, {hju}retrying ")
        except (http.client.HTTPException, TimeoutError) as e:
            log(mrh + f"Error: {pth}{e}, {hju}retrying ")
        if attempt < retries - 1:
            time.sleep(10)
        else:
            log(mrh + f"Failed after several attempt , {hju}reseting bot")
            return None
    return None

def fetch(account_line):
    with open(query_file, 'r') as file:
        raw_data = file.readlines()[account_line - 1].strip()

    tg_web_data = unquote(unquote(raw_data))
    params = dict(param.split('=') for param in tg_web_data.split('&'))

    user_data = json.loads(unquote(params['user']))
    query_id = params['query_id']
    auth_date = int(params['auth_date'])
    hash_ = params['hash']

    url = 'api-gw-tg.memefi.club'
    headers = headers_set.copy()

    data = {
        "operationName": "MutationTelegramUserLogin",
        "variables": {
            "webAppData": {
                "auth_date": auth_date,
                "hash": hash_,
                "query_id": query_id,
                "checkDataString": f"auth_date={auth_date}\nquery_id={query_id}\nuser={unquote(params['user'])}",
                "user": {
                    "id": user_data["id"],
                    "allows_write_to_pm": user_data.get("allows_write_to_pm", False),
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "username": user_data.get("username", "Please set username"),
                    "language_code": user_data["language_code"],
                    "version": "7.2",
                    "platform": "ios",
                    "is_premium": user_data.get("is_premium", False)
                }
            }
        },
        "query": """
        mutation MutationTelegramUserLogin($webAppData: TelegramWebAppDataInput!) {
            telegramUserLogin(webAppData: $webAppData) {
                access_token
                __typename
            }
        }
        """
    }

    conn = http.client.HTTPSConnection(url)
    payload = json.dumps(data)
    conn.request("POST", "/graphql", payload, headers)
    res = conn.getresponse()
    response_data = res.read().decode("utf-8")
    
    if res.status == 200:
        try:
            json_response = json.loads(response_data)
            if 'errors' in json_response:
                print(mrh + "Errors encountered during login.")
                return None
            return json_response['data']['telegramUserLogin']['access_token']
        except json.JSONDecodeError:
            print(mrh + "Failed to decode JSON response.")
            return None
    else:
        print(mrh + f"Failed to login, status code: {res.status}")
        return None

def cek_user(index):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"

    headers = headers_set.copy()
    headers['Authorization'] = f'Bearer {access_token}'

    json_payload = {
        "operationName": "QueryTelegramUserMe",
        "variables": {},
        "query": QUERY_USER
    }

    response = safe_post(url, headers, json_payload)
    if response and 'errors' not in response:
        user_data = response['data']['telegramUserMe']
        return user_data 
    else:
        print(mrh + f"Failed with response {response}")
        return None 

def activate_energy_recharge_booster(index, headers):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"

    headers = headers_set.copy() 
    headers['Authorization'] = f'Bearer {access_token}'

    recharge_booster_payload = {
        "operationName": "telegramGameActivateBooster",
        "variables": {"boosterType": "Recharge"},
        "query": QUERY_BOOSTER
    }

    response = safe_post(url, headers, recharge_booster_payload)
    if response and 'data' in response and response['data'] and 'telegramGameActivateBooster' in response['data']:
        new_energy = response['data']['telegramGameActivateBooster']['currentEnergy']
        log(hju + f"succesfully charged {pth}{new_energy} {kng}energy ")
        time.sleep(1)
    else:
        log(f"{mrh}recharge Booster incomplete or missing data.{reset}")

def exponential_backoff(attempt, base_delay=1.0, factor=2.0, max_delay=30.0):
    delay = min(base_delay * (factor ** attempt), max_delay)
    time.sleep(delay)

def activate_booster(index, headers):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"
    log(hju + "Activating turbo boost, please wait!")

    headers = headers_set.copy()
    headers['Authorization'] = f'Bearer {access_token}'

    recharge_booster_payload = {
        "operationName": "telegramGameActivateBooster",
        "variables": {"boosterType": "Turbo"},
        "query": QUERY_BOOSTER
    }

    response = safe_post(url, headers, recharge_booster_payload)
    if not response or 'data' not in response:
        log(f"{mrh}Failed to activate booster, no data received.{reset}")
        return

    booster_data = response['data']['telegramGameActivateBooster']
    current_health = booster_data['currentBoss']['currentHealth']
    current_level = booster_data['currentBoss']['level']

    if current_health == 0:
        log(pth + f"Boss has been defeated, setting up the next boss")
        set_next_boss(index, headers)
        return

    min_damage = config.get('min_damage', 1000) 
    max_damage = config.get('max_damage', 10000)
    damage = config.get('crazy_damage', False)
    
    if damage == True:
        total_hit = random.randint(min_damage, max_damage)
    else:
        total_hit = random.randint(10000, 20000)

    tap_payload = {
        "operationName": "MutationGameProcessTapsBatch",
        "variables": {
            "payload": {
                "nonce": generate_random_nonce(),
                "tapsCount": total_hit
            }
        },
        "query": MUTATION_GAME_PROCESS_TAPS_BATCH
    }
    attempt_hit = config.get('attempt_hit_boss',5)
    for attempt in range(attempt_hit):
        stat_result = cek_stat(index, headers)
        if not stat_result:
            log(f"{mrh}Failed to retrieve stats on attempt {attempt + 1}.{reset}")
            continue

        bos_health = stat_result['currentBoss']['currentHealth']
        tap_result = submit_taps(index, tap_payload)
        if not tap_result or 'data' not in tap_result:
            log(f"{mrh}Failed with proud status None on attempt {attempt + 1}.{reset}")
            continue

        tap_data = tap_result['data']['telegramGameProcessTapsBatch']
        boss_level = tap_data['currentBoss']['level']
        balance = tap_data['coinsAmount']
        log(kng + f"Fighting {hju}with the boss on {pth}level {boss_level}")
        if bos_health == 0 :
            set_next_boss(index, headers)
            continue
        elif bos_health <= current_health:
            log(bru + f"Success ! {hju}balance {pth}{_number(balance)} {hju}coins")
            log(hju + f"Current health {mrh}{_number(tap_data['currentBoss']['currentHealth'])} {hju}remaining")
        elif balance == balance or bos_health == current_health:
            log(mrh + f"Failed {pth}{attempt + 1} {mrh}to fight the boss")
        else:
            log(mrh + f"Failed {pth}{attempt + 1} {mrh}to defeat the boss")

def submit_taps(index, json_payload):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"

    headers = headers_set.copy()
    headers['Authorization'] = f'Bearer {access_token}'

    response = safe_post(url, headers, json_payload)
    if response:
        return response 
    else:
        log(f"failed with {response}, try again")
        return None 

def set_next_boss(index, headers):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"

    headers = headers_set.copy()
    headers['Authorization'] = f'Bearer {access_token}'
    boss_payload = {
        "operationName": "telegramGameSetNextBoss",
        "variables": {},
        "query": QUERY_NEXT_BOSS
    }

    response = safe_post(url, headers, boss_payload)
    if response and 'data' in response:
        log(hju + f"Try to {pth}find {hju}or {pth}awaken {hju}the boss",flush=True)
    else:
        log(mrh + f"Failed to find a {kng}new boss.", flush=True)

def cek_stat(index, headers):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"

    headers = headers_set.copy()
    headers['Authorization'] = f'Bearer {access_token}'

    json_payload = {
        "operationName": "QUERY_GAME_CONFIG",
        "variables": {},
        "query": QUERY_GAME_CONFIG
    }

    response = safe_post(url, headers, json_payload)
    if response and 'errors' not in response:
        user_data = response['data']['telegramGameGetConfig']
        return user_data
    else:
        log(response)
        log(f"failed with {response.status}, try again...")
        return None 
    
def claim_combo(index, headers):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"
    headers = headers_set.copy()  
    headers['Authorization'] = f'Bearer {access_token}'

    nonce = generate_random_nonce()
    taps_count = random.randint(5, 10)

    with open('combo.txt', 'r') as file:
        vector = file.readline().strip()
        
    claim_combo_payload = {
        "operationName": "MutationGameProcessTapsBatch",
        "variables": {
            "payload": {
                "nonce": nonce,
                "tapsCount": taps_count,
                "vector": vector
            }
        },
        "query": QUERY_COMBO
    }

    response = safe_post(url, headers, claim_combo_payload)
    if response and 'data' in response and 'telegramGameProcessTapsBatch' in response['data']:
        game_data = response['data']['telegramGameProcessTapsBatch']
        if game_data['tapsReward'] is None:
            log(kng + f"Combo has already been claimed before")
        else:
            log(hju + f"Succesfully claim combo {pth}+{kng}{_number(game_data['tapsReward'])}")
    else:
        log("Claim combo incomplete or missing data.")