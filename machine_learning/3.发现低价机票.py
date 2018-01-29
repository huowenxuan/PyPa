import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt

url = 'https://www.google.com/flights/explore/#explore;f=SFO;t=r-Europe-0x46ed8886cfadda85%253A0x72ef99e6b3fcf079;li=0;lx=14;d=2018-02-05'
driver = webdriver.PhantomJS()
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap['phantomjs.page.settings.userAgent'] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36 QQBrowser/4.2.4976.400")
driver = webdriver.PhantomJS(desired_capabilities=dcap)

driver.implicitly_wait(20)
# 发起请求
driver.get(url)
# 保存截图，返回True为成功
driver.save_screenshot(r'flight_explorer.png')
