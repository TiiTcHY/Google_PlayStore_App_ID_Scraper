import time
import re
from pandas import DataFrame
from bs4 import BeautifulSoup
from collections import OrderedDict
import urllib.request, urllib.error, urllib.parse
from selenium import webdriver
driver = webdriver.Chrome()
driver.implicitly_wait(30)
def ScrapeID():
    try:
        SCROLL_PAUSE_TIME = 1.0
        URL =("https://play.google.com/store/search?q=")
        SearchTerm = ("")
        Apps = ("&c=apps")
        FullURL = URL+SearchTerm+Apps
        driver.get(FullURL)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        soup = BeautifulSoup(driver.page_source, "html.parser")
        l= []
        res = []
        for c in soup:
          ID = c.findAll("a", href=re.compile("id="))
          for apps in ID:
              x=apps.get('href',None)
              if x.find("/store/apps/details?id=")!=-1:
                if not(x[23:] in l):
                  l.append(x[23:])
                  df = DataFrame (l)
                  df.drop_duplicates()
                  df.columns = ['appID']
                  df.to_csv('out.csv', index=False)              
    finally:
        driver.quit()
        
ScrapeID()
