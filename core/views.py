from django.shortcuts import render
from django.contrib import messages
from core.forms import EventForm
from core.models import Event, Attendee
from core.tasks import send_invitations_in_background
import datetime
import pytz


def index(request):
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
            attendees = Attendee.objects.all()
            send_invitations_in_background.delay({
                'summary': request.POST['summary'],
                'description': request.POST['description'],
                'location': request.POST['location'],
                'attendees': [attendee.email for attendee in attendees],
                'starttime': request.POST['starttime'] + ':00',
                'endtime': request.POST['endtime'] + ':00'
            })  
            messages.info(request, 'Invitations will be sent shortly.')
        else:
            messages.info(request, 'Something went wrong !')
    return render(request, 'core/index.html')
