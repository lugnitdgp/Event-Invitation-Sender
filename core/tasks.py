from __future__ import absolute_import, unicode_literals, print_function
import datetime
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from yaml import load, dump
from celery import shared_task
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


SCOPES = ['https://www.googleapis.com/auth/calendar']

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
    token = os.path.join(os.environ['HOME'], 'Desktop/inviter_files/token.pickle')
    creds = None
    if os.path.exists(token):
        with open(token, 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    return service

@shared_task
def send_invitations_in_background(data):
    service = authorize_and_prepare_service()
    service.events().insert(
        calendarId='primary', 
        body=prepare_event_body(data),
        sendNotifications=True
    ).execute()
