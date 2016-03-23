from .models import DataImport
from django import forms #import the forms framework

class DataUploadForm(forms.ModelForm):

    class Meta:
        model = DataImport
        exclude= ['timestamp']
        
