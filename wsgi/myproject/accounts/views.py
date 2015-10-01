from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import  csrf
from forms import MyRegistrationForm, UserProfileForm, UserBasicForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import messages

from messenger.models import InternalMessage
from content.models import Content
from django.contrib.auth.models import User
from myproject.settings import ADMIN_USERNAME
from django.utils import timezone

# Create your views here.

def login(request):
	c = {}
	c.update(csrf(request))
	return render(request, 'login.html', c)

def auth_view(request):
	username = request.POST['username']
	password = request.POST['password']
	nextpage = request.POST.get('next','')

	user = auth.authenticate(username=username, password=password)

	if user is not None:
		if user.is_active:
			auth.login(request, user)

			if nextpage != '':
				return HttpResponseRedirect(nextpage)
			else:
				return HttpResponseRedirect('/data/process/all/')
		else:
		# Return a 'disabled account' error message
			return HttpResponseRedirect('/accounts/invalid/')
	else:
		# Return an 'invalid login' error message.
		return HttpResponseRedirect('/accounts/invalid/')

def loggedin(request):
	return render(request, 'loggedin.html', {'full_name':request.user.username})

def invalid_login(request):
	return render(request, 'invalid_login.html')

def logout(request):
	auth.logout(request)
	return render(request, 'logout.html')

def register_user(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			new_user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
			auth.login(request, new_user)

			admin = User.objects.get(username=ADMIN_USERNAME)
			welcomeContent = Content.objects.get(name='WelcomeMessage')
			welcomeBody = 'Hi ' + new_user.username +',\n' + welcomeContent.body

			print welcomeContent.title
			print welcomeBody

			welcome = InternalMessage(sender=admin, title = welcomeContent.title, body = welcomeBody)
			welcome.save()
			welcome.recipient.add(new_user)
			welcome.save()

			messages.success(request,'Thanks ' + request.POST['username'] + ', you are now registered. Please fill in your details below...')
			return HttpResponseRedirect("/accounts/profile")


	args = {}
	args.update(csrf(request))

	args['form'] = MyRegistrationForm()

	return render(request, 'register.html', args)

def register_success(request):
	return render(request, 'register_success.html')


@login_required
def user_profile(request):

	if request.method == 'POST':
		basicform = UserBasicForm(request.POST, instance = request.user)
		extraform = UserProfileForm(request.POST, request.FILES, instance = request.user.profile)

		if extraform.is_valid() and basicform.is_valid():
			basicform.save()
			extraform.save()
			messages.success(request, "Changes saved")
			return HttpResponseRedirect('/')
	else:
		user = request.user
		profile = user.profile
		basicform = UserBasicForm(instance = user)
		extraform = UserProfileForm(instance = profile)

		args ={}
		args.update(csrf(request))
		args['basicform'] = basicform
		args['extraform'] = extraform

		return render(request, 'profile.html', args)
