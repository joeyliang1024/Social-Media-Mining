import requests
import random
from bs4 import BeautifulSoup as bs4


def search_page(search_name, start_date, end_date, proxy, session):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "zh-TW,zh;q=0.9",
    }
    session = requests.Session() if session is None else session

    # print('----s1----')
    response = session.get(
        "https://twpat1.tipo.gov.tw/twpatc/twpatkm", headers=header, proxies=proxy
    )
    response.encoding = "UTF-8"

    print(response.cookies.get_dict())

    # print('----s2----')
    # TTS anti proxy
    # <script language="javascript">
    # document.writeln('<META HTTP-EQUIV=Refresh CONTENT=0;URL=twpatkm?@@'+Math.random()+'>');
    # </script>
    first_url = "https://twpat1.tipo.gov.tw/twpatc/twpatkm?@@{}".format(random.random())
    response = session.get(f"{first_url}", headers=header, proxies=proxy)
    response.encoding = "UTF-8"

    print(response.status_code)
    print(session.cookies.get_dict())
    soup = bs4(response.text, "lxml")
    search_url = soup.find("form", {"name": "KM"}).get("action")
    INFO = soup.find("input", {"name": "INFO"}).get("value")
    print(search_url)

    # print('----s3----')
    params = {
        "INFO": INFO,  # if contain date
        "@_0_57_S": "S_IX",
        "_0_57_S_CI": "on",
        "_0_57_S_CM": "on",
        "_0_57_S_CD": "on",
        "@_0_56_S": "S_IX",
        "_0_56_S_AA": "on",
        "_0_56_S_AG": "on",
        "@_0_55_S": "S6_LS",
        "_0_55_S_01*": "on",
        "_0_55_S_05*": "on",
        "_0_55_S_06*": "on",
        "_0_55_S_02*": "on",
        "_0_55_S_03*": "on",
        "_0_55_S_04*": "on",
        "@_0_58_S": "S7_RC",
        "@_0_54_S": "S_ZY",
        "@_0_6_S": "S_o",
        "@_5_5_T": "T_XX",
        "_5_5_T": search_name,
        "@_5_6_K": "K_DATETYPE",
        "_5_6_K": "ID",
        "@_5_7_T": "T_XX",
        "_5_7_T": start_date,
        "@_5_8_T": "T_XX",
        "_5_8_T": end_date,
        "BUTTON": "檢索",
    }
    # header.update({"Referer": first_url})
    response = session.post(search_url, data=params, headers=header, proxies=proxy)
    response.encoding = "UTF-8"

    soup = bs4(response.text, "lxml")
    list_hundred_lines_url = soup.find("select").find_all("option")[5].get("value")
    # list_hundred_lines_url = soup.select('body > form > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > div > table > tbody > tr > td:nth-child(1) > select > option:nth-child(6)')

    response = session.get(list_hundred_lines_url, headers=header, proxies=proxy)

    return response, list_hundred_lines_url, session
    # return


def advanced_search(start_date, end_date, proxy, session):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "zh-TW,zh;q=0.9",
    }
    session = requests.Session() if session is None else session

    response = session.get(
        "https://twpat2.tipo.gov.tw/twpatc/twpatkm", headers=header, proxies=proxy
    )
    response.encoding = "UTF-8"

    first_url = "https://twpat2.tipo.gov.tw/twpatc/twpatkm?@@{}".format(random.random())
    response = session.get(f"{first_url}", headers=header, proxies=proxy)
    response.encoding = "UTF-8"
    # with open("first_page.html", "w", encoding="UTF-8") as f:
    #     f.write(response.text)

    soup = bs4(response.text, "lxml")
    advanced_search_url = (
        soup.find("td", {"class": "menu"}).find_all("a")[1].get("href")
    )
    print(advanced_search_url)
    response = session.get(advanced_search_url, headers=header, proxies=proxy)
    response.encoding = "UTF-8"
    # with open("advanced_search.html", "w", encoding="UTF-8") as f:
    #     f.write(response.text)
    soup = bs4(response.text, "lxml")
    INFO = soup.find("input", {"name": "INFO"}).get("value")
    params = {
        "INFO": INFO,
        "@_0_57_S": "S_IX",
        "_0_57_S_CI": "on",
        "@_0_56_S": "S_IX",
        "_0_56_S_AA": "on",
        "_0_56_S_AG": "on",
        "@_0_55_S": "S6_LS",
        "_0_55_S_01*": "on",
        "@_0_58_S": "S7_RC",
        "@_0_54_S": "S_ZY",
        "@_0_6_S": "S_o",
        "@_3_5_X": "X_XX",
        "_3_5_X": "",
        "@_3_9_w": "w_IC:當前 IPC",
        "_3_9_w_1": "0",
        "_3_9_w_3": "IC",
        "_3_9_w_2": "C OR F OR G OR H",
        "@_3_10_w": "w_IQ:LOC",
        "_3_10_w_1": "0",
        "_3_10_w_3": "IQ",
        "_3_10_w_2": "",
        "@_3_6_K": "K_DATETYPE",
        "_3_6_K": "ID",
        "@_3_7_T": "T_XX",
        "_3_7_T": start_date,
        "@_3_8_T": "T_XX",
        "_3_8_T": end_date,
        "BUTTON": "檢索",
    }
    real_advanced_search_url = soup.find("form", {"name": "KM"}).get("action")
    response.encoding = "UTF-8"
    response = session.post(
        real_advanced_search_url, data=params, headers=header, proxies=proxy
    )
    # with open("list_page.html", "w", encoding="UTF-8") as f:
    #     f.write(response.text)
    soup = bs4(response.text, "lxml")
    list_hundred_lines_url = soup.find("select").find_all("option")[0].get("value")
    # list_hundred_lines_url = soup.select('body > form > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > div > table > tbody > tr > td:nth-child(1) > select > option:nth-child(6)')

    response = session.get(list_hundred_lines_url, headers=header, proxies=proxy)

    return response, list_hundred_lines_url, session


if __name__ == "__main__":
    # from proxy_pooler import ProxyPooler
    session = requests.Session()
    text = search_page("台積電", "20210101", "20210601", None, session)
    # print (text)
