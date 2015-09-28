from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):

    submitting_user = models.ForeignKey(User)
    comment = models.TextField()
    page = models.CharField(max_length=500)

    def __unicode__(self):
        return "Comment " + str(self.id) + " by " + self.submitting_user.first_name + " on " + self.page
