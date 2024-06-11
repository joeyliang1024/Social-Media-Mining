from bs4 import BeautifulSoup as bs4
import requests
import random


def get_next_page_url(page, url, proxy, session: requests.Session):
    soup = bs4(page, "lxml")
    INFO = soup.find("input", {"name": "INFO"}).get("value")
    inputs = soup.find_all("input")
    search_form_param = {}

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
    search_form_param["JPAGE"] = ""
    search_form_param["_IMG_次頁.x"] = random.randint(2,34)
    search_form_param["_IMG_次頁.y"] = random.randint(2,34)
    
    url = soup.find("form", {"name": "KM"}).get("action")
    response = session.post(url, data=search_form_param, proxies=proxy)
    response.encoding = "UTF-8"
    return response.url, response.text, session
