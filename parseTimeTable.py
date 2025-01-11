import json
from bs4 import BeautifulSoup
import re
    
class Parser():
    def __init__(self,documentRAW):
        self.document = self.formatDocument(documentRAW)
        self.dayData = [
            {
                "poniedziałek": {
                    "start": None,
                    "end": None
                }
            },
            {
                "wtorek": {
                    "start": None,
                    "end": None
                }
            },
            {
                "środa": {
                    "start": None,
                    "end": None
                }
            },
            {
                "czwartek": {
                    "start": None,
                    "end": None
                }
            },
            {
                "piątek": {
                    "start": None,
                    "end": None
                }
            }
        ]
    def saveToFile(self):
        saveReady = json.dumps(self.dayData,indent=2)
        with open("lessonData.json","w") as file:
            file.write(saveReady)
    
    def formatDocument(self,documentRAW):
        scriptTags = re.findall(r"(<script.*?>.*?</script>)", documentRAW, re.DOTALL)
        for tag in scriptTags:
            documentRAW = documentRAW.replace(tag,"")

        return BeautifulSoup(documentRAW,"html.parser")

    def assingStartEndTime(self,day,dayName,lessonStartTime,lessonEndTime):
        day[dayName]["end"] = lessonEndTime

        if day[dayName]["start"]:
            return
        
        day[dayName]["start"] = lessonStartTime

    def getLessonRows(self):
        form = self.document.find(attrs={"name": "formPrzegladajPlan"})
        timeTable = form.find(class_="plan-lekcji")
        lessonRows = timeTable.tbody.find_all("tr",class_="line1")
        return lessonRows
    
    def parseLesson(self,lesson,day,lessonStartTime,lessonEndTime):
        lessonDescBox = lesson.find_all("div",class_="text")
        lessonInfoBox = lesson.find_all("div",attrs={"class":"plan-lekcji-info"})
        if not lessonDescBox:
            return
        
        
        dayName = next(iter(day))

        if not lessonInfoBox:
            self.assingStartEndTime(
                day=day,
                dayName=dayName,
                lessonStartTime=lessonStartTime,
                lessonEndTime=lessonEndTime
            )
            return
        
        lessonDescBox = lessonDescBox[-1]
        lessonInfoBox = lessonInfoBox[-1]
        info = lessonInfoBox.text.strip()

        if info == "dzień wolny szkoły": 
            return
        elif info == "odwołane": 
            return
        elif info == "przesunięcie":
            if lessonDescBox.parent.name == "s": 
                return

        self.assingStartEndTime(
            day=day,
            dayName=dayName,
            lessonStartTime=lessonStartTime,
            lessonEndTime=lessonEndTime
        )

    def parseLessonRow(self,lessonRow):
        lessonStartTime = lessonRow.find("td",attrs={"id": "timetableEntryBox"})["data-time_from"]
        lessonEndTime = lessonRow.find("td",attrs={"id": "timetableEntryBox"})["data-time_to"]
        lessons = lessonRow.find_all("td",class_="line1",attrs={"id": "timetableEntryBox"})
        for lesson,day in zip(lessons,self.dayData):
            self.parseLesson(
                lesson=lesson,
                day=day,
                lessonStartTime=lessonStartTime,
                lessonEndTime=lessonEndTime
            )
                  
    def parseDocument(self):
        lessonRows = self.getLessonRows()
        for lessonRow in lessonRows:
            self.parseLessonRow(lessonRow)
        self.saveToFile()
        return self.dayData
            
            










