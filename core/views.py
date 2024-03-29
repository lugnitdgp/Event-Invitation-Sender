from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from core.forms import EventForm
from core.models import Event, Attendee
from core.tasks import send_invitations_in_background
import datetime
import pytz


def index(request):
    if not request.user.is_authenticated:
        return HttpResponse('Please login as admin to use the app.')
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid:
            event = Event(
                summary = request.POST['summary'],
                description = request.POST['description'],
                location = request.POST['location'],
                starttime = request.POST['starttime'],
                endtime = request.POST['endtime']
            )
            event.save()
            event_id = event.id
            attendees = Attendee.objects.all()
            send_invitations_in_background.delay({
                'summary': request.POST['summary'],
                'description': request.POST['description'],
                'location': request.POST['location'],
                'attendees': [attendee.email for attendee in attendees],
                'starttime': request.POST['starttime'] + ':00',
                'endtime': request.POST['endtime'] + ':00'
            }, event_id)
            messages.info(request, 'Invitations will be sent shortly.')
        else:
            messages.info(request, 'Something went wrong !')
    return render(request, 'core/index.html')
