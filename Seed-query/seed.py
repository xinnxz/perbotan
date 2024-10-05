import requests

import time
from colorama import init, Fore, Style
import sys
import os
init(autoreset=True)
import requests



def print_welcome_message():
    print(r"""
      _______
    /        /|
   /        / |
  /________/  |
 |        |   |
 | BABI   |  /
 |        | /
 ---------
""")
    print(Fore.GREEN + Style.BRIGHT + "Seed BOT")
    print(Fore.GREEN + Style.BRIGHT + "ANJING BABI NGENTOT BANGSAT")
 

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# URL endpoint
url_claim = 'https://elb.seeddao.org/api/v1/seed/claim'
url_balance = 'https://elb.seeddao.org/api/v1/profile/balance'
url_checkin = 'https://elb.seeddao.org/api/v1/login-bonuses'
url_upgrade_storage = 'https://elb.seeddao.org/api/v1/seed/storage-size/upgrade'
url_upgrade_mining = 'https://elb.seeddao.org/api/v1/seed/mining-speed/upgrade'
url_upgrade_holy = 'https://elb.seeddao.org/api/v1/upgrades/holy-water'
url_get_profile = 'https://elb.seeddao.org/api/v1/profile'
# Headers yang diperlukan untuk request
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
    'content-length': '0',
    'dnt': '1',
    'origin': 'https://cf.seeddao.org',
    'priority': 'u=1, i',
    'referer': 'https://cf.seeddao.org/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'telegram-data': 'tokens',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def load_credentials():
    # Membaca token dari file dan mengembalikan daftar token
    try:
        with open('query.txt', 'r') as file:
            tokens = file.read().strip().split('\n')
        # print("Token berhasil dimuat.")
        return tokens
    except FileNotFoundError:
        print("File tokens.txt tidak ditemukan.")
        return [  ]
    except Exception as e:
        print("Terjadi kesalahan saat memuat token:", str(e))
        return [  ]

import datetime
import pytz

def check_worm():
    response = requests.get('https://elb.seeddao.org/api/v1/worms', headers=headers)
    if response.status_code == 200:
        worm_data = response.json().get('data', {})
        print(f"Online")  # Log the full response
        next_refresh = worm_data.get('next_worm')  # Corrected key
        is_caught = worm_data.get('is_caught', False)

        if next_refresh is not None:
            # Convert string time to datetime object
            next_refresh_dt = datetime.datetime.fromisoformat(next_refresh[:-1] + '+00:00')
            now_utc = datetime.datetime.now(pytz.utc)

            # Calculate time difference in seconds
            time_diff_seconds = (next_refresh_dt - now_utc).total_seconds()
            hours = int(time_diff_seconds // 3600)
            minutes = int((time_diff_seconds % 3600) // 60)

            print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Lanjutkan Setelah {hours} jam {minutes} menit - Status: {'Caught' if is_caught else 'Available'}")

            return worm_data
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: 'next_worm' key not found in response.")
            return None
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Tidak dapat memperoleh data.")
        return None

def catch_worm():
    worm_data = check_worm()
    if worm_data:
        print(f"Mencoba menangkap cacing ")
        if not worm_data['is_caught']:
            response = requests.post('https://elb.seeddao.org/api/v1/worms/catch', headers=headers)
            print(f"Kirim permintaan POST untuk menangkap worm, kode status: {response.status_code}")
            if response.status_code == 200:
                print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Berhasil ditangkap")
            elif response.status_code == 400:
                print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Enam ditangkap")
            elif response.status_code == 404:
                print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Berikut ini tidak ditemukan. Response: {response.json()}")
            else:
                print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Kesalahan lainnya. Status code: {response.status_code}. Response: {response.json()}")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Cacing telah ditangkap sebelumnya")
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Tidak ada informasi mengenai yang terakhir")


def get_profile():
    response = requests.get(url_get_profile, headers=headers)
    if response.status_code == 200:
        # Menguraikan response JSON
        profile_data = response.json()
        # Mengakses nama dari data
        name = profile_data['data']['name']
        print(f"{Fore.CYAN+Style.BRIGHT}============== [ Akun | {name} ] ==============")  # Mencetak nama

        # Mengakses bagian 'upgrades' dari data dan mengelompokkan berdasarkan tipe upgrade
        upgrades = {}
        for upgrade in profile_data['data']['upgrades']:
            upgrade_type = upgrade['upgrade_type']
            upgrade_level = upgrade['upgrade_level']
            if upgrade_type in upgrades:
                # Memperbarui level jika level yang baru lebih tinggi
                if upgrade_level > upgrades[upgrade_type]:
                    upgrades[upgrade_type] = upgrade_level
            else:
                upgrades[upgrade_type] = upgrade_level

        # Mencetak 'upgrade_level' dari setiap upgrade dengan level ditambah 1
        for upgrade_type, level in upgrades.items():
            print(f"{Fore.BLUE+Style.BRIGHT}[ {upgrade_type.capitalize()} Level ]: {level + 1}")
    else:
        print("Khong lay duoc du lieu, status code:", response.status_code)
        return None  # Mengembalikan None jika gagal mendapatkan profil

def check_balance():
    # Melakukan GET request untuk cek balance
    response = requests.get(url_balance, headers=headers)
    if response.status_code == 200:
        balance_data = response.json()
        print(f"{Fore.YELLOW+Style.BRIGHT}[ Balance ]: {balance_data[ 'data' ] / 1000000000}")
        return True  # Mengembalikan True jika berhasil mendapatkan balance
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Balance ]: That bai |{response.status_code}")
        return False  # Mengembalikan False jika gagal mendapatkan balance

