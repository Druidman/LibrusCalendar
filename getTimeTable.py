from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class Scraper():
    def __init__(self,driver,login,password,weeksToScrape):
        
        self.LOGIN: str = login
        self.PASSWORD: str = password
        self.WEEKS_TO_SCRAPE: str = weeksToScrape
        self.driver: webdriver.Chrome = driver

        self.PAGELINK = "https://portal.librus.pl/rodzina"

    def clickButton(self,xpath: str):
        button = self.driver.find_element(By.XPATH,xpath)
        button.click()
        time.sleep(1)
        

    def fillInputTag(self,data,xpath):
        inputTag = self.driver.find_element(By.XPATH,xpath)
        inputTag.send_keys(data)
        time.sleep(1) 

    def scrape(self) -> list:
        self.driver.get(self.PAGELINK)
        
        acceptButton = '//div[@id="consent-categories-description"]//button[@class="modal-button__primary"]'
        self.clickButton(acceptButton)

        dropDown = '//*[@id="dropdownTopRightMenuButton"]'
        self.clickButton(dropDown)

        loginPageButton = '//*[@id="dropdownSynergiaMenu"]/a[2]'
        self.clickButton(loginPageButton)


        self.driver.switch_to.frame("caLoginIframe")


        loginInput = '//input[@id="Login"]'
        self.fillInputTag(self.LOGIN,loginInput)

        passwordInput = '//input[@id="Pass"]'
        self.fillInputTag(self.PASSWORD,passwordInput)
       

        loginButton = "//button[@id='LoginBtn']"
        self.clickButton(loginButton)


        self.driver.switch_to.parent_frame()
        time.sleep(7)


        selectButton = '//div[@id="main-menu"]/ul/li[7]/a'
        self.clickButton(selectButton)
        

        timetableButton = '//div[@id="main-menu"]/ul/li[7]/ul/li[1]/a'
        self.clickButton(timetableButton)


        for window in self.driver.window_handles:
            self.driver.switch_to.window(window)
        # driver switches to windows first window in default one so last one is the opened timetable one  
        pageHTMLs = []
        for i in range(0,self.WEEKS_TO_SCRAPE):
            
            pageHTMLs.append(self.driver.page_source)
            self.clickButton("/html/body/div[1]/div/div/div/form/table[1]/tbody/tr[1]/th/a[2]")
            time.sleep(7)
        self.driver.close()
        return pageHTMLs
        












