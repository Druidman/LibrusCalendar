from getTimeTable import Scraper
from selenium import webdriver

driver = webdriver.Chrome()
scraper = Scraper(driver=driver)
scraper.scrape()