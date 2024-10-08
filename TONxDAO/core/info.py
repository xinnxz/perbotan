import requests,json,os
from core.headers import headers
from urllib.parse import unquote, parse_qs

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    banner = r"""
 ▄▄▄       ██▀███ ▓██   ██▓ ▄▄▄     ▄▄▄█████▓ █    ██ ▒██   ██▒
▒████▄    ▓██ ▒ ██▒▒██  ██▒▒████▄   ▓  ██▒ ▓▒ ██  ▓██▒▒▒ █ █ ▒░
▒██  ▀█▄  ▓██ ░▄█ ▒ ▒██ ██░▒██  ▀█▄ ▒ ▓██░ ▒░▓██  ▒██░░░  █   ░
░██▄▄▄▄██ ▒██▀▀█▄   ░ ▐██▓░░██▄▄▄▄██░ ▓██▓ ░ ▓▓█  ░██░ ░ █ █ ▒ 
 ▓█   ▓██▒░██▓ ▒██▒ ░ ██▒▓░ ▓█   ▓██▒ ▒██▒ ░ ▒▒█████▓ ▒██▒ ▒██▒
 ▒▒   ▓▒█░░ ▒▓ ░▒▓░  ██▒▒▒  ▒▒   ▓▒█░ ▒ ░░   ░▒▓▒ ▒ ▒ ▒▒ ░ ░▓ ░
  ▒   ▒▒ ░  ░▒ ░ ▒░▓██ ░▒░   ▒   ▒▒ ░   ░    ░░▒░ ░ ░ ░░   ░▒ ░
  ░   ▒     ░░   ░ ▒ ▒ ░░    ░   ▒    ░       ░░░ ░ ░  ░    ░  
      ░  ░   ░     ░ ░           ░  ░           ░      ░    ░  
                   ░ ░                                                                                                                                                                                                                  
"""
    print(f"\033[92m{banner}")

def get_info(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/profile"
    )
    auth_headers = headers(token)
    response = requests.get(url=url, headers=auth_headers)
    data = response.json()
    full_name = data.get('full_name', 'No name provided')
    coins = data.get('coins', 'No coins provided')
    energy = data.get('energy', 'No energy provided')
    return full_name, coins, energy

def get_fullname(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/profile"
    )
    auth_headers = headers(token)
    response = requests.get(url=url, headers=auth_headers)
    data = response.json()
    full_name = data.get('full_name', 'No name provided')
    return full_name

def get_info_coin(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/profile"
    )
    auth_headers = headers(token)
    response = requests.get(url=url, headers=auth_headers)
    data = response.json()
    coins = data.get('coins', 'No coins provided')
    return coins

def get_info_energy(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/profile"
    )
    auth_headers = headers(token)
    response = requests.get(url=url, headers=auth_headers)
    data = response.json()
    energy = data.get('energy', 'No energy provided')
    return energy

def get_user_dao(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/dao_users"
    )
    auth_headers = headers(token)
    response = requests.get(url=url, headers=auth_headers)
    data = response.json()
    return data

def get_token(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/centrifugo-token"
    )
    auth_headers = headers(token)
    response = requests.get(url=url, headers=auth_headers)
    data = response.json()["token"]
    return data

def get_username(token):
    tokens = open('data.txt').read().strip().split('\n')
    for data in tokens:
        return json.loads(parse_qs(data)['user'][0]).get('username', '<NOT SET>')

def config(name, default):
    with open("config.json", 'r') as file:
        config = json.load(file)
        return config.get(name, default)