from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class InternalMessage(models.Model):

    sender = models.ForeignKey(User, related_name='sender')
    recipient = models.ForeignKey(User, related_name = 'recipient')
    title = models.CharField(max_length=500)
    body = models.TextField()
    timestamp = models.DateTimeField('timestamp', default=timezone.now())
    read = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Message from ' + self.sender.username + ' to ' + self.recipient.username + ' at ' + str(self.timestamp)
