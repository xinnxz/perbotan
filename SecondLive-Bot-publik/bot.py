import requests
import json
import time
import os


class Color:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

last_claim_time = 0

def login_telegram(telegram_data):
    url = "https://app.secondlive.world/api/user/telegram-login"
    
    headers = {
        "Authorization": "Bearer ", 
        "Content-Type": "application/json"
    }

    payload = {
        "invite_code": "",  
        "telegram_data": telegram_data,
        "username": "",  
        "photo_url": ""
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        if response_data["code"] == 0:
            print(Color.OKGREEN + "Login berhasil!" + Color.ENDC)
            user_id = response_data["data"]["user_id"]
            access_token = response_data["data"]["access_token"]
            print(Color.OKBLUE + "User ID: " + str(user_id) + Color.ENDC)
            return access_token  
        else:
            print(Color.FAIL + "Login gagal: " + response_data["message"] + Color.ENDC)
    else:
        print(Color.FAIL + "Terjadi kesalahan saat melakukan permintaan. Status kode: " + str(response.status_code) + Color.ENDC)

def get_user_info(access_token):
    url = "https://app.secondlive.world/api/user/info"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data["code"] == 0:
            user_info = response_data["data"]
            print(Color.OKBLUE + "User Name: " + user_info["user_name"] + Color.ENDC)
        else:
            print(Color.FAIL + "Gagal mengambil informasi pengguna: " + response_data["message"] + Color.ENDC)
    else:
        print(Color.FAIL + "Terjadi kesalahan saat mengambil informasi pengguna. Status kode: " + str(response.status_code) + Color.ENDC)

def checkin(access_token):
    url = "https://app.secondlive.world/api/user/checkin"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data["code"] == 0:
            print(Color.OKGREEN + "Check-in berhasil!" + Color.ENDC)
        else:
            print(Color.FAIL + "Gagal check-in: " + response_data["message"] + Color.ENDC)
    else:
        print(Color.FAIL + "Terjadi kesalahan saat melakukan check-in. Status kode: " + str(response.status_code) + Color.ENDC)

def claim_crush(access_token):
    global last_claim_time
    current_time = time.time()

    if current_time - last_claim_time < 3600:
        remaining_time = 3600 - (current_time - last_claim_time)
        minutes, seconds = divmod(remaining_time, 60)
        print(Color.WARNING + f"Claim setelah {int(minutes)} menit {int(seconds)} detik." + Color.ENDC)
        return

    url = "https://app.secondlive.world/api/user/figure/claim"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "is_claim_double": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        if response_data["code"] == 0:
            print(Color.OKGREEN + "Claim berhasil!" + Color.ENDC)
            last_claim_time = current_time
            
            claim_data = response_data["data"]
            print(Color.OKBLUE + "Claim Intimacy: " + str(claim_data["claim_intimacy"]) + Color.ENDC)
            print(Color.OKBLUE + "Space Level: " + str(claim_data["space_level"]) + Color.ENDC)
            print(Color.OKBLUE + "Food Level: " + str(claim_data["food_level"]) + Color.ENDC)
            print(Color.OKBLUE + "Storage Level: " + str(claim_data["storage_level"]) + Color.ENDC)
            print(Color.OKBLUE + "Intimacy Balance: " + str(claim_data["intimacy_balance"]) + Color.ENDC)
            print(Color.OKBLUE + "USDT Balance: " + str(claim_data["usdt_balance"]) + Color.ENDC)
            print(Color.OKBLUE + "Ranking: " + str(claim_data["ranking"]) + Color.ENDC)
            print(Color.OKBLUE + "Has Claimed: " + str(claim_data["has_claimed"]) + Color.ENDC)
            
            level_info = claim_data.get("level_info", {})
            print(Color.OKBLUE + "Current Food Speed: " + str(level_info.get("current_food_speed", "N/A")) + Color.ENDC)
            print(Color.OKBLUE + "Next Food Speed: " + str(level_info.get("next_food_speed", "N/A")) + Color.ENDC)
        else:
            print(Color.FAIL + "Gagal melakukan klaim: " + response_data["message"] + Color.ENDC)
    else:
        print(Color.FAIL + "Terjadi kesalahan saat melakukan klaim. Status kode: " + str(response.status_code) + Color.ENDC)

def claim_tasks(access_token):
    url = "https://app.secondlive.world/api/user-task/list"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data["code"] == 0:
            tasks = response_data["data"]
            completed_tasks = []
            uncompleted_tasks = []

            if "basic" in tasks:
                for task_name, task_info in tasks["basic"].items():
                    if task_info["task_status"] == "Completed":
                        completed_tasks.append(task_name)
                    else:
                        uncompleted_tasks.append(task_name)

            if "daily" in tasks:
                for task_name, task_info in tasks["daily"].items():
                    if task_info["task_status"] == "Completed":
                        completed_tasks.append(task_name)
                    else:
                        uncompleted_tasks.append(task_name)

            print(Color.OKGREEN + "Tugas yang sudah dikerjakan:" + Color.ENDC)
            for name in completed_tasks:
                print(f"- {name}")

            print(Color.WARNING + "\nTugas yang belum dikerjakan:" + Color.ENDC)
            for name in uncompleted_tasks:
                print(f"- {name}")

        else:
            print(Color.FAIL + "Gagal mengambil daftar tugas: " + response_data["message"] + Color.ENDC)
    else:
        print(Color.FAIL + "Terjadi kesalahan saat mengambil daftar tugas. Status kode: " + str(response.status_code) + Color.ENDC)

def print_welcome_message():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Color.OKBLUE + "-" * 40 + Color.ENDC)
    print(Color.OKGREEN + "Bot free From AirdropfamilyIDN" + Color.ENDC)
    print(Color.OKGREEN + "Ga di Encrypt Biar kalau mau maling Gampang" + Color.ENDC)
    print(Color.OKBLUE + "-" * 40 + Color.ENDC)  

def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        minutes, secs = divmod(remaining, 60)
        timer = f"{minutes:02}:{secs:02}"
        print(f"\r{Color.WARNING}Menunggu 30 menit sebelum mengulang... {timer}{Color.ENDC}", end="")
        time.sleep(1)
    print() 

def main():
    print_welcome_message()
    
    with open('data.txt', 'r') as file:
        accounts = file.readlines()

    while True: 
        for account in accounts:
            account = account.strip()
            
            print(f" ")
            access_token = login_telegram(account)
            
            if access_token:
                get_user_info(access_token) 
                checkin(access_token)  
                claim_crush(access_token) 
                claim_tasks(access_token)  

        print(Color.OKGREEN + "\nSemua Akun Telah di proses" + Color.ENDC)
        countdown_timer(30 * 60)  

if __name__ == "__main__":
    main()
