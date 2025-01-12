import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def getEvents(service,calendarId,personName):
    allEvents = service.events().list(
        calendarId=calendarId
    ).execute().get("items")
    eventIds = []
    for event in allEvents:
        description = event.get("description",None)
  
        if not description:
            continue
        if description.lower() == f"botentry{personName.lower()}":
            eventIds.append(event["id"])
    return eventIds


  

def nextYearDate():
  fastForwardYear = datetime.datetime(
    datetime.datetime.now().year + 1,
    datetime.datetime.now().month,
    datetime.datetime.now().day
  ).isoformat().replace("-","").replace(":","") + "Z"
  return fastForwardYear

def chooseCalendar(service):
  calendars = service.calendarList().list().execute()["items"]
  num = 0
  
  for calendar in calendars:
    num+=1
    print(f'{num}. {calendar["summary"]},')
    
  result = int(input(f"\nChoose calendar (type number {1}-{num}): "))
  if not result:
    return 
  return calendars[result - 1]["id"]
  
def googleOAuth():
  creds = None
  
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds

def loadLessonData(personName):
  with open(f"{personName}lessonData.json","r") as file:
    data = json.load(file)
  return data

def updateEvents(service,data,personName,calendarId):
  eventIds = getEvents(service,calendarId=calendarId,personName=personName)

  print(eventIds)
  for day in data:
    dayName = next(iter(day))
    date = day[dayName]["date"]
    startTime = day[dayName]["start"]
    endTime = day[dayName]["end"]
    if not startTime or not endTime:
      continue

    startDateTime = f"{date}T{startTime}:00.0Z"
    endDateTime = f"{date}T{endTime}:00.0Z"
    
    fastForwardYear = nextYearDate()
    
    event = service.events().insert(
      calendarId=calendarId,
      body={
        "summary": f"{personName} w szkole",
        "start": {
          "dateTime": startDateTime,
          "timeZone": "Europe/Warsaw"
        },
        "end": {
          "dateTime": endDateTime,
          "timeZone": "Europe/Warsaw"
        },
        'recurrence': [
          f'RRULE:FREQ=WEEKLY;UNTIL={fastForwardYear}'
        ],
        "description": f"BotEntry{personName}"
      }
      
    ).execute()
    break

def main():
  creds = googleOAuth()
  try:
    service = build("calendar", "v3", credentials=creds)
    calendarId = chooseCalendar(
      service=service
    )
    if not calendarId:
      return
    personName = "Mateusz"
    data = loadLessonData(personName=personName)
    
    updateEvents(
      service=service,
      data=data,
      calendarId=calendarId,
      personName=personName
  
    )
  except HttpError as error:
    print(f"An error occurred: {error}")

main()
