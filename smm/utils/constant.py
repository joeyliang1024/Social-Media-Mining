HOME_PAGE_URL = "https://ctext.org/searchbooks.pl?if=gb&searchu=%E6%98%8E%E5%AF%A6%E9%8C%84"
HOME_PATH_TXT_PTH = "origin_craw_data\home_page.txt"
HOME_PAGE_BOOK_PTH = "origin_craw_data\home_page_book.json"
PROXY_URL = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
# add proxy here...
PROXY_ADDRESS_LIST = [
    '36.226.245.61:80',
    '103.172.42.113:8080', 
    '103.189.249.163:1111', 
    '103.165.222.190:8080',
    ]

PROXY_LIST = [
    {"http": f"http://{proxy_address}"} for  proxy_address in PROXY_ADDRESS_LIST
]