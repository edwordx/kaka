# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response


def home(request):
    """
    网站首页
    """
    return HttpResponse(u"hello word!")


def page_404(request):
    return render_to_response('404.html')
