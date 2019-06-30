from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import os
import pickle

def rawtable(cookie):
    headless = Options()
    headless.add_argument("--headless")
    ngrok = webdriver.Chrome(chrome_options=headless)

    ngrok.get("https://dashboard.ngrok.com/a")
    ngrok.add_cookie(cookie)
    ngrok.refresh()
    ngrok.get("https://dashboard.ngrok.com/status")

    try:
        element = WebDriverWait(ngrok, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "rt-table"))
            )
    except TimeoutException:
        print("Didn't load!")

    tableid = ngrok.find_element_by_class_name("rt-table")
    tablecontent = tableid.find_elements_by_class_name("rt-td")

    #ngrok.quit()

    return tablecontent

def rawtabletext(cookie):
    raw = rawtable(cookie)
    rawtext = []
    for i in range(0, len(raw)):
        if((i != 0) and (i % 5 != 0)):
            rawtext.append(str(raw[i].text))

    return rawtext

def servertable(rawtext, servernum):
    index = 0
    server = {'type':'', 'dns':'', 'port':'', 'ip':''}
    for i in range(0, servernum):
        index += 4

    server['type'] = rawtext[index].split(":")[0]
    server['dns'] = rawtext[index].split("//")[1].split(":")[0]
    server['port'] = rawtext[index].split("//")[1].split(":")[1]
    server['ip'] = rawtext[index+1]

    return server

def tabledict(rawtext):
    table = []
    servercount = int(len(rawtext)/4)

    for i in range(0, servercount):
        table.append(servertable(rawtext, i))

    return table

def getcookie():
    input("A browser will now open. Press enter and return here once you have logged in.\n")
    chrome_as_app = Options()
    chrome_as_app.add_argument("--app=https://dashboard.ngrok.com")
    chrome_as_app.add_argument("--window-size=300,400")
    ngrok = webdriver.Chrome(chrome_options=chrome_as_app)
    input("Press enter if you have logged in.")
    cookie = ngrok.get_cookie("default")
    cookie.pop('expiry')
    ngrok.quit()

    return cookie

def login():
    cookie = getcookie()
    path_cookie = str(Path.home())+'/.config/pygrok/cookie'
    pickle.dump(cookie, open(path_cookie, "wb"))

def logindriver():
    if(os.path.exists(str(Path.home())+'/.config/pygrok') == False):
        print("Creating the pygrok config folder...")
        os.mkdir(str(Path.home())+'/.config/pygrok')

    if(os.path.exists(str(Path.home())+'/.config/pygrok/cookie') == False):
        login()

    cookie = pickle.load(open(str(Path.home())+'/.config/pygrok/cookie', "rb"))

    return cookie
