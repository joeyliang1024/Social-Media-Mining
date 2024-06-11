from bs4 import BeautifulSoup as bs4

TO_REC = [
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


class ParserError(Exception):
    pass


def parse_detail_page(page):
    soup = bs4(page, "lxml")

    table = soup.find("div", {"class": "L_box"}).find("table")
    rows = [tr for tr in table.find_all("tr")]
    data = {}
    for r in rows:
        try:
            if r.find_all("td")[0].text in TO_REC:
                data.update(
                    {
                        r.find_all("td")[0].text: r.find_all("td")[1].text.replace(
                            "&nbsp", " "
                        )
                    }
                )
            # data.update({r.find_all("td")[0].text: r.find_all("td")[1].text})
        except:
            raise ParserError("Error in parsing detail page")

    return data


if __name__ == "__main__":
    page = open("detail_page.html", "r", encoding="UTF-8").read()
    data = parse_detail_page(page)
    print(data)
