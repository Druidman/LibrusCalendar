from getTimeTable import Scraper
from parseTimeTable import Parser
from selenium import webdriver

driver = webdriver.Chrome()
scraper = Scraper(driver=driver)
documentRAW = scraper.scrape()

parser = Parser(documentRAW=documentRAW)
lessonData = parser.parseDocument()
print(lessonData)