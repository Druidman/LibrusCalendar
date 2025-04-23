from getTimeTable import Scraper
from parseTimeTable import Parser
from insertIntoCalendar import Calendar
from selenium import webdriver

from selenium.webdriver.chrome.options import Options


import os, json

def setupAppData():
    data = None
    scraperDataFilePath = os.path.join(os.getcwd(),"scraperWorkingData.json")
    if os.path.exists(scraperDataFilePath):
        data = json.load(open(scraperDataFilePath,"r"))

    if not data:
        personName = str(input("Name: "))
        librus_login = str(input("librus login: "))
        librus_password = str(input("librus password: "))
        calendarId = calendar.setCalendar()
        weeksToScrape = 0
        while weeksToScrape <= 0:
            weeksToScrape = int(input("weeks to scrape: "))
        data = {
            "personName": personName,
            "calendarId": calendarId,
            "weeksToScrape": weeksToScrape,
            "librusLogin": librus_login,
            "librusPassword": librus_password
        }
        with open(scraperDataFilePath,"w") as file:
            dataToSave = json.dumps(data,indent=2)
            file.write(dataToSave)
            file.close()

    
    return data

calendar = Calendar()

appData = setupAppData()
calendar.personName = appData["personName"]
calendar.calendarId = appData["calendarId"]
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--mute-audio")
# chrome_options.add_argument("--headless=new")


driver = webdriver.Chrome(options=chrome_options)
scraper = Scraper(
    driver=driver,
    login=appData["librusLogin"],
    password=appData["librusPassword"],
    weeksToScrape=appData["weeksToScrape"]
)

documentsRAW = scraper.scrape()
for documentRAW in documentsRAW:
    parser = Parser(documentRAW=documentRAW,personName=appData["personName"])
    lessonData = parser.parseDocument()
    calendar.insertToCalendar(lessonData=lessonData)
        