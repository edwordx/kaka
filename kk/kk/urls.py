# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.home, name="site_home"),
    url(r'^admin/', admin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^vuser/', include('vuser.urls')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
]

handler404 = "kk.views.page_404"