def cekin_daily():
    # Melakukan GET request untuk check-in harian
    response = requests.post(url_checkin, headers=headers)
    if response.status_code == 200:
        data = response.json()
        day = data.get('data', {}).get('no', '')
        print(f"{Fore.GREEN+Style.BRIGHT}[ Check-in ]: Check-in berhasil | Day {day}")
    else:
        data = response.json()
        if data.get('message') == 'already claimed for today':
            print(f"{Fore.RED+Style.BRIGHT}[ Check-in ]: Misi selesai hari ini")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Check-in ]: Kegagalan | {data}")
        

def upgrade_storage():
    # Meminta konfirmasi dari pengguna
    confirm = input("Apakah ada peningkatan akomodasi? (y/n): ")
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_storage, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade storage ]: Sukses'
        else:
            return '[ Upgrade storage ]: Saldo tidak mencukupi, MATALU MINUS?'
    else:
        return None  # Mengembalikan None jika pengguna memilih 'n'

def upgrade_mining():
    # Meminta konfirmasi dari pengguna
    confirm = input("upgrade mining? (y/n): ")
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_mining, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade mining ]: Sukses'
        else:
            return '[ Upgrade mining ]: Saldo tidak mencukupi, MATALU MINUS?'
    else:
        return None  # Mengembalikan None jika pengguna memilih 'n'

def upgrade_holy():
    # Meminta konfirmasi dari pengguna
    confirm = input(" upgrade holy? (y/n): ")
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_holy, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade holy ]: Sukses'
        else:
            return '[ Upgrade holy ]: Saldo tidak mencukupi, MATALU MINUS?'
    else:
        return None  # Mengembalikan None jika pengguna memilih 'n'
# Modifikasi fungsi upgrade untuk menerima parameter konfirmasi
def upgrade_storage(confirm):
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_storage, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade storage ]: Sukses'
        else:
            return '[ Upgrade storage ]: Saldo tidak mencukupi, MATALU MINUS?'
    else:
        return None  # Mengembalikan None jika pengguna memilih 'n'

