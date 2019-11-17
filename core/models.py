from django.db import models
from datetime import datetime

class Event(models.Model):
    summary = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.summary


class Attendee(models.Model):
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.email
