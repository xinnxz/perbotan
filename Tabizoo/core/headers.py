def headers(data):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://miniapp.tabibot.com",
        "Rawdata": data,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }
    return headers
