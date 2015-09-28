from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):

    submitting_user = models.ForeignKey(User)
    comment = models.TextField()
    page = models.CharField(max_length=500)
