import os
from bs4 import BeautifulSoup


def hrefCollect(htmlpath: str) -> list:
    path = htmlpath
    collector = []
    files = os.listdir(path)
    for f in files:
        html = ""
        with open(".\\html\\{}".format(f)) as f:
            html = f.read()
        bs = BeautifulSoup(html, "html.parser")
        a = bs.select_one("#gs_res_ccl_mid")
        b = a.find_all("div", {"class": "gs_r gs_or gs_scl"})
        for x in b:
            c = x.find("h3", {"class": "gs_rt"})
            if (c == None):
                c = x.find("span", {"class": "gs_ctc"})
            collector.append(c.a['href'])
    return collector
