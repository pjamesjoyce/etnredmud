from django.shortcuts import render
from content.models import Content

from messenger.views import check_messages
from lxml import html
import requests

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

    args['latestNews'] = redmudLatest("http://etn.redmud.org/news/")
    args['latestBlog'] = redmudLatest("http://etn.redmud.org/blog/")

    return render(request, 'home.html', args)

def redmudLatest(url):

    page = requests.get(url)
    encoding = page.encoding
    print encoding

    if encoding != 'utf-8':
        encpage = page.content.decode(encoding, 'replace').encode('utf-8')

    tree = html.fromstring(encpage)

    titleXPath = '//article/h2/a/text()'
    linkXPath = '//article/h2/a/@href'
    imgXpath = '//article/div/a/img/@src'
    titles = tree.xpath(titleXPath)
    links = tree.xpath(linkXPath)
    images = tree.xpath(imgXpath)

    data = []
    for i, title in enumerate(titles):
        data.append({'title':title, 'link':links[i], 'img':images[i]})

    return data
