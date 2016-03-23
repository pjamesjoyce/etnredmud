from django.shortcuts import render
import flowdata.models as m
import json
import xml.etree.ElementTree as ET
import urllib2
from HTMLParser import HTMLParser
from lxml import html
import requests


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    articles = []
    def handle_starttag(self, tag, attrs):
        print tag
        if tag == 'article':
            self.articles.append(attrs)
    # def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
    # def handle_data(self, data):
        #print "Encountered some data  :", data

# Create your views here.


def treemap(request):

    system_id=request.session['currentSystemID']
    data = get_LCI_data(system_id)

    return render(request, 'treemap.html',{'data' : data})


def get_LCI_data(system_id):

    jsonLCI = {"name": "System", "children":[]}

    system = m.FlowSystem.objects.get(id = system_id)

    firstLevels = m.FlowTransformation.objects.filter(partOfSystem = system)

    for process in firstLevels:
        thisChildren = []

        for item in m.FlowInputMembership.objects.filter(partOfSystem = system).filter(transformation = process):
            thisChildren.append({"name":item.inputsubstance.name, "value": item.inputsubstance.emission_factor*item.amount_required})

        for item in m.FlowOutputMembership.objects.filter(partOfSystem = system).filter(transformation = process):
            thisChildren.append({"name":item.outputsubstance.name, "value": item.outputsubstance.emission_factor*item.amount_required})

        jsonLCI["children"].append({"name": process.name, "children":thisChildren})



    stuff = json.dumps(jsonLCI)

    return stuff

    #print firstLevels


def redmudRSSfeed(request):

    # instantiate the parser and fed it some HTML
    #parser = MyHTMLParser()


    #myxml = urllib2.urlopen("http://etn.redmud.org/feed/").read()
    #root = ET.fromstring(myxml)

    #items = []
    #for child in root.iter('channel'):
        #for item in child.findall('item'):
            #title = item.find('title').text
            #link = item.find('link').text
            #category = item.find('category').text
            #description = item.find('description').text

    #connection = urllib2.urlopen("http://etn.redmud.org/blog/")
    #encoding = connection.headers.getparam('charset')
    #page = connection.read().decode(encoding)
    page = requests.get("http://etn.redmud.org/blog/")
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



    #for i in articles:
    #    print i
    #parser.feed(page)


            #if category == 'Blog':
                #items.append({'title':title, 'link':link, 'category':category, 'description':description})
    #print parser.articles

    return render(request, 'rsstest.html', {'data':data})
