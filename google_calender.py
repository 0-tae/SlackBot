from flask import Flask, request, make_response
import requests
from slackbot_info import json_prettier
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import calendar as module_calendar
import os.path
import pytz
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
SEOUL_TIMEZONE = pytz.timezone('Asia/Seoul')


class GoogleCalendarAPI:
  creds = None
  instance = None

  def __init__(self):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not self.creds or not self.creds.valid:
      if self.creds and self.creds.expired and self.creds.refresh_token:
        self.creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        self.creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(self.creds.to_json())
    
    self.instance = build("calendar", "v3", credentials=self.creds)

  # 캘린더에서 일정을 삭제(shortcut), 우선순위 나중

  # 캘린더에 일정이 등록 되면, 슬랙봇에 출력 -> app.py

  # 캘린더에서 일정을 받아온 후 슬랙봇에 출력 -> app.py

  # 캘린더에서 일정 수정

  # 캘린더에 일정 등록
  # event_request = Dict {summary, start, end, all-day}
  def insert_event(self, event_request):
    body = self.event_request_convert(event_request = event_request)
    events_result = (
        self.instance.events()
        .insert(
            calendarId="primary",
            body=body
        )
        .execute()
    )

    print(prettier(events_result))

    return events_result
  
  # event_request를 API 규격에 맞는 body로 변환
  def event_request_convert(self,event_request):
    body = {
        'summary': event_request['summary'], # 일정 제목
        'location': None, # 일정 장소
        'description': event_request['description'], # 일정 설명
        'start': { # 시작 날짜
              'dateTime': event_request['start'].isoformat(),
              'timeZone': 'Asia/Seoul'
        },
        'end': { # 종료 날짜
            'dateTime': event_request['end'].isoformat(),
            'timeZone': 'Asia/Seoul'
        }
    }

    # 상세 시간 일정일 때, datetime 객체를 date_str 형식으로 변환
    if event_request['all-day']:
      body['start'] = {"date" : event_request['start'].date().strftime("%Y-%m-%d")}
      body['end'] = {"date" : event_request['end'].date().strftime("%Y-%m-%d")}

    return body

  # 캘린더에 휴가 등록
  # 연차(day_off), 시간연차(part_day_off), 반차(half_day).. 굳이 영문 매핑을 해야 할까?
  def insert_vacation(self, event_request):

    # 반차는 시작 시간대를 확인하고 오전인지, 오후인지 분석
    if event_request["vacation"] == "반차":
        event_request["vacation"] = \
          "오전반차" if self.is_AM_range(event_request["start"]["date"]) else "오후반차"
   
    # 시간연차, 연차일 경우는 달리 작업할 것 없음
    return self.insert_event(event_request = event_request)
  
  # 오전 오후 시간분석
  def is_AM_range(time : datetime):
    am_start_time = 9
    pm_start_time = 12
    return am_start_time < time.hour < pm_start_time

  # 캘린더에서 휴가 받아오기
  # 일정에서 휴가만 필터링 하는 방식
  # option : 일별, 월별
  def get_vacation_list(self, option):
    return list(filter(lambda e: "연차" or "반차" in e["summary"] , self.get_event_list(option=option)))
    
  # 캘린더에서 일정 받아오기
  # option : 일별, 월별
  def get_event_list(self, option):
    now = datetime.now(SEOUL_TIMEZONE)    

    # "month" 옵션일 때, 해당 월의 스케줄을 가져옴
    # "week" 옵션일 때,  당월에 해당하는 한 주차 스케줄을 가져옴 (좀 복잡함)
    # "today" 옵션일 때, 금일의 스케줄을 가져옴(default)

    time_min = now
    time_max = datetime(year=time_min.year, month=time_min.month, day=time_min.day+1).astimezone(SEOUL_TIMEZONE)

    if option == "month":
      last_day_of_month = module_calendar.monthrange(now.year, now.month)[1]
      time_max = datetime(now.year, now.month, last_day_of_month).astimezone(SEOUL_TIMEZONE)

    print("TIMEMAX",time_max)
    print("TIMEMIN",time_min)

    events_result = (
        self.instance.events()
        .list(
            calendarId="primary",
            timeMin=time_min.isoformat(),
            timeMax=time_max.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return
  
    event_list = []

    for event in events:
      print(json_prettier(event))
      event_info = {"start":event["start"]["dateTime"], "summary":event["summary"]}
      
      event_list.append(event_info)


    return list(map(lambda event : self.make_response(event), event_list))
  




  def make_response(event):
    response = {
      "summary" : event["summary"],
      "start" : event["start"]["dateTime"],
      "end" : event["end"]["dateTime"],
      "creator" : event["creator"]["email"],
      "created" : event["created"],
      "updated" : event["updated"]
    }

    return response



calendar = GoogleCalendarAPI()

event_list = calendar.get_event_list(option="today")

# time_to_add = timedelta(days= 2,hours = 2, minutes = 30)
# now = datetime.now(SEOUL_TIMEZONE)

# # Required : summary, start, end, description, vacation, allday
# event_request = {"summary" : "수도공사", "start" : now, "end" : now, "description" : None, "vacation": "연차", "all-day":True}
# calendar.insert_event(event_request=event_request)
# [END calendar_quickstart]