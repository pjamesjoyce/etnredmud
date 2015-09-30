from django.shortcuts import render
from content.models import Content

from messenger.views import check_messages

def home(request):

    args = {}

    if request.user.is_authenticated():
        myMessages = check_messages(request.user)
        args.update(myMessages)



    homeblock1 = Content.objects.get(name='homeblock1')
    homeblock2 = Content.objects.get(name='homeblock2')
    homeblock3 = Content.objects.get(name='homeblock3')

    args['homeblock1']=homeblock1
    args['homeblock2']=homeblock2
    args['homeblock3']=homeblock3

    return render(request, 'home.html', args)