def upgrade_mining(confirm):
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_mining, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade mining ]: Sukses'
        else:
            return '[ Upgrade mining ]: Saldo tidak mencukupi, MATALU MINUS?'
    else:
        return None  # Mengembalikan None jika pengguna memilih 'n'

def upgrade_holy(confirm):
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_holy, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade holy ]: Sukses'
        else:
            return '[ Upgrade holy ]: Saldo tidak mencukupi, MATALU MINUS?'
    else:
        return None  # Mengembalikan None jika pengguna memilih 'n'

def get_tasks():
    
    response = requests.get('https://elb.seeddao.org/api/v1/tasks/progresses', headers=headers)

    tasks = response.json()['data']
    
    for task in tasks:
        if task['task_user'] is None or not task['task_user']['completed']:
            complete_task(task['id'],task['name'])

def complete_task(task_id,task_name):
   
    response = requests.post(f'https://elb.seeddao.org/api/v1/tasks/{task_id}', headers=headers)
    if response.status_code == 200:
        print(f"{Fore.GREEN+Style.BRIGHT}[ Tasks ]: Misi {task_name} Selesai/Sukses.")
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Tasks ]: Tidak dapat menyelesaikan tugas {task_name}, status code: {response.status_code}")


def main():
    print_welcome_message()
    tokens = load_credentials()  # Memuat daftar token
    
    # Meminta konfirmasi upgrade sekali saja sebelum loop
    confirm_storage = input("Tingkatkan memori secara otomatis KONTOL? (y/n): ")
    confirm_mining = input("Peningkatan eksploitasi otomatis PEPEQ? (y/n): ")
    confirm_holy = input("Tingkatkan versi suci secara otomatis ANJING? (y/n): ")
    confirm_task = input("Menyelesaikan tugas secara otomatis BABI? (y/n): ")
    while True:
        # try:
        # Memanggil fungsi upgrade berdasarkan konfirmasi awal
            hasil_upgrade = upgrade_storage(confirm_storage)
            hasil_upgrade1 = upgrade_mining(confirm_mining)
            hasil_upgrade2 = upgrade_holy(confirm_holy)
        
            for index, token in enumerate(tokens):
                headers[ 'telegram-data' ] = token
                info = get_profile()
                if info:
                    print(f"Memproses untuk token ke {info[ 'data' ][ 'name' ]}")
                    
                if hasil_upgrade:
                    print(hasil_upgrade)
                    time.sleep(1)  
                if hasil_upgrade1:
                    print(hasil_upgrade1) 
                    time.sleep(1)
                if hasil_upgrade2:
                    print(hasil_upgrade2)
                    time.sleep(1)

                # Melakukan GET request untuk cek balance terlebih dahulu
                if check_balance():
                    # Jika berhasil mendapatkan balance, lakukan check-in harian
                   
                    # Jika berhasil mendapatkan balance, lakukan POST request untuk claim
                    response = requests.post(url_claim, headers=headers)

                    # Cek status code dari response
                    if response.status_code == 200:
                        print(f"{Fore.GREEN+Style.BRIGHT}[ Claim ]: Klaim Berhasil NJING")
                    elif response.status_code == 400:
                        # Mendapatkan response JSON
                        response_data = response.json()
                        # Mencetak pesan dari response
                        print(f"{Fore.RED+Style.BRIGHT}[ Claim ]: Klaim gagal GOBLOK")
                    else:
                        print("Terjadi kesalahan, status code:", response.status_code)

                    cekin_daily()
                    catch_worm()
                    if confirm_task.lower() == 'y':
                        get_tasks()
            for i in range(30, 0, -1):
                sys.stdout.write(f"\r{Fore.CYAN+Style.BRIGHT}============ Selesai, harap tunggu ya ANJING {i} Detik lagi.. ============")
                sys.stdout.flush()
                time.sleep(1)
            print()  # Cetak baris baru setelah hitungan mundur selesai

            # Membersihkan konsol setelah hitungan mundur
            clear_console()

        
if __name__ == "__main__":
    main()
