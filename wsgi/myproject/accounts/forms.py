from django import forms #import the forms framework
from django.contrib.auth.models import User # import the model to be edited
from django.contrib.auth.forms import UserCreationForm #import the form to be edited

class MyRegistrationForm(UserCreationForm):

    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit = True):
        user = super(MyRegistrationForm, self).save(commit = False) # run the parent save command but don't commit to the database yet

        user.email = self.cleaned_data['email'] # add our stuff
        if commit:
            user.save() # save our bits (but only if commit is true (so we can override it if needs be later))

        return user

from data.models import UserProfile

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('institution', 'esr_number', 'work_package', 'profile_picture')

class UserBasicForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
