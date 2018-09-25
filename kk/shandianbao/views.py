# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import dbutils
from vuser.utils import get_user_by_id


@login_required
def home(request):
    return HttpResponse("shadianbao!")


@staff_member_required
def add_user_terminals(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id', "")
        user_id = int(user_id) if user_id.isdigit() else 0
        target_user = get_user_by_id(user_id)
        return render(request, 'admin/add_user_terminals.html', {'target_user': target_user})
    else:
        user_id = request.POST.get('user_id', "")
        user_id = int(user_id) if user_id.isdigit() else 0
        target_user = get_user_by_id(user_id)
        start = request.POST.get('start', "")
        end = request.POST.get('end', "")
        start = int(start) if start.isdigit() else 0
        end = int(end) if end.isdigit() else 0
        if target_user and start and end:
            dbutils.add_user_terminals(target_user, start, end)
        return redirect("/admin/shandianbao/sdbpos/?user_id=%s" % user_id)


@staff_member_required
def add_user_terminals_agent(request):
    """
    通过代理商ID添加终端
    """
    if request.method == 'GET':
        user_id = request.GET.get('user_id', "")
        user_id = int(user_id) if user_id.isdigit() else 0
        target_user = get_user_by_id(user_id)
        return render(request, 'admin/add_user_terminals_agent.html', {'target_user': target_user})
    else:
        user_id = request.POST.get('user_id', "")
        user_id = int(user_id) if user_id.isdigit() else 0
        target_user = get_user_by_id(user_id)
        agent = request.POST.get('agent', "")
        if target_user and agent:
            dbutils.add_user_terminals_agent(target_user, agent)
        return redirect("/admin/shandianbao/sdbpos/?user_id=%s" % user_id)
