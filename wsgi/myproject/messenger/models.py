from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from time import strftime
# Create your models here.

class InternalMessage(models.Model):

    sender = models.ForeignKey(User, related_name='sender')
    recipient = models.ManyToManyField(User, related_name = 'recipient')
    title = models.CharField(max_length=500)
    body = models.TextField()
    timestamp = models.DateTimeField('timestamp', default=timezone.now())
    read = models.BooleanField(default=False)

    def __unicode__(self):

        recipient_list = ""
        for r in self.recipient.all():
            recipient_list += r.username + '; '

        recipient_list = recipient_list[:-2]

        nice_time = self.timestamp.strftime("%H:%M %d %b %Y")

        return self.title + ' (' + 'Message from ' + self.sender.username + ' to ' + recipient_list + ' at ' + nice_time + ')'
