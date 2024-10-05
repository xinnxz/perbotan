import requests

from smart_airdrop_claimer import base
from core.headers import headers


def get_me(token, proxies=None):
    url = "https://backend.babydogepawsbot.com/getMe"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        balance = data["balance"]
        return balance
    except:
        return None


def get_card(token, proxies=None):
    url = "https://backend.babydogepawsbot.com/cards"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def buy_card(token, card_id, proxies=None):
    url = "https://backend.babydogepawsbot.com/cards"
    payload = {"id": card_id}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        return data
    except:
        return None


def get_higest_ratio_item(token, proxies=None):
    balance = get_me(token=token, proxies=proxies)
    categories = get_card(token=token, proxies=proxies)

    highest_ratio_item = None
    highest_ratio = 0

    for category in categories:
        category_id = category["id"]
        category_name = category["name"]
        cards = category["cards"]
        for card in cards:
            card_id = card["id"]
            card_name = card["name"]
            card_price = card["upgrade_cost"]
            card_profit = card["farming_upgrade"]
            is_available = card["is_available"]
            ratio = float(card_profit) / float(card_price)

            if (
                int(card_price) <= int(balance)
                and ratio > highest_ratio
                and is_available
            ):
                highest_ratio = ratio
                highest_ratio_item = {
                    "category": category_name,
                    "id": card_id,
                    "name": card_name,
                    "price": card_price,
                    "profit": card_profit,
                    "ratio": ratio,
                }

    return highest_ratio_item


def process_buy_card(token, proxies=None):
    while True:
        highest_ratio_item = get_higest_ratio_item(token=token, proxies=proxies)
        if highest_ratio_item:
            category_name = highest_ratio_item["category"]
            card_id = highest_ratio_item["id"]
            card_name = highest_ratio_item["name"]
            card_price = highest_ratio_item["price"]
            card_profit = highest_ratio_item["profit"]
            base.log(
                f"{base.white}Auto Buy Card: {base.yellow}Highest profitable card {base.white}| {base.yellow}Category: {base.white}{category_name} - {base.yellow}Name: {base.white}{card_name} - {base.yellow}Price: {base.white}{int(card_price):,} - {base.yellow}Profit Increase: {base.white}{int(card_profit):,}"
            )
            start_buy_card = buy_card(token=token, card_id=card_id, proxies=proxies)
            try:
                balance = start_buy_card["balance"]
                profit_per_hour = start_buy_card["profit_per_hour"]
                base.log(
                    f"{base.white}Auto Buy Card: {base.green}Sucess {base.white}| {base.green}New balance: {base.white}{balance:,} - {base.green}New Profit per Hour: {base.white}{profit_per_hour:,}"
                )
            except Exception as e:
                base.log(f"{base.white}Auto Buy Card: {base.red}Error - {e}")
                break
        else:
            base.log(
                f"{base.white}Auto Buy Card: {base.red}Not enough coin to buy card"
            )
            break
