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
lessons = timeTable.tbody.find_all("tr",class_="line1")


firstlessonStart = lessons[0].find("td",class_="line1")["data-time_from"]
print(firstlessonStart)


