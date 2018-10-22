# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    # vuser
    url(r'^$', views.home, name="vuser_home"),
    url(r'^home_login/$', views.home_login, name="home_login"),
    url(r'^account/$', views.account, name="vuser_account"),
    url(r'^news/$', views.news, name="vuser_news"),
    url(r'^login/$', views.login, name="vuser_login"),
    url(r'^register/$', views.register, name="vuser_register"),
    url(r'^logout/$', views.logout, name="vuser_logout"),
    # wx
    url(r'^bind_wx_page/$', views.bind_wx_page, name="bind_wx_page"),
    url(r'^bind_wx/$', views.bind_wx, name="bind_wx"),
    url(r'^wx_redirect/$', views.wx_redirect, name="wx_redirect"),
    url(r'^wx_redirect_login/$', views.wx_redirect_login, name="wx_redirect_login"),
]
