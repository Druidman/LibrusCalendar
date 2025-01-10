from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv
load_dotenv()


class Scraper():
    def __init__(self,driver):
        self.LOGIN: str = os.getenv("LOGIN")
        self.PASSWORD: str = os.getenv("PASSWORD")
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
    def saveHtmlToFile(self):
        with open("lessons.html","w") as file:
            file.write(self.driver.page_source)
            file.close()

    def scrape(self):
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
        # driver switches to windows first window in defaultt one so last one is the opened timetable one 
        self.saveHtmlToFile()   
        self.driver.close()












