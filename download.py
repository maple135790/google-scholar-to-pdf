import os
import time
from os import getcwd
from selenium import webdriver
from href_collect import hrefCollect
from json import dumps


def download() -> int:
    htmlPath = ".\\html"
    pdfPath = getcwd()+'\\pdf'
    chromeDriverPath = ".\\chromedriver.exe"
    topicHrefDict = hrefCollect(htmlPath)
    downloadCount = 0
    availIndex = 0
    retryTimes = 1
    availableSciHubUrls = [
        "https://sci-hub.se/",
        "https://sci-hub.ren/",
        "https://sci-hub.st/",
        "https://sci-hub.do/",
        "https://sci-hub.ee",
        "https://sci-hub.shop"
    ]
    downloadXpaths = [
        '//*[@id="buttons"]/button',
        '//*[@id="buttons"]/ul/li[2]/a',
        '//*[@id="buttons"]/button',
        '//*[@id="buttons"]/button',
        '//*[@id="buttons"]/ul/li[2]/a',
        '//*[@id="buttons"]/ul/li[2]/a'
    ]
    appState = {
        "recentDestinations": [
            {
                "id": "Save as PDF",
                "origin": "local",
                "account": ""
            }
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }

    with open("dl.log", 'w') as fLog:
        # for t in list(topicHrefDict.keys())[:3]:
        for t in topicHrefDict.keys():
            dlPath = pdfPath + "\\" + t
            if (not os.path.exists(dlPath)):
                os.mkdir(dlPath)
            chrome_options = webdriver.ChromeOptions()
            prefs = {'printing.print_preview_sticky_settings.appState': dumps(appState),
                     'savefile.default_directory': dlPath,
                     'download.default_directory': dlPath,
                     }
            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_argument('--kiosk-printing')
            driver = webdriver.Chrome(
                chromeDriverPath, chrome_options=chrome_options)
            fLog.write("[I]start download topic {}\n".format(t))
            for h in topicHrefDict[t]:
                isEntered = False
                while (not isEntered):
                    try:
                        driver.get(availableSciHubUrls[availIndex])
                        driver.find_element_by_id("open")
                        isEntered = True
                    except:
                        isEntered = False
                        availIndex = availIndex + \
                            1 if (availIndex + 1 <=
                                  len(availableSciHubUrls)-1) else 0
                        print('retry for {}s...'.format(1.5 * retryTimes))
                        time.sleep(1.5 * retryTimes)
                retryTimes = 1
                element = driver.find_element_by_name("request")
                element.send_keys(h)
                button_search = driver.find_element_by_id("open")
                button_search.click()
                try:
                    button_download = driver.find_element_by_xpath(
                        downloadXpaths[availIndex])
                    button_download.click()
                    print("[I]sci-hub download {}".format(h))
                    fLog.write("[I]sci-hub download {}\n".format(h))
                    downloadCount += 1
                except:
                    if (h.split(".")[-1] == 'pdf'):
                        print("[W]direct download {} ".format(h))
                        fLog.write("[W]direct download {} \n".format(h))
                        driver = webdriver.Chrome(options=chrome_options)
                        driver.get(h)
                        driver.execute_script('window.print();')
                        downloadCount += 1
                        time.sleep(5)
                    else:
                        print("[E]cannot be downloaded {}".format(h))
                        fLog.write("[E]cannot be downloaded {}\n".format(h))
                time.sleep(2.5)
    return downloadCount
