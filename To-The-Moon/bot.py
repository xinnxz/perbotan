import requests
import json
import time
from colorama import Fore, Style, init
from datetime import datetime, timedelta

init(autoreset=True)

def read_init_data():
    try:
        with open('data.txt', 'r') as file:
            init_data_list = file.read().strip().split('\n')
        return init_data_list
    except Exception as e:
        print(Fore.RED + "Error saat membaca data dari file")
        print(Fore.RED + "==================================")
        return []

def login(init_data):
    url = "https://moon.popp.club/pass/login"
    
    try:
        query_id = init_data.split('&user=')[0].split('=')[1]
        user_data = init_data.split('&user=')[1].split('&')[0]
        auth_date = init_data.split('&auth_date=')[1].split('&')[0]
        hash_value = init_data.split('&hash=')[1]
        
        try:
            user = json.loads(requests.utils.unquote(user_data))
        except json.JSONDecodeError as e:
            print(Fore.RED + "Error decoding JSON dari data pengguna")
            return None, None, False
        
        payload = {
            "initData": init_data,
            "initDataUnSafe": {
                "query_id": query_id,
                "user": user,
                "auth_date": auth_date,
                "hash": hash_value
            }
        }
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        
        if response.ok and 'data' in result and 'token' in result['data']:
            token = result['data']['token']
            cookies = response.cookies
            
            sign_in_status = result['data'].get('data', {}).get('signIn', 1)
            if sign_in_status == 0:
                checkin_successful = checkin_daily(token, cookies)
                if checkin_successful:
                    sign_in_count = result['data'].get('data', {}).get('signInCount', 0) + 1
                    print(Fore.GREEN + f"Daily check-in successful. Total check-ins: {sign_in_count}")
                else:
                    print(Fore.RED + "Daily check-in failed.")
            return token, cookies, True
        else:
            print(Fore.RED + "Login gagal")
            print(Fore.RED + "===========")
            return None, None, False

    except requests.RequestException as e:
        print(Fore.RED + "Error saat melakukan login")
        print(Fore.RED + "==========================")
        return None, None, False

def checkin_daily(token, cookies):
    url = "https://moon.popp.club/moon/sign/in"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(url, headers=headers, cookies=cookies)
        result = response.json()
        
        if result.get("code") == "200" and result.get("msg") == "success":
            print(Fore.GREEN + "Daily check-in successful")
            return True
        else:
            print(Fore.RED + "Daily check-in failed: " + result.get("msg", "Unknown error"))
            return False
    except requests.RequestException as e:
        print(Fore.RED + "Error saat melakukan check-in harian")
        return False

def claim_sd_from_ref(token, cookies):
    url = "https://moon.popp.club/moon/claim/invite"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        result = response.json()
        
        if result.get("code") == "00":
            print(Fore.GREEN + "Claim SD Dari Reff sukses")
            return True
        else:
            print(Fore.RED + "Claim SD Dari Reff gagal")
            return False
    except requests.RequestException as e:
        print(Fore.RED + "Error saat melakukan claim SD dari reff")
        return False

def farming(token, cookies):
    url = "https://moon.popp.club/moon/farming"
    headers = {
        "Authorization": token
    }
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        result = response.json()
        
        if result.get("code") == "200":
            print(Fore.GREEN + "Farming sukses " + Fore.GREEN + "😊")
            print(Fore.GREEN + "--------------")
            return True
        else:
            print(Fore.YELLOW + "Farming cooldown " + Fore.YELLOW + "⏳")
            print(Fore.YELLOW + "----------------")
            return False
    except requests.RequestException as e:
        print(Fore.RED + "Error saat melakukan farming")
        return False

def claim_farming(token, cookies):
    url = "https://moon.popp.club/moon/claim/farming"
    headers = {
        "Authorization": token
    }
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        result = response.json()
        
        if result.get("code") == "200":
            return True
        else:
            return False
    except requests.RequestException as e:
        print(Fore.RED + "Error saat melakukan claim farming")
        return False

def explorer(token, cookies, planet_id):
    url = f"https://moon.popp.club/moon/explorer?plantId={planet_id}"
    headers = {
        "Authorization": token
    }
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        result = response.json()
        
        if response.ok and result.get("code") == "00" and "data" in result:
            amount = result["data"]["amount"]
            award = result["data"]["award"]
            print(Fore.GREEN + f"Reward: {amount} {award}")
            print(Fore.GREEN + "--------------------")
            return True
        else:
            print(Fore.YELLOW + "Explorer cooldown " + Fore.YELLOW + "⏳")
            print(Fore.YELLOW + "===================")
            return False
    except requests.RequestException as e:
        print(Fore.RED + "Error saat melakukan explorer")
        return False

