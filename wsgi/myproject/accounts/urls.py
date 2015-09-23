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
    url(r'^login/$', 'accounts.views.login'),
    url(r'^auth/$', 'accounts.views.auth_view'),
    url(r'^logout/$', 'accounts.views.logout'),
    url(r'^loggedin/$', 'accounts.views.loggedin'),
    url(r'^invalid/$', 'accounts.views.invalid_login'),
    url(r'^register/$', 'accounts.views.register_user'),
    url(r'^register_success/$', 'accounts.views.register_success'),
    url(r'^profile/$', 'accounts.views.user_profile')
]
