from fetcher.search_page import advanced_search
from fetcher.get_page import get_page
from fetcher.goto_specific_page import goto_specific_page
from parsers.list_page import parse_list_page
from parsers.detail_page import parse_detail_page, ParserError
from parsers.next_page import get_next_page_url
from proxy.web_share_proxy import ProxyPoolFromWebShare
from logger.csv_logger import CsvLogger
from logger.sqlite_logger import SQLiteLogger
import requests
from requests.auth import HTTPProxyAuth
import time
import random
import fire
import sys
import datetime
import os
import traceback
def main(start_time=None, end_time=None, start_page=None, start_idx=None, end_page=None, proxy_idx=None):
    print("Running with parameters: ", start_time, end_time, start_page, start_idx)

    if start_time is None or end_time is None:
        print("error")
        raise ValueError("start_time and end_time must be provided")
    if start_time > end_time:
        print("error")
        raise ValueError("start_time must be earlier than end_time")
    if start_page :
        start_page = int(start_page)
    if start_idx:
        start_idx = int(start_idx)
    if end_page:
        end_page = int(end_page)
    if proxy_idx:
        proxy_idx = int(proxy_idx)

    proxy_pool = ProxyPoolFromWebShare(start_index=proxy_idx)
    proxy = proxy_pool.get_proxy()
    print(f"Using proxy: {proxy['ip']}:{proxy['port']}")
    auth = HTTPProxyAuth(proxy["username"], proxy["password"])

    session = requests.Session()

    proxies = {
        "http": f"http://{proxy['ip']}:{proxy['port']}",
    }

    session.proxies = proxies
    session.auth = auth

    path = f'data_{start_time}_{end_time}_sp{start_page}_ep{end_page}'
    if not os.path.exists(path):
        os.makedirs(path)
    csv_logger = CsvLogger(path)
    sqlite_logger = SQLiteLogger(path)
    row_name = [
        "公告號",
        "公告日",
        "公報卷期",
        "證書號",
        "申請號",
        "申請日",
        "公報IPC",
        "當前IPC",
        "申請人",
        "當前專利權人",
        "發明人",
        "代理人",
        "當前代理人",
        "摘要",
    ]
    
    csv_logger.init_logger(row_name)
    sqlite_logger.init_logger(row_name)

    proxy_fail = True

    while proxy_fail:
        try:
            res, list_url, session = advanced_search(
                start_time, end_time, proxy, session
            )
            proxy_fail = False
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            proxy_pool.delete_proxy(proxy["ip"])
            proxy = proxy_pool.get_proxy()
            auth = HTTPProxyAuth(proxy["username"], proxy["password"])
            session = requests.Session()
            print(f"New proxy: {proxy['ip']}:{proxy['port']}")
            proxies = {
                "http": f"http://{proxy['ip']}:{proxy['port']}",
            }
            session.proxies = proxies

    list_page, session = get_page(list_url, proxy, session)
    index = start_page if start_page else 0
    link_idx = start_idx if start_idx else 0
    restart_flag = False

    if start_page:
        list_url, list_page, session = goto_specific_page(
            list_page, list_url, start_page, proxy, session
        )


    while 1:
        # print(f"Page {index+ 1: 3} Running", end="\t")
        with open(f'{index}.html', 'w', encoding='utf-8') as f:
            f.write(list_page)
        # print(list_url)
        list_links, has_next_page = parse_list_page(list_page)
        # print("List links: ", len(list_links))
        # print(list_links)
        if link_idx != 0:
            list_links = list_links[link_idx:]
        link_idx = 0
        for link in list_links:
            try:
                detail_page, session = get_page(link, proxy, session)
                data = parse_detail_page(detail_page)
                link_idx += 1
                csv_logger.log(data)
                sqlite_logger.log(data)
                time.sleep(random.randint(2, 4))
            except ParserError:
                restart_flag = True
            except requests.exceptions.HTTPError:
                restart_flag = True
            except Exception as e:
                print(traceback.format_exc())
                print(e)
                restart_flag = True

            if restart_flag:
                print("Restarting")
                time.sleep(random.randint(5, 10))
                proxy_pool.delete_proxy(proxy["ip"])
                proxy = proxy_pool.get_proxy()
                auth = HTTPProxyAuth(proxy["username"], proxy["password"])
                session = requests.Session()
                print(f"New proxy: {proxy['ip']}:{proxy['port']}")
                proxies = {
                    "http": f"http://{proxy['ip']}:{proxy['port']}",
                    # "https": f"https://{proxy['ip']}:{proxy['port']}",
                }
                session.proxies = proxies
                
                proxy_fail = True
                retry_times = 0
                while proxy_fail:
                    try:
                        if retry_times > 20: 
                            break
                        retry_times += 1
                        res, list_url, session = advanced_search(
                            start_time, end_time, proxy, session
                        )
                        list_page, session = get_page(list_url, proxy, session)
                        list_url, list_page, session = goto_specific_page(
                            list_page, list_url, index, proxy, session
                        )
                        proxy_fail = False
                    except Exception as e:
                        print(traceback.format_exc())
                        print(e)
                        proxy_pool.delete_proxy(proxy["ip"])
                        proxy = proxy_pool.get_proxy()
                        auth = HTTPProxyAuth(proxy["username"], proxy["password"])
                        session = requests.Session()
                        print(f"New proxy: {proxy['ip']}:{proxy['port']}")
                        proxies = {
                            "http": f"http://{proxy['ip']}:{proxy['port']}",
                            # "https": f"https://{proxy['ip']}:{proxy['port']}",
                        }
                        session.proxies = proxies
                        time.sleep(random.randint(5, 10))

                restart_flag = False
                proxy_fail = False
            now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
            print(f"{now.strftime('%Y-%m-%d, %H:%M:%S')}  {index:3} -- {link_idx: 3} Finished", end="\n")
            sys.stdout.flush()
        link_idx = 0
        

        if not has_next_page:
            break
        else:
            # list_url, list_page, session = goto_specific_page(
            #     list_page, list_url, index, proxy, session
            # )
            list_url, list_page, session = get_next_page_url(
                list_page, list_url, proxy, session
            )
            index += 1

        if end_page and index >= end_page:
            break
        
        time.sleep(random.randint(2, 4))
        print("Finished")

    csv_logger.close()
    sqlite_logger.close()


if __name__ == "__main__":
    fire.Fire(main)
