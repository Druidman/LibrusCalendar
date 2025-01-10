from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

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
loginInput.send_keys("")
time.sleep(1)
passwordInput.send_keys("")
time.sleep(1)

sendLogDataButton = driver.find_element(By.XPATH,"//button[@id='LoginBtn']")
sendLogDataButton.click()
time.sleep(1)
driver.close()
