import requests
from bs4 import BeautifulSoup as bs4

def goto_specific_page(page, url, goto_page, proxy, session):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "zh-TW,zh;q=0.9",
    }

    soup = bs4(page, "lxml")

    search_form_param = {}
    INFO = soup.find("input", {"name": "INFO"}).get("value")
    inputs = soup.find_all("input")
    for ip in inputs:
        if ip.get("name") is not None and (
            ip.get("name").startswith("@") or ip.get("name").startswith("_")
        ):
            if ip.get('type') == 'checkbox' :
                if ip.get('checked') is not None:
                    search_form_param[ip.get("name")] = "on" 
                else:
                    search_form_param[ip.get("name")] = ""
            else:
                search_form_param[ip.get("name")] = ip.get("value")
    search_form_param["INFO"] = INFO
    search_form_param["JPAGE"] = goto_page
    search_form_param["BUTTON"] = "GO"

    url = soup.find("form", {"name": "KM"}).get("action")


    response = session.post(url, data=search_form_param, headers=header, proxies=proxy)

    response.encoding = "UTF-8"
    

    return response.url, response.text, session