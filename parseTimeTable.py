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
        if lesson.find("div",class_="text"):
            dayName = next(iter(day))
            day[dayName]["end"] = lessonEndTime
            if day[dayName]["start"]:
                continue
            day[dayName]["start"] = lessonStartTime


print(dayData)







