from __future__ import absolute_import, unicode_literals, print_function
import datetime
import pickle
import os
from django.conf import settings
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from yaml import load, dump
from celery import shared_task
from core.models import Event
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def prepare_event_body(data):
    attendees = data['attendees']
    attendees_list = list()
    for email in attendees:
        attendees_list.append({'email': email})
    event = {
        'summary': data['summary'],
        'location': data['location'],
        'description': data['description'],
        'start': {
            'dateTime': data['starttime'],
            'timeZone': 'Asia/Kolkata'
        },
        'end': {
            'dateTime': data['endtime'],
            'timeZone': 'Asia/Kolkata'
        },
        'attendees': attendees_list,
    }
    return event

def authorize_and_prepare_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = settings.GOOGLE_API_SERVICE_ACCOUNT_FILE
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    return service

@shared_task
def send_invitations_in_background(data, event_id):
    service = authorize_and_prepare_service()
    service.events().insert(
        calendarId='primary', 
        body=prepare_event_body(data),
        sendNotifications=True
    ).execute()
    event = Event.objects.get(id=event_id)
    event.sent = True
    event.save()
