# -*- coding: utf-8 -*-
"""
#=========================================================
목적 : 브라우저가 가져야할 기본기능 모음

https://www.reddit.com/r/webscraping/comments/qwxfdr/what_does/
#=========================================================
"""
import os, sys
from datetime import datetime
from time import sleep, time

import pickle
import logging

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

## 로거 설정
log = logging.getLogger(__name__)
log.info("Logging Started... {}".format(__name__))


class BasicBrowser():       

    # Use time.sleep for waiting and uniform for randomizing
    def wait_between(self, a, b):
        rand=uniform(a, b)
        sleep(rand)


    def dump_cookie(self, filename):

        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))


    def load_cookie(self, filename):

        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)


    def save_cookie(self, filename):
        ''' 쿠키를 TXT 파일로 저장 '''

        cookies = self.driver.get_cookies()
        print('Cookie DATA: \n', cookies)

        with open(filename, "w") as f:
            for cookie in cookies:
                f.write(str(cookie)+"\n")


    def read_cookie(self, filename):
        ''' TXT 파일로부터 쿠키 가져오기 '''

        with open(filename, "r") as f:
            cookies = eval(f.read())

        for cookie in cookies:
            self.driver.add_cookie(cookie)


    def add_cookie(self, cookie_dict=None):
        ''' 쿠키 추가 '''

        self.driver.add_cookie({"name": "test1", "value": "cookie1"})


    def __del__(self):

        self.driver.quit()
        #self.display.stop()
        print('Web Driver Destructor called.')


    def get_driver(self):

        return self.driver

        
    def page_loading_completed(self, driver):
        """
            페이지 로딩여부를 체크한다.
        """

        result = WebDriverWait(driver, 30).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        print('페이지 로딩 상태: {}'.format(result))


    def scroll_into_view(self, element):
        ''' element가 화면에 위치하도록 한다. block: center 중앙에 보이도록'''

        self.driver.execute_script('arguments[0].scrollIntoView({block: "center", behavior: "smooth"});', element)


    def check_exists_by_xpath(self, xpath, method='xpath'):
        try:
            if (method == 'css_selector'):
                self.driver.find_element(By.CSS_SELECTOR, xpath)
            else:
                self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True
    

    def goto_url(self, url):
        
        self.driver.get(url)
        self.page_loading_completed(self.driver)


    def click_link(self, element):
        
        element.click()
        self.page_loading_completed(self.driver)

    def get_title(self):
        
        return self.driver.title
    
    def get_page_source(self):
        
        return self.driver.page_source

    def close_tabs(self, main_window):
        ''' 메인윈도우를 제외한 모든 윈도우를 닫는다. '''

        for w in self.driver.window_handles:
            if w != main_window:
                print('close window:',w)
                self.driver.switch_to.window(w)
                self.driver.close()
                sleep(1)
        
        self.driver.switch_to.window(main_window)

