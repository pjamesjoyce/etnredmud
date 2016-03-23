from django.db import models
from time import time

# Create your models here.

def get_upload_file_name(instance, filename):
    print  "%s_%s" % (str(time()).replace('.','_'), filename)
    return "%s_%s" % (str(time()).replace('.','_'), filename)

class DataImport(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    data_file = models.FileField(upload_to=get_upload_file_name, blank =True)

    def __unicode__(self):
        return "Data import %s" % self.timestamp.strftime("%H:%M  %B %d, %Y")

    def get_data_file(self):
		data_file = str(self.data_file)
		return data_file
