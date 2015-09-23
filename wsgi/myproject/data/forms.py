from .models import Process, ProcessMembership, SubProcess, InputMembership, OutputMembership, InputSubstance, OutputSubstance
from django import forms #import the forms framework
from django.forms.models import modelformset_factory, inlineformset_factory

class ProcessForm(forms.ModelForm):

    class Meta:
        model = Process
        exclude= ['subprocesses']
        widgets = {'owner': forms.HiddenInput()}

class SubProcessForm(forms.ModelForm):
    class Meta:
        model = SubProcess
        exclude= ['inputs', 'outputs']
        widgets = {'author': forms.HiddenInput()}
'''
    def __init__(self, request = None, *args, **kwargs):
        super(SubProcessForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.author != request.user:
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['name'].widget.attrs['class'] = 'disabled'
            self.fields['unit'].widget.attrs['readonly'] = True
            self.fields['unit'].widget.attrs['disabled'] = 'disabled'
            self.fields['unit'].widget.attrs['class'] = 'disabled'
            self.fields['category'].widget.attrs['readonly'] = True
            self.fields['category'].widget.attrs['class'] = 'disabled'

    def clean_name(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.author != request.user:
            return instance.name
        else:
            return self.cleaned_data['name']

    def clean_unit(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.author != request.user:
            return instance.unit
        else:
            return self.cleaned_data['unit']

    def clean_category(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.author != request.user:
            return instance.category
        else:
            return self.cleaned_data['category']
'''
class InputForm(forms.ModelForm):
    class Meta:
        model = InputSubstance
        fields= ['name', 'unit', 'emission_factor']

class OutputForm(forms.ModelForm):
    class Meta:
        model = OutputSubstance
        fields= ['name', 'unit', 'emission_factor']


SubProcessFormSet = inlineformset_factory(Process, ProcessMembership, exclude=[], widgets={
    'note': forms.Textarea(attrs={'cols':20, 'rows':2})})



InputFormSet = inlineformset_factory(SubProcess, InputMembership, exclude=['subprocess', 'id'], widgets={
    'note': forms.Textarea(attrs={'cols':20, 'rows':2})})



OutputFormSet = inlineformset_factory(SubProcess, OutputMembership, exclude=['subprocess', 'id'], widgets={
    'note': forms.Textarea(attrs={'cols':20, 'rows':2})})
