# -*- coding: utf-8 -*-
"""
#=========================================================
목적 : selenium Firefox 브라우저 동작 정의
* headless
* 쿠키
* 프록시
* 익스텐션 설치

https://www.reddit.com/r/webscraping/comments/qwxfdr/what_does/
#=========================================================
"""
import os, sys
from datetime import datetime
from time import sleep, time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

import pickle
import logging

from . import basicBrowser

from webdriver_manager.chrome import ChromeDriverManager


## 로거 설정
log = logging.getLogger(__name__)
log.info("Logging Started... {}".format(__name__))


class BaseChrome(basicBrowser.BasicBrowser):

    def __init__(self, config):

        self.driver    = None
        self.headless  = config['headless']
        self.user_agent = None
        self.profile   = config['profile']
        self.extension = config['extension']
        if 'proxy' in config:
            self.proxy = config['proxy']
        else:
            self.proxy = ''

        self.setUpOptions()
        # self.setUpProxy() # comment this line for ignore proxy

        #service = webdriver.ChromeService(log_output=log_path)
        #service = Service(executable_path=r'/usr/bin/chromedriver', log_output='aaa.log')

        # On Linux?
        # https://github.com/mozilla/geckodriver/issues/1756
        # binary = FirefoxBinary('/usr/lib/firefox-esr/firefox-esr')
        #self.driver = webdriver.Firefox(options=self.options, capabilities=self.capabilities, firefox_profile=self.profile, executable_path='./geckodriver.exe', firefox_binary=binary)
        #self.driver = webdriver.Firefox(options=self.options, capabilities=self.capabilities, firefox_profile=self.profile, executable_path='../geckodriver.exe')
        #self.driver = webdriver.Firefox(options=self.options, capabilities=self.capabilities, executable_path='geckodriver.exe', service_log_path=os.devnull)
        #self.driver = webdriver.Chrome(service=service, options=self.options)
        
        
    def get_driver(self):
        """웹드라이버 설정"""

        # 가상 디스플레이 사용 코드 추가
        #self.display = Display(visible=0, size=(1920, 1080))
        #self.display.start()

        #service = Service(executable_path=r'/usr/bin/chromedriver', log_output='aaa.log')
        service=Service(ChromeDriverManager().install(), log_output='browser.log')

        self.driver = webdriver.Chrome(service=service, options=self.options)
        return self.driver

    
    # Setup options for webdriver
    def setUpOptions(self):

        self.options = Options()

        # Default
        self.options.add_argument("--no-sandbox"); # Bypass OS security model
        self.options.add_argument("--disable-gpu"); # applicable to windows os only
        #self.options.add_argument("--remote-debugging-port=9222") # 멀티인스턴스시 사용금지
        self.options.add_argument('--disable-blink-features=AutomationControlled') # 구글 로그인 에러 해결

        #self.options.add_argument("ignore-certificate-errors")
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #self.options.add_argument('--disable-logging')

        #self.options.add_argument("--window-size=1920,1080")

        #self.options.add_argument("--disable-crash-reporter")
        #self.options.add_argument("--disable-oopr-debug-crash-dump")
        #self.options.add_argument("--no-crash-upload")

        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-renderer-backgrounding")
        self.options.add_argument("--disable-background-timer-throttling")
        self.options.add_argument("--disable-backgrounding-occluded-windows")
        self.options.add_argument("--disable-client-side-phishing-detection")
        self.options.add_argument("--disable-crash-reporter")
        self.options.add_argument("--disable-oopr-debug-crash-dump")
        self.options.add_argument("--no-crash-upload")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-low-res-tiling")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("--silent")

        if self.headless:
            self.options.add_argument("--headless")

        if self.user_agent:
            self.options.add_argument('user-agent={0}'.format(self.user_agent))

        if self.profile:
            profile_path = os.path.join(os.getcwd(), 'Chrome_Profiles', self.profile)
            self.options.add_argument("user-data-dir=" + profile_path)
            self.options.add_argument("--profile-directory=" + self.profile)
        
        if self.proxy:            
            self.options.add_argument('--proxy-server={}'.format(self.proxy))            

        if self.extension:
            self.options.add_extension(r'G:\PyExample\ebay_rank\extension\tunnelbear-3.6.0_0.crx')
            log.debug(f"loaded extension...")

        '''
        options.add_argument(f"--window-size=1366,768")
        options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--password-store=basic")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--enable-automation")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-software-rasterizer")

        options.add_argument(f"--user-data-dir=PATH_TO_CHROME_PROFILE")
        options.add_argument('--proxy-server=IP_ADRESS:PORT')
        '''


    # Setup proxy
    def setUpProxy(self):
        self.log(PROXY)
        self.capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY
        }

    # Simple logging method
    def log(s,t=None):
        now = datetime.now()
        if t == None :
            t = "Main"
        print ("%s :: %s -> %s " % (str(now), t, s))


    def __del__(self):

        self.driver.quit()
        #self.display.stop()
        print('Web Driver Destructor called.')


if __name__ == "__main__":

    config = {
        'headless': False,
        'profile': 'aaaa',
        'proxy': '',
        'proxy-port': '',
    }

    driver = ChromeBrowser(config=config)

    url = 'http://www.unlocktown.com/bbs/write.php?bo_table=qa'
    #url = 'https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php'
    url = 'https://www.att.com/deviceunlock/'
    url = 'https://www.google.com/'
    driver.run(url)