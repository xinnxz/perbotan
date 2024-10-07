import requests
import json
import urllib.parse
import time
from datetime import datetime
import pytz
import sys

WIB = pytz.timezone('Asia/Jakarta')

def print_bright(text):
    print(f"\033[93m{text}\033[0m")

def get_wib_time():
    now = datetime.now(WIB)
    return now.strftime('%d/%m/%Y %H:%M:%S WIB')

def get_auth_token(query_data):
    AUTH_URL = "https://api.dormint.io/api/auth/telegram/verify"
    response = requests.get(AUTH_URL, params=query_data)
    if response.status_code == 200:
        return response.text.strip()
    else:
        print_bright(f"Gagal mendapatkan auth token. Status: {response.status_code}")
        return None

def save_tokens(token_data):
    with open('token.json', 'w') as token_file:
        json.dump(token_data, token_file, indent=4)

def load_query_strings():
    try:
        with open('query.txt', 'r') as query_file:
            queries = [line.strip() for line in query_file if line.strip()]
        return queries
    except FileNotFoundError:
        print_bright("File query.txt tidak ditemukan.")
        return []

def check_farming_status(auth_token):
    url = f"https://api.dormint.io/tg/farming/status"
    data = {"auth_token": auth_token}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        return {
            "farming_left": result.get('farming_left', 0),
            "farming_value": result.get('farming_value', 0.0),
            "sleepcoin_balance": result.get('sleepcoin_balance', 0.0),
            "farming_speed": result.get('farming_speed', 0.0)
        }
    else:
        print_bright(f"[{get_wib_time()}] Gagal memeriksa status farming (Kode: {response.status_code})")
        return None

def start_farming(auth_token):
    url = f"https://api.dormint.io/tg/farming/start"
    data = {"auth_token": auth_token}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print_bright(f"[{get_wib_time()}] Farming dimulai")
    else:
        print_bright(f"[{get_wib_time()}] Gagal memulai farming (Kode: {response.status_code})")

def get_quest_list(auth_token):
    url = f"https://api.dormint.io/tg/quests/list"
    data = {"auth_token": auth_token}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print_bright(f"[{get_wib_time()}] Gagal mendapatkan daftar quest (Kode: {response.status_code})")
        return None

def start_quest(auth_token, quest_id):
    url = f"https://api.dormint.io/tg/quests/start"
    data = {"auth_token": auth_token, "quest_id": quest_id}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("status") == "ok":
            print_bright(f"[{get_wib_time()}] Quest {quest_id} berhasil dijalankan.")
        else:
            print_bright(f"[{get_wib_time()}] Gagal menjalankan quest {quest_id}. Status: {result.get('status')}")
    else:
        print_bright(f"[{get_wib_time()}] Gagal memulai quest {quest_id} (Kode: {response.status_code})")

def check_quest_completion(auth_token, quest_id):
    quest_list = get_quest_list(auth_token)
    if quest_list:
        for quest in quest_list:
            if quest['quest_id'] == quest_id and quest['status'] == 'quest_completed':
                print_bright(f"[{get_wib_time()}] Quest {quest_id} berhasil diselesaikan.")
                return True
    return False

def auto_complete_quests(auth_token):
    quest_list = get_quest_list(auth_token)
    if quest_list:
        print_bright("\n[Quest Selesai]")
        for quest in quest_list:
            if quest['status'] == 'quest_completed':
                print_bright(f"- {quest['name']}")

        print_bright("\n[Quest yang Belum Selesai]")
        for quest in quest_list:
            if quest['status'] == 'quest_not_completed':
                print_bright(f"- Memulai quest: {quest['name']} (ID: {quest['quest_id']})")
                start_quest(auth_token, quest['quest_id'])

                for attempt in range(3):
                    if check_quest_completion(auth_token, quest['quest_id']):
                        print_bright(f"[{get_wib_time()}] Quest {quest['quest_id']} berhasil diselesaikan.")
                        break
                    print_bright(f"[{get_wib_time()}] Menunggu quest {quest['quest_id']} selesai... (Percobaan ke-{attempt + 1})")
                    time.sleep(5)
                else:
                    print_bright(f"[{get_wib_time()}] Quest {quest['quest_id']} gagal diselesaikan setelah 3 kali percobaan.")
    else:
        print_bright(f"[{get_wib_time()}] Tidak ada quest yang ditemukan.")

def auto_farming(auth_token):
    farming_status = check_farming_status(auth_token)
    if farming_status:
        farming_left = farming_status['farming_left']
        farming_value = farming_status['farming_value']
        farming_speed = farming_status['farming_speed']
        sleepcoin_balance = farming_status['sleepcoin_balance']

        print_bright(f"[{get_wib_time()}] Status Farming:")
        print_bright(f"   - Sisa Waktu: {farming_left} detik")
        print_bright(f"   - Balance Menunggu: {farming_value:.2f}")
        print_bright(f"   - Sleepcoin Balance: {sleepcoin_balance:.2f}")

        while farming_left > 0:
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(farming_left))
            farming_value += farming_speed
            sys.stdout.write(f"\r[{get_wib_time()}] Sisa Waktu: {formatted_time}, Balance Menunggu: {farming_value:.2f}")
            sys.stdout.flush()
            time.sleep(1)
            farming_left -= 1

        print_bright(f"\n[{get_wib_time()}] Farming selesai! Total koin yang bisa di-claim: {farming_value:.2f}")
        start_farming(auth_token)

def main():
    queries = load_query_strings()
    if not queries:
        return

    token_data = {}

    for idx, query_string in enumerate(queries, start=1):
        query_data = urllib.parse.parse_qs(query_string)
        auth_token = get_auth_token(query_data)
        username = f"akun_{idx}"

        if auth_token:
            token_data[username] = auth_token
            auto_complete_quests(auth_token)
            auto_farming(auth_token)
        else:
            print_bright(f"Gagal mendapatkan token untuk akun {username}")

if __name__ == "__main__":
    main()
