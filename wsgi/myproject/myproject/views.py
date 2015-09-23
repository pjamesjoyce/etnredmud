from django.shortcuts import render
#from content.models import Content

def home(request):

    args = {}

    #homeblock1 = Content.objects.get(name='homeblock1')
    #homeblock2 = Content.objects.get(name='homeblock2')
    #homeblock3 = Content.objects.get(name='homeblock3')

    #args['homeblock1']=homeblock1
    #args['homeblock2']=homeblock2
    #args['homeblock3']=homeblock3

    return render(request, 'home.html', args)
