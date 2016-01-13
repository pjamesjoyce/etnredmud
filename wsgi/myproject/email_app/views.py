from django.shortcuts import render
from django.core.mail import send_mail, mail_admins
from django.http import HttpResponseRedirect

# Create your views here.

def testEmail(request):
    mail_admins("Something's happened on the RedMud site", "This is a test email to let all of the admins on the redmud site know something's happened.")
    send_mail('Subject here', 'Here is the message.', 'from@example.com',
    ['pjamesjoyce@gmail.com'], fail_silently=False)

    return HttpResponseRedirect('/email/view/')

def viewMail(request):
    return render(request,'email.html')
