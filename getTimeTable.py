from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class Scraper:
    def __init__(self, driver, login, password, weeksToScrape):
        self.LOGIN: str = login
        self.PASSWORD: str = password
        self.WEEKS_TO_SCRAPE: str = weeksToScrape
        self.driver: webdriver.Chrome = driver

        self.PAGELINK = "https://portal.librus.pl/rodzina"
        self.wait = WebDriverWait(driver=driver, timeout=10)

    def clickButton(self, xpath: str, errorName: str | None = None):
        try:
            button = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            button.click()
            time.sleep(1)

        except Exception as e:
            print(f"EXCEPTION OCCURED IN [CLICKING] ELEMENT [{errorName if errorName != None else 'unknown'}]: {xpath}")
            if input("print exception?"):
                print(e)
            os.exit()
            return

    def fillInputTag(self, data, xpath):
        try:
            inputTag = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            inputTag.send_keys(data)

        except Exception as e:
            print(f"EXCEPTION OCCURED IN [filling]  ELEMENT: {xpath}")
            if input("print exception?"):
                print(e)
            os.exit()
            return

    def scrape(self) -> list:
        self.driver.get(self.PAGELINK)

        acceptButton = '//div[@id="consent-categories-description"]//button[@class="modal-button__primary"]'
        self.clickButton(acceptButton, 'acceptCookies')

        loginDropDown = "/html/body/nav/div/div[1]/div/div[2]/a[3]"
        self.clickButton(loginDropDown, 'loginDropDown')

        loginPageButton = "/html/body/nav/div/div[1]/div/div[2]/div/a[2]"
        self.clickButton(loginPageButton, 'loginPageButton')

        self.driver.switch_to.frame("caLoginIframe")

        loginInput = '//input[@id="Login"]'
        self.fillInputTag(self.LOGIN, loginInput)

        passwordInput = '//input[@id="Pass"]'
        self.fillInputTag(self.PASSWORD, passwordInput)

        loginButton = "//button[@id='LoginBtn']"
        self.clickButton(loginButton, 'loginButton')
        self.driver.save_screenshot("idk.png")

        self.driver.switch_to.parent_frame()
        time.sleep(7)


        print("Idk")
        selectButton = '/html/body/div[3]/div[1]/div[1]/div/div/ul/li[7]/a'
        self.clickButton(selectButton , 'selectButton')

        timetableButton = '/html/body/div[3]/div[1]/div[1]/div/div/ul/li[7]/ul/li[1]/a'
        self.clickButton(timetableButton, 'timetableButton')

        for window in self.driver.window_handles:
            self.driver.switch_to.window(window)
        # driver switches to windows first window in default one so last one is the opened timetable one
        pageHTMLs = []
        for i in range(0, self.WEEKS_TO_SCRAPE):
            pageHTMLs.append(self.driver.page_source)
            self.clickButton(
                "/html/body/div[1]/div/div/div/form/table[1]/tbody/tr[1]/th/a[2]",
                'timetableNextWeekbutton'
            )
            time.sleep(7)
        self.driver.close()
        return pageHTMLs
