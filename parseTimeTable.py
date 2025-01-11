import json
from bs4 import BeautifulSoup
import re
"""
data = {
    "poniedziałek": {
        "start": ,
        "end":
    },

}
"""


with open("lessons.html","r") as file:
    documentRAW: str = file.read() 
    
    scriptTags = re.findall(r"(<script.*?>.*?</script>)", documentRAW, re.DOTALL)
    for tag in scriptTags:

        documentRAW = documentRAW.replace(tag,"")

    
    

document = BeautifulSoup(documentRAW,"html.parser")

form = document.find(attrs={"name": "formPrzegladajPlan"})

timeTable = form.find(class_="plan-lekcji")
lessonRows = timeTable.tbody.find_all("tr",class_="line1")

dayData = [
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

for lessonRow in lessonRows:
    lessonNum = int(lessonRow.find("td").text)
    lessonStartTime = lessonRow.find("td",attrs={"id": "timetableEntryBox"})["data-time_from"]
    lessonEndTime = lessonRow.find("td",attrs={"id": "timetableEntryBox"})["data-time_to"]

    lessons = lessonRow.find_all("td",class_="line1",attrs={"id": "timetableEntryBox"})
    for lesson,day in zip(lessons,dayData):

        for toolTipInfoBox in lesson.select(".tooltip"):
            toolTipInfoBox.extract()

        lessonDescBox = lesson.find_all("div",class_="text")
        
        lessonInfoBox = lesson.find("div",attrs={"class":"plan-lekcji-info"})
        if not lessonDescBox:
            continue
        lessonDescBox = lessonDescBox[-1]
        
        dayName = next(iter(day))
        if not lessonInfoBox:
            day[dayName]["end"] = lessonEndTime
            if day[dayName]["start"]:
                continue
            day[dayName]["start"] = lessonStartTime
            continue
        info = lessonInfoBox.text.strip()

        if info == "dzień wolny szkoły": 
            continue
        elif info == "odwołane": 
            continue
        elif info == "przesunięcie":
            if lessonDescBox.parent.name == "s": 
                continue

        day[dayName]["end"] = lessonEndTime
        if day[dayName]["start"]:
            continue
        day[dayName]["start"] = lessonStartTime


print(dayData)







