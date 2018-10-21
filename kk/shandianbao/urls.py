# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="sdb_home"),
    url(r'^add_user_terminals/$', views.add_user_terminals, name="add_user_terminals"),
    url(r'^add_user_terminals_agent/$', views.add_user_terminals_agent, name="add_user_terminals_agent"),
    url(r'^friends/$', views.friend_list, name="friend_list"),
    url(r'^terminal_index/$', views.terminal_index, name="terminal_index"),
    url(r'^terminal_list/$', views.terminal_list, name="terminal_list"),
    url(r'^terminal_statistics/$', views.terminal_statistics, name="terminal_statistics"),
    url(r'^trade_index/$', views.trade_index, name="trade_index"),
    url(r'^trade_info/$', views.trade_info, name="trade_info"),
    url(r'^trade_list/$', views.trade_list, name="trade_list"),
    url(r'^fenrun_index/$', views.fenrun_index, name="fenrun_index"),
    url(r'^fenrun_info/$', views.fenrun_info, name="fenrun_info"),
    url(r'^tixian_list/$', views.tixian_list, name="tixian_list"),
    url(r'^set_fenrun/(?P<child>[0-9]{11})/$', views.set_fenrun, name="set_fenrun"),
]
