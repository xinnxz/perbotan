import requests
import urllib.parse
from package.core.headers import headers


def encode_query_id(query_id):
    return urllib.parse.quote(query_id, safe="")


def get_token(query_id, proxies=None):
    auth_data = encode_query_id(query_id=query_id)
    url = f"https://api.pixelfarm.app/user/login?auth_data={auth_data}"

    try:
        response = requests.get(url=url, headers=headers(), proxies=proxies, timeout=20)
        token = response.json()["data"]
        return token
    except:
        return None
