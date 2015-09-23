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
    url(r'^process/all/$', 'data.views.all_processes'),
    url(r'^process/edit/(?P<process_id>\d+)$', 'data.views.create_edit_process'),
    url(r'^process/delete/(?P<process_id>\d+)$', 'data.views.delete_process'),
    url(r'^process/create/$', 'data.views.create_edit_process'),

    url(r'^subprocess/all/$', 'data.views.all_subprocesses'),
    url(r'^subprocess/edit/(?P<subprocess_id>\d+)$', 'data.views.create_edit_subprocess'),
    url(r'^subprocess/create/$', 'data.views.create_edit_subprocess'),
    url(r'^subprocess/delete/(?P<subprocess_id>\d+)$', 'data.views.delete_subprocess'),
    url(r'^subprocess/duplicate/(?P<subprocess_id>\d+)$', 'data.views.duplicate_subprocess'),

    url(r'^input/all/$', 'data.views.all_inputs'),
    url(r'^input/edit/(?P<input_id>\d+)$', 'data.views.create_edit_input'),
    url(r'^input/create/$', 'data.views.create_edit_input'),
    url(r'^input/delete/(?P<input_id>\d+)$', 'data.views.delete_input'),

    url(r'^output/all/$', 'data.views.all_outputs'),
    url(r'^output/edit/(?P<output_id>\d+)$', 'data.views.create_edit_output'),
    url(r'^output/create/$', 'data.views.create_edit_output'),
    url(r'^output/delete/(?P<output_id>\d+)$', 'data.views.delete_output'),
    
    url(r'^process/LCI/(?P<process_id>\d+)$', 'data.views.get_LCI'),
]
