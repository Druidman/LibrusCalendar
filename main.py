from getTimeTable import Scraper
from parseTimeTable import Parser
from selenium import webdriver

driver = webdriver.Chrome()
scraper = Scraper(driver=driver)
scraper.scrape()

with open("lessons.html","r") as file:
    documentRAW: str = file.read() 

parser = Parser(documentRAW=documentRAW)
parser.parseDocument()