from selenium import webdriver
from selenium.webdriver.common.by import By

import time

import os
from dotenv import load_dotenv
load_dotenv()
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")



options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome()
driver.get("https://portal.librus.pl/rodzina")



acceptButton = driver.find_element(By.XPATH,'''//div[@id="consent-categories-description"]//button[@class="modal-button__primary"]''')

acceptButton.click()
time.sleep(1)


dropButton = driver.find_element(By.XPATH,'//*[@id="dropdownTopRightMenuButton"]')
dropButton.click()
time.sleep(1)

logButton = driver.find_element(By.XPATH,'//*[@id="dropdownSynergiaMenu"]/a[2]')
logButton.click()



driver.switch_to.frame("caLoginIframe")
loginInput = driver.find_element(By.XPATH,'//input[@id="Login"]')
passwordInput = driver.find_element(By.XPATH,'//input[@id="Pass"]')
loginInput.send_keys(LOGIN)
time.sleep(1)
passwordInput.send_keys(PASSWORD)
time.sleep(1)

sendLogDataButton = driver.find_element(By.XPATH,"//button[@id='LoginBtn']")
sendLogDataButton.click()

driver.switch_to.parent_frame()

time.sleep(7)

selectButton = driver.find_element(By.XPATH,'//div[@id="main-menu"]/ul/li[7]/a')
selectButton.click()
time.sleep(1)
plan = driver.find_element(By.XPATH,'//div[@id="main-menu"]/ul/li[7]/ul/li[1]/a')
plan.click()


for window in driver.window_handles:
    driver.switch_to.window(window)
# driver switches to windows first window in defaultt one so last one is the opened timetable one    
with open("lessons.html","w") as file:
    file.write(driver.page_source)
    file.close()
driver.close()

