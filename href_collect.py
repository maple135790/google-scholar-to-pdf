import os
from bs4 import BeautifulSoup


def hrefCollect(htmlpath: str) -> dict:
    path = htmlpath
    collector = {}
    topics = os.listdir(path)
    if (".gitignore" in topics):
        topics.remove(".gitignore")
    for t in topics:
        files = os.listdir(path + "\\" + t)
        hrefs = []
        for f in files:
            html = ""
            with open(path + "\\" + t + "\\" + "{}".format(f)) as f:
                html = f.read()
            bs = BeautifulSoup(html, "html.parser")

            a = bs.select_one("#gs_res_ccl_mid")
            b = a.find_all("div", {"class": "gs_r gs_or gs_scl"})
            for x in b:
                c = x.find("h3", {"class": "gs_rt"})
                if (c == None):
                    c = x.find("span", {"class": "gs_ctc"})
                if (bool(c.find("a"))):
                    hrefs.append(c.a['href'])
        collector[t] = hrefs
    return collector
