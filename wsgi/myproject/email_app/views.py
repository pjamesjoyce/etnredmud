from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

# Create your views here.

def testEmail(request):

    send_mail('Subject here', 'Here is the message.', 'from@example.com',
    ['to@example.com'], fail_silently=False)

    return HttpResponseRedirect('/email/view/')

def viewMail(request):
    return render(request,'email.html')