def get_planets(token, cookies):
    url = "https://moon.popp.club/moon/planets"
    headers = {
        "Authorization": token
    }
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        result = response.json()
        
        if result.get("code") == "200" and result.get("data"):
            planets = result["data"]
            planet_count = len(planets)
            print(Fore.GREEN + f"Jumlah Planet: {planet_count}")
            print(Fore.GREEN + "===================")
            
            return planets
        else:
            print(Fore.YELLOW + "Tidak ada planet " + Fore.YELLOW + "⏳")
            print(Fore.YELLOW + "----------------")
            return []
    except requests.RequestException as e:
        print(Fore.RED + "Error saat mendapatkan planet")
        return []

def info_assets(token, cookies):
    url = "https://moon.popp.club/moon/asset"
    headers = {
        "Authorization": token
    }
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        result = response.json()
        
        if response.ok and result.get("code") == "200" and "data" in result:
            data = result["data"]
            print(Fore.GREEN + f"Tickets: {data.get('probe', 0)}")
            print(Fore.GREEN + "--------------------")
            return data
        else:
            print(Fore.YELLOW + "InfoAssets cooldown " + Fore.YELLOW + "⏳")
            print(Fore.YELLOW + "====================")
            return None
    except requests.RequestException as e:
        print(Fore.RED + "Error saat mendapatkan info assets")
        return None

def info_assets2(token, cookies):
    url = "https://moon.popp.club/moon/asset"
    headers = {
        "Authorization": token
    }
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        result = response.json()
        
        if response.ok and result.get("code") == "200" and "data" in result:
            data = result["data"]
            print(Fore.GREEN + f"SD: {data.get('sd', 0)}")
            print(Fore.GREEN + f"ETH: {data.get('eth', 0)}")
            print(Fore.GREEN + f"bitLayerBox: {data.get('blb', 0)}")
            print(Fore.GREEN + "--------------------")
            return data
        else:
            print(Fore.YELLOW + "InfoAssets cooldown " + Fore.YELLOW + "⏳")
            print(Fore.YELLOW + "====================")
            return None
    except requests.RequestException as e:
        print(Fore.RED + "Error saat mendapatkan info assets")
        return None

def countdown_timer(seconds):
    while seconds > 0:
        minutes, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(minutes, secs)
        print(Fore.CYAN + f"Tunggu {timeformat} sebelum menjalankan kembali ", end='\r')
        time.sleep(1)
        seconds -= 1

def main():
    print(Fore.CYAN + "="*30)
    print(Fore.CYAN + " BOT To The Moon MULTI AKUN ")
    print(Fore.CYAN + "="*30)
    print(Fore.CYAN + " BOT FROM AirDropFamilyIDN")
    print(Fore.CYAN + "="*30)
    init_data_list = read_init_data()
    
    if not init_data_list:
        print(Fore.RED + "Daftar akun kosong.")
        return
    
    while True: 
        for idx, init_data in enumerate(init_data_list):
            print(Fore.MAGENTA + f"\nMencoba login Akun {idx + 1}")
            print(Fore.MAGENTA + "="*24 + "\n")
            token, cookies, login_successful = login(init_data)
            if not login_successful:
                print(Fore.RED + "Login gagal, mencoba akun berikutnya...")
                continue
            
            print(Fore.GREEN + "Login berhasil.")
            print(Fore.GREEN + "==============")
            
            assets_info = info_assets(token, cookies) 
            if assets_info is None:
                print(Fore.RED + "Gagal mendapatkan informasi assets.")
                continue
            
            tickets = assets_info.get('probe', 0)
            
            farming_done = farming(token, cookies)
            time.sleep(3)
            
            planets = get_planets(token, cookies)
            time.sleep(3)

            if planets and tickets == 0:
                print(Fore.YELLOW + "Ticket tidak mencukupi")
            else:
                for planet in planets:
                    planet_id = planet.get("id")
                    if planet_id:
                        explorer(token, cookies, planet_id)
                        time.sleep(3)  

            claim_done = claim_farming(token, cookies)
            time.sleep(3)
            
            info_sd_eth = info_assets2(token, cookies) 
            time.sleep(3)

            claim_sd_successful = claim_sd_from_ref(token, cookies)
            time.sleep(3)
            
            if not (farming_done or planets or claim_done or info_sd_eth or claim_sd_successful):
                print(Fore.YELLOW + "Semua clear. Beralih ke akun berikutnya.")
                print(Fore.YELLOW + "========================================")
                continue
            
            print(Fore.GREEN + f"Selesai dengan akun {idx + 1}, mencoba akun berikutnya")
            print(Fore.GREEN + "==================================================")
        
        print(Fore.CYAN + "Semua akun sudah diproses")
        print(Fore.CYAN + "=========================\n")
        
        countdown_timer(300)  

if __name__ == "__main__":
    main()
