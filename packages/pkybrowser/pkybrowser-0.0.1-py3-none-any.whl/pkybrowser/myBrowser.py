# -*- coding: utf-8 -*-
'''
#=====================================================================
제목: 이베이 내상품 자동클릭
버전: v0.1
날짜: 2021-12-13
설명: 조회수 또는 상품을 상단에 배치하기 위해서는 많은 클릭이 필요
#=====================================================================
'''
import os
import sys
import re
#import pyautogui
from time import sleep, time
import argparse
import random

from . import baseChrome

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import logging
from .LIB import logger

from bs4 import BeautifulSoup

# 로거 설정
log = logging.getLogger(__name__)
log.info(f"Logging Started... {__name__}")


class MyBrowser(baseChrome.BaseChrome):

    def __init__(self, config):
        
        super().__init__(config)
        

    def page_loading_completed(self, driver):
        """
            Page loading check
        """

        result = WebDriverWait(driver, 30).until(lambda driver: driver.execute_script(
            'return document.readyState') == 'complete')
        #log.debug('Page loaded: {}'.format(result))
        
    
    def open_url_new_tab(self, driver, url):
        """
            Open a link with new tab
        """
        # open new window
        driver.execute_script("window.open('" + url +"');")


    def run(self, driver, keyword, itemIDList):

        log.info('정보 => {}, {}'.format(keyword, itemIDList))

        #driver = self.driver

        #driver.set_window_position(0, 0)
        #driver.set_window_size(1150, 850)
        #log.debug('브라우저 크기: {}'.format(driver.get_window_rect()))
        
        #driver.get(url)
        #self.page_loading_completed(driver)
        
        # 메인 윈도우 핸들
        main_window = driver.current_window_handle
        #print('1. current_window_handle:', main_window)
        
        
        ## Move to Search Box
        #log.debug(">>> Search Box 이동")
        sleep(1)
        search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="gh-ac"]')))
        search_box.clear()
        search_box.send_keys(keyword)
        #search_box.send_keys(Keys.RETURN)

        
        ## Click Search Button
        log.debug('>>> Search Button 클릭')
        sleep(1)
        if self.check_exists_by_xpath('//input[@id="gh-btn"]'):
          btn_search = driver.find_element('xpath','//input[@id="gh-btn"]')
        else:
          btn_search = driver.find_element('xpath','//button[@id="gh-search-btn"]')
        	
        #btn_search = driver.find_element('xpath','//input[@id="gh-btn"]')
        ActionChains(driver).move_to_element(btn_search).click().perform()
        sleep(2)
        self.page_loading_completed(driver)
        
        if driver.find_element('xpath','//div[@class="srp-controls__sort srp-controls__control"]/div/span/button'):
            #print("Element exists")
            pass

        ## Sorting Box
        #self.select_sorting(driver)
        #sleep(2)
        #self.page_loading_completed(driver)
        
        ## 가끔 툴팁이 띄어서 검색을 방해한다. 따라서 툴팁을 닫는다.
        try:
            if driver.find_element('xpath','//div[@class="srp-save-search__tooltip srp-save-search__tooltip--shown"]'):
                print("Tooltip Element exists")
                sleep(2)
                tooltip = driver.find_element('xpath','//div[@class="srp-save-search__tooltip srp-save-search__tooltip--shown"]/button')
                tooltip.click()
        except NoSuchElementException:
            pass

 
        ## HTML 페이지 저장
        with open('page.txt', 'w', encoding='utf-8') as f:
            f.write(self.driver.page_source)
        
        ## itemID 찾기
        log.debug('>>> Search ItemID...')
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        klist = self.get_itemid(soup, keyword, itemIDList)
        
        ## click to new tab
        """
        item_url = 'https://www.ebay.com/itm/' + '224672009642'
        link = driver.find_element_by_css_selector('a[href^="' + item_url + '"]')
        if link:
            print("ok exists")
            self.get_position_leftTop(link)
 
            driver.execute_script("arguments[0].scrollIntoView();", link)
            self.get_position_leftTop(link)
            
            link2 = driver.find_elements_by_css_selector('a[href^="' + item_url + '"]')[1]
            print(link2.get_attribute('outerHTML'))
            print(link2.is_enabled())
            print(link2.is_displayed())
            #element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href^="https://www.ebay.com/itm/284404370220"]')))
            #element.click()
            input('?')
            #ActionChains(driver).move_to_element(link).context_click(link).send_keys("t").perform()
            #ActionChains(driver).move_to_element(link2).click().perform()
            link2.click()
        """
        self.click_itemid(driver, itemIDList)
        for w in driver.window_handles:
            if w != main_window:
                #print('close window:',w)
                driver.switch_to.window(w)
                driver.close()
                sleep(1)


        driver.switch_to.window(main_window)
        #log.info('Successfully Completed!!!')
        
        return klist
        
        

    def get_itemid(self, soup, keyword, myitems):
        """
            HTML 파일로부터 item_id을 가져온다.
        """
        
        item = []
        klist = []
        root  = soup.find('ul', class_="srp-results")
        items = root.find_all("div", {"class": "s-item__image-section"})
        for i, itm in enumerate(items, start=1):
            try:
              href = itm.find('a').get('href')
              item.append(href)
            except Exception as e:
              pass

        #item = [ m.find('a').get('href') for m in root.find_all("div", {"class": "s-item__image-section"}) ]
        #print(item ,len(item))

        f = open('item.txt','a',encoding='utf-8')
        for i, id in enumerate(item, start=1):
            itno = re.search('https://www.ebay.com/itm/(\d+)\?', id)
            
            for mi in myitems:    		
                if itno.group(1) == mi:
                    log.info('Rank: {}\t{}\t({})'.format(keyword, mi, i))
                    klist.append([keyword, mi, i])
                    sleep(1)
                #else:
                #	log.debug('{} {}'.format(i, itno.group(1)))
        f.close()
        
        return klist

        
    def click_itemid(self, driver, myitems):
        """
            선택된 item_id을 새탭에 연다.
        """

        main_window = driver.window_handles[0]
        for id in myitems:
            item_url = 'https://www.ebay.com/itm/' + id
            print(item_url)
            try:
                link = driver.find_element('css selector','a[href^="' + item_url + '"]')
            
                if link.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView();", link)
                    #input('scrollIntoView?')
                    link2 = driver.find_elements('css selector','a[href^="' + item_url + '"]')[1]
                    link2.send_keys('')
                    #input('select?')
                    link2.click()
                    #print('wait 3 seconds...')
                    sleep(3)
            
            except Exception as e:
                log.error('%s %s' % (sys.exc_info()[0], sys.exc_info()[1]) )
                
            sleep(random.randint(3, 9))



    def select_sorting(self, driver):
        """
            Select Sorting Box :: Price+Shipping lowest first(4), Best Match(1)
        """
        
        log.debug(">>> Sort Select Box로 이동")
        sleep(2)
        sort_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@class="srp-controls__sort srp-controls__control"]/div/span/button')))
        action = ActionChains(driver)
        self.human_like_mouse_move(action, sort_box)
        sort_box.click()
        input('?')
        sleep(2)
        log.debug('>>> 200 선택')
        sleep(2)
        item_200 = driver.find_element('xpath','//div[@class="srp-controls__sort srp-controls__control"]/div/span/span/ul/li[4]/a')
        ActionChains(driver).move_to_element(item_200).click().perform()


        


