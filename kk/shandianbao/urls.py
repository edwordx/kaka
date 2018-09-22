# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="sdb_home"),
    url(r'^add_user_terminals/$', views.add_user_terminals, name="add_user_terminals"),
]
