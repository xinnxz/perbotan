def headers(token=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        'accept-language': 'en,en-EG;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        "origin": "https://app.production.tonxdao.app/",
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://app.production.tonxdao.app/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        'x-requested-with': 'org.telegram.messenger',
    }
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
        # headers["Authorization"] = token
    return headers