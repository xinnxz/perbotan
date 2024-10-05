import requests

from smart_airdrop_claimer import base
from core.headers import headers


def get_boost(token, proxies=None):
    url = "https://api-clicker.ageofmars.io/v1/boosts"

    try:
        response = requests.get(
            url=url,
            headers=headers(token=token),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        taps = data["data"]["taps"]
        collector = data["data"]["collector"]
        return taps, collector
    except:
        return None


def upgrade_tap(token, tap_type, proxies=None):
    url = "https://api-clicker.ageofmars.io/v1/boosts/upgrade"
    payload = {"boost": tap_type}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        taps = data["data"]["taps"]
        return taps
    except:
        return None


def upgrade_collector(token, collector_type, proxies=None):
    url = "https://api-clicker.ageofmars.io/v1/collector/detail/upgrade"
    payload = {"detail": collector_type}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        collector = data["data"]
        return collector
    except:
        return None


def process_upgrade_tap(token, proxies=None):
    try:
        taps, collector = get_boost(token=token, proxies=proxies)
        min_level = 10000
        for tap in taps:
            tap_type = tap["id"]
            tap_name = tap["name"]
            tap_level = tap["level"]
            base.log(
                f"{base.white}Auto Upgrade Tap: {base.yellow}INFO {base.white}| {base.yellow}Name: {base.white}{tap_name} - {base.yellow}Level: {base.white}{tap_level}"
            )
            if tap_level < min_level:
                min_level = tap_level
                upgrade_tap_id = tap_type
                upgrade_tap_name = tap_name
        base.log(
            f"{base.white}Auto Upgrade Tap: {base.green}UPGRADE {base.white}| {base.yellow}Name: {base.white}{upgrade_tap_name} - {base.yellow}Level: {base.white}{min_level}"
        )
        start_upgrade = upgrade_tap(
            token=token, tap_type=upgrade_tap_id, proxies=proxies
        )
        for tap in start_upgrade:
            tap_type = tap["id"]
            tap_name = tap["name"]
            tap_level = tap["level"]
            base.log(
                f"{base.white}Auto Upgrade Tap: {base.yellow}INFO {base.white}| {base.yellow}Name: {base.white}{tap_name} - {base.yellow}Level: {base.white}{tap_level}"
            )
    except Exception as e:
        base.log(f"{base.white}Auto Upgrade Tap: {base.red}Error - {e}")


def process_upgrade_collector(token, proxies=None):
    try:
        taps, collector = get_boost(token=token, proxies=proxies)
        min_level = 10000
        for c in collector:
            collector_type = c["id"]
            collector_name = c["name"]
            collector_level = c["level"]
            base.log(
                f"{base.white}Auto Upgrade Collector: {base.yellow}INFO {base.white}| {base.yellow}Name: {base.white}{collector_name} - {base.yellow}Level: {base.white}{collector_level}"
            )
            if collector_level < min_level:
                min_level = collector_level
                upgrade_collector_id = collector_type
                upgrade_collector_name = collector_name
        base.log(
            f"{base.white}Auto Upgrade Collector: {base.green}UPGRADE {base.white}| {base.yellow}Name: {base.white}{upgrade_collector_name} - {base.yellow}Level: {base.white}{min_level}"
        )
        start_upgrade = upgrade_collector(
            token=token, collector_type=upgrade_collector_id, proxies=proxies
        )
        for c in start_upgrade:
            collector_type = c["id"]
            collector_name = c["name"]
            collector_level = c["level"]
            base.log(
                f"{base.white}Auto Upgrade Collector: {base.yellow}INFO {base.white}| {base.yellow}Name: {base.white}{collector_name} - {base.yellow}Level: {base.white}{collector_level}"
            )
    except Exception as e:
        base.log(f"{base.white}Auto Upgrade Collector: {base.red}Error - {e}")
