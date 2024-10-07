def headers(token=None):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://g.cyberfin.xyz",
        "Referer": "https://g.cyberfin.xyz/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers
