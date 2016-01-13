import flowdata.models as m
from django import forms #import the forms framework
from django.forms.models import modelformset_factory, inlineformset_factory

class AddInputForm(forms.ModelForm):

    class Meta:
        model = m.FlowInputMembership
        exclude= []
        widgets = {'transformation': forms.HiddenInput(), 'partOfSystem': forms.HiddenInput(), 'note':forms.Textarea()}

class AddOutputForm(forms.ModelForm):

    class Meta:
        model = m.FlowOutputMembership
        exclude= []
        widgets = {'transformation': forms.HiddenInput(), 'partOfSystem': forms.HiddenInput(), 'note':forms.Textarea()}

class AddTechOutputForm(forms.ModelForm):

    class Meta:
        model = m.FlowTechnosphereMembershipOutput
        exclude= []
        widgets = {'transformation': forms.HiddenInput(), 'partOfSystem': forms.HiddenInput(), 'note':forms.Textarea()}

class AddTechInputForm(forms.ModelForm):

    class Meta:
        model = m.FlowTechnosphereMembershipInput
        exclude= []
        widgets = {'techFlow': forms.HiddenInput(), 'partOfSystem': forms.HiddenInput(), 'note':forms.Textarea()}

class CreateInputForm(forms.ModelForm):

    class Meta:
        model = m.FlowInputSubstance
        exclude= []

class CreateOutputForm(forms.ModelForm):

    class Meta:
        model = m.FlowOutputSubstance
        exclude= []

class CreateTechFlowForm(forms.ModelForm):

    class Meta:
        model = m.FlowTechnosphere
        exclude= []

class CreateTransformationForm(forms.ModelForm):

    class Meta:
        model = m.FlowTransformation
        exclude= ['inputflows', 'outputflows', 'technosphereInputs', 'technosphereOutputs']
        widgets = {'author': forms.HiddenInput(), }#'partOfSystem': forms.HiddenInput()}

class CreateSystemForm(forms.ModelForm):

    class Meta:
        model = m.FlowSystem
        exclude= []
