"""REDMUD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url

urlpatterns = [

    url(r'analysis/', include('analysis.urls')),

    url(r'^systems/$', 'flowdata.views.all_systems'),

    url(r'^setSystem/(?P<system_id>\d+)/$', 'flowdata.views.setSystem'),
    url(r'^chooseSystem/$', 'flowdata.views.chooseSystem'),
    url(r'^newSystem/$', 'flowdata.views.newSystem'),
    url(r'^createSystem/$', 'flowdata.views.createSystem'),

    url(r'^scan/$', 'flowdata.views.systemScan'),
    url(r'^scan/(?P<action_id>[\w]+)\|(?P<item_type>[\w]+)\|(?P<item_name>[\w\(\)-:]+)\|(?P<item_id>[\w]+)','flowdata.views.parseAction'),
    url(r'^addInputConfirm/$', 'flowdata.views.addInputConfirm'),
    url(r'^addOutputConfirm/$', 'flowdata.views.addOutputConfirm'),
    url(r'^addTechOutputConfirm/$', 'flowdata.views.addTechOutputConfirm'),
    url(r'^addTechInputConfirm/$', 'flowdata.views.addTechInputConfirm'),

    url(r'^editInputConfirm(?P<edit_id>[\w]+)/$', 'flowdata.views.editInputConfirm'),
    url(r'^editOutputConfirm(?P<edit_id>[\w]+)/$', 'flowdata.views.editOutputConfirm'),

    url(r'^createTechOutputSetup/$', 'flowdata.views.createTechFlowSetup'),
    url(r'^createTechInputSetup/$', 'flowdata.views.createProcessSetup'),
    url(r'^createTechFlowConfirm/$', 'flowdata.views.createTechFlowConfirm'),

    url(r'^createInputSetup/$', 'flowdata.views.createInputSetup'),
    url(r'^createInputConfirm/$', 'flowdata.views.createInputConfirm'),

    url(r'^createOutputSetup/$', 'flowdata.views.createOutputSetup'),
    url(r'^createOutputConfirm/$', 'flowdata.views.createOutputConfirm'),

    url(r'^addProcessConfirm/$', 'flowdata.views.addProcessConfirm'),
    url(r'^editProcessConfirm(?P<edit_id>[\w]+)/$', 'flowdata.views.editProcessConfirm'),

    url(r'^deleteSystem/(?P<system_id>[\d]+)/$', 'flowdata.views.deleteSystem'),

    ]
