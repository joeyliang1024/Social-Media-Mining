def get_page(url, proxy, session):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "zh-TW,zh;q=0.9",
    }
    response = session.get(url, headers=header, proxies=proxy)
    response.raise_for_status()
    response.encoding = "UTF-8"
    return response.text, session
