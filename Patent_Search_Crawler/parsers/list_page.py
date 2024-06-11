from bs4 import BeautifulSoup as bs4


def parse_list_page(page):
    soup = bs4(page, "lxml")
    rows = [tr for tr in soup.find("table", {"class": "sumtab"}).find_all("tr")]
    # print(rows[0])
    links = []
    for r in rows[1:]:
        try:
            link = r.find_all("td")[2].find("a").get("href")
            links.append(link)
        except:
            continue
    if soup.find("input", {"name": "_IMG_次頁"}):
        return links, True
    return links, False


if __name__ == "__main__":
    page = open("list_page.html", "r", encoding="UTF-8").read()
    links = parse_list_page(page)
    print(links)
