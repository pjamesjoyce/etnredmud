from .models import BibDataImport
from django import forms #import the forms framework

class BibDataUploadForm(forms.ModelForm):

    class Meta:
        model = BibDataImport
        exclude= ['timestamp']
        
