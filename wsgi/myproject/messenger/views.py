from django.shortcuts import render
from .models import InternalMessage
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from myproject import settings
from django.utils import timezone

# Create your views here.

def check_messages(user):
    response={}
    myMessages = InternalMessage.objects.filter(recipient=user).order_by('-timestamp')
    unreadMessages = myMessages.filter(read=False)
    msgNo = len(unreadMessages)

    response.update({'myMessages':myMessages, 'msgNo':msgNo,})

    #print 'Checking messages for ' + user.first_name + ' ' + user.last_name
    #print user.first_name + ' ' + user.last_name + ' has ' + str(msgNo) + ' unread messages'

    return response

def inbox(request):
    args = {}

    if request.user.is_authenticated():
        myMessages = check_messages(request.user)
        args.update(myMessages)

    return render(request, 'inbox.html', args)

def showMessage(request):
    args = {}
    if request.method=="POST":
        msgID = request.POST['msgID']
        thisMessage = InternalMessage.objects.get(id=msgID)
        thisMessage.read=True
        thisMessage.save()
        args['thisMessage'] = thisMessage

    return render(request, 'show_message.html', args)

def replyToMessage(request):
    if request.method=="POST":
        oldSubject= request.POST['oldSubject']
        newBody = request.POST['messageReply']
        senderID = request.POST['senderID']
        mainRecipient = User.objects.get(id=senderID)
        sender = request.user
        oldRecipientList = request.POST.getlist('oldRecipient')

        if oldSubject[:4] != 'RE: ':
            newSubject = 'RE: ' + oldSubject
        else:
            newSubject = oldSubject

        if newBody=="":
            messages.add_message(request,
                                settings.DISALLOWED_MESSAGE,
                                "Please type a message!")
        else:

            reply = InternalMessage(sender=sender, title = newSubject, body = newBody, timestamp=timezone.now())
            reply.save()
            reply.recipient.add(mainRecipient)
            reply.save()
            #print 'Sent to ' + mainRecipient.first_name

            if request.POST.get('replyAll'):
                for r in oldRecipientList:
                    if int(r) != sender.id:
                        recipient = User.objects.get(id=r)
                        reply.recipient.add(recipient)
                        reply.save()
                        #print 'Sent to ' + recipient.first_name

            messages.success(request, "Message sent")

    return HttpResponseRedirect('/messages/inbox/')

def writeMessage(request):
    users = User.objects.exclude(id=request.user.id)
    args = {}
    args['users']=users
    return render(request, 'new_message.html', args)

def sendMessage(request):
    if request.method=="POST":
        title= request.POST['title']
        body = request.POST['message']
        recipients = request.POST.getlist('to_list')
        sender = request.user

        message = InternalMessage(sender=sender, title = title, body = body, timestamp=timezone.now())
        message.save()

        for recipientID in recipients:
            recipient = User.objects.get(id=int(recipientID))
            message.recipient.add(recipient)

        message.save()


        messages.success(request, "Message(s) sent")

    return HttpResponseRedirect('/messages/inbox/')
