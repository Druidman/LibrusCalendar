import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class Calendar:
    def __init__(self):
        creds = self.googleOAuth()
        self.service = self.buildCalendarService(creds=creds)
        self.calendarId = None
        self.personName = None

    def getEvents(self, date):
        events = (
            self.service.events()
            .list(
                calendarId=self.calendarId,
                q=f"BotEntry{self.personName}",
                timeMin=f"{date}T00:00:00Z",
                timeMax=f"{date}T23:59:59Z",
                timeZone="Europe/Warsaw",
            )
            .execute()
            .get("items")
        )

        return events

    def setCalendar(self) -> str:
        calendars = self.service.calendarList().list().execute()["items"]

        num = 0

        for calendar in calendars:
            num += 1
            print(f"{num}. {calendar['summary']},")

        result = int(input(f"\nChoose calendar (type number {1}-{num}): "))
        if not result:
            return
        self.calendarId = calendars[result - 1]["id"]
        return calendars[result - 1]["id"]

    def googleOAuth(self):
        creds = None
        tokenPath = os.path.join(os.getcwd(), "token.json")
        credsPath = os.path.join(os.getcwd(), "credentials.json")
        if os.path.exists(tokenPath):
            creds = Credentials.from_authorized_user_file(tokenPath, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(credsPath, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(tokenPath, "w") as token:
                token.write(creds.to_json())
        return creds

    def upsertEvents(self, data):
        print("update for")
        for day in data:
            dayName = next(iter(day))
            date = day[dayName]["date"]
            startTime = day[dayName]["start"]
            endTime = day[dayName]["end"]

            startDateTime = f"{date}T{startTime}:00"
            endDateTime = f"{date}T{endTime}:00"

            inSchoolBody = {
                "summary": f"{self.personName} w szkole",
                "start": {"dateTime": startDateTime, "timeZone": "Europe/Warsaw"},
                "end": {"dateTime": endDateTime, "timeZone": "Europe/Warsaw"},
                "colorId": "5",
                "description": f"BotEntry{self.personName}",
            }

            notInSchoolBody = {
                "summary": f"{self.personName} w Domu",
                "start": {"dateTime": f"{date}T00:00:01", "timeZone": "Europe/Warsaw"},
                "end": {"dateTime": f"{date}T23:59:59", "timeZone": "Europe/Warsaw"},
                "colorId": "10",
                "description": f"BotEntry{self.personName}",
            }

            events = self.getEvents(date=date)

            if events:
                if not startTime or not endTime:
                    eventId = events[0]["id"]
                    res = (
                        self.service.events()
                        .delete(calendarId=self.calendarId, eventId=eventId)
                        .execute()
                    )

                    print(f"delete event {eventId}")
                else:
                    res = (
                        self.service.events()
                        .update(
                            calendarId=self.calendarId,
                            eventId=events[0]["id"],
                            body=inSchoolBody,
                        )
                        .execute()
                    )
                    print(f"update event {res['summary']} {res['start']['dateTime']}")
            else:
                if startTime and endTime:
                    self.insertEvent(body=inSchoolBody)

    def loadLessonData(self) -> dict:
        with open(f"{self.personName}LessonData.json", "r") as file:
            data = json.load(file)
        return data

    def buildCalendarService(self, creds):
        return build("calendar", "v3", credentials=creds)

    def insertToCalendar(self, lessonData):
        try:
            if lessonData:
                data = lessonData
            else:
                data = self.loadLessonData()

            self.upsertEvents(data=data)
        except HttpError as error:
            print(f"An error occurred: {error}")

    def insertEvent(self, body: str) -> bool:
        res = (
            self.service.events()
            .insert(calendarId=self.calendarId, body=body)
            .execute()
        )
        if not res:
            print(f"ERROR inserting event")
            return False

        print(f"SUCCES insert event {res['summary']} {res['start']['dateTime']}")
        return True