if __name__ == "__main__":

    log.info('===== 프로그램 시작 : Get itemID =====')

    parser = argparse.ArgumentParser(description='eBay item ID 가져오기')
    parser.add_argument('user_id', help='가져오고 싶은 User ID')
    #parser.add_argument('-p','--page', help='start page: 시작할 페이지를 지정하는 경우')    
    parser.add_argument('page', nargs='?', default=1, help='start page: 시작할 페이지를 지정하는 경우')
    #parser.add_argument('-d','--date', help='DART 데이타를 가져오고 싶은 날짜')
    args = parser.parse_args()

    www = myClass()
    url = 'https://www.ebay.com/'
    www.run(url, args.user_id, int(args.page))
    
    # 파일을 이용한 HTML 파일 파싱(테스트)
    """
    myitem = '115070184414'
    file_name = 'page.txt'
    soup = BeautifulSoup(open(file_name, encoding="utf-8"), "html.parser")
    root = soup.find('ul', class_="srp-results")
    item = [ m.find('a').get('href') for m in root.find_all("div", {"class": "s-item__image-section"}) ]
    print(item ,len(item))
    f = open('link.txt', 'a', encoding='utf-8')
    for i, id in enumerate(item, start=1):
        f.write(str(id) + '\n')
        m = re.search('https://www.ebay.com/itm/(\d+)\?', id)
        print(i, m.group(1))
        if m.group(1) == myitem:
            print('MATCH:', i, id)
    f.close()
    """
    
    

