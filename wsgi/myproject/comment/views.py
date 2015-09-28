from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Comment
# Create your views here.

def submit_comment(request):

    print request.user
    print request.POST['comment']
    print request.POST['path']

    redirect = request.POST['path']

    new_comment = Comment(submitting_user=request.user, comment = request.POST['comment'], page = request.POST['path'])
    new_comment.save()

    return HttpResponseRedirect(redirect)
