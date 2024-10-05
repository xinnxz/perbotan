import requests
import time

from package.core.headers import headers
from package import base
from package.core.info import balance, my_cards


def cards(token, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/inventory/cards"

    try:
        response = requests.get(
            url=url, headers=headers(token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def buy_card(token, card_id, category, proxies=None):
    url = "https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users/buy-card"
    payload = {"card_id": card_id, "category": category}

    try:
        response = requests.post(
            url=url, headers=headers(token), json=payload, proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def get_highest_ratio_item(token, proxies=None):
    inventory_cards = cards(token=token, proxies=proxies)
    current_balance = balance(token=token, proxies=proxies)
    current_cards = my_cards(token=token, proxies=proxies)
    friends_count = inventory_cards["equipment"][0]["newRefsCount"]

    # Function to update price and profit of bought cards
    def update_inventory_prices_and_profits(current_cards, inventory_cards):
        for card in current_cards:
            card_id = card["cardId"]
            card_level = card["level"]

            for category in inventory_cards.values():
                for item in category:
                    if item["id"] == card_id:
                        item["price"] = item["prices"][card_level]
                        try:
                            item["profit"] = (
                                item["profits"][card_level]
                                - item["profits"][card_level - 1]
                            )
                        except:
                            item["profit"] = (
                                item["stackingProfits"][card_level]
                                - item["stackingProfits"][card_level - 1]
                            )

    update_inventory_prices_and_profits(
        current_cards=current_cards, inventory_cards=inventory_cards
    )

    # Function to calculate price/profit ratio
    def profit_price_ratio(item):
        return float(item["profit"]) / float(item["price"])

    # Function to check if requirements are met
    def requirements_met(requirements, cards):
        if not requirements:
            return True
        required_card_id = requirements.get("requiredCardId")
        required_card_level = requirements.get("requiredCardLevel")
        required_friends_count = requirements.get("requiredFriendsCount")
        if required_friends_count is not None and int(required_friends_count) > int(
            friends_count
        ):
            return False
        if required_card_id is None or required_card_level is None:
            return True
        for card in cards:
            if (
                card["cardId"] == required_card_id
                and card["level"] >= required_card_level
            ):
                return True
        return False

    # Variable to store the item with the highest ratio
    highest_ratio_item = None
    highest_ratio = 0

    # Iterate through all categories
    for category in inventory_cards.keys():
        for item in inventory_cards[category]:
            item_price = float(item["price"])
            if item_price <= current_balance and requirements_met(
                item["requirementsJson"], current_cards
            ):
                ratio = profit_price_ratio(item)
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    highest_ratio_item = {
                        "category": category,
                        "id": item["id"],
                        "name": item["name"],
                        "price": item_price,
                        "profit": float(item["profit"]),
                        "ratio": ratio,
                    }

    return highest_ratio_item


def process_buy_card(token, proxies=None):
    while True:
        highest_ratio_item = get_highest_ratio_item(token=token, proxies=proxies)
        if highest_ratio_item:
            card_id = highest_ratio_item["id"]
            category = highest_ratio_item["category"]
            card_name = highest_ratio_item["name"]
            card_price = highest_ratio_item["price"]
            card_profit = highest_ratio_item["profit"]
            base.log(
                f"{base.white}Auto Buy Card: {base.yellow}Highest profitable card {base.white}| {base.yellow}Category: {base.white}{category} - {base.yellow}Name: {base.white}{card_name} - {base.yellow}Price: {base.white}{int(card_price):,} - {base.yellow}Profit Increase: {base.white}{int(card_profit):,}"
            )
            start_buy_card = buy_card(
                token=token, card_id=card_id, category=category, proxies=proxies
            )
            try:
                buy_card_name = start_buy_card["card"]["name"]
                buy_card_level = start_buy_card["level"]
                current_balance = start_buy_card["balance"]
                base.log(
                    f"{base.white}Auto Buy Card: {base.green}Sucess {base.white}| {base.green}New balance: {base.white}{current_balance} - {base.green}Buy Card: {base.white}{buy_card_name} - {base.green}Level: {base.white}{buy_card_level}"
                )
            except:
                error_message = start_buy_card["message"]
                base.log(f"{base.white}Auto Buy Card: {base.red}{error_message}")
                break
        else:
            base.log(
                f"{base.white}Auto Buy Card: {base.red}Not enough coin to buy card"
            )
            break
