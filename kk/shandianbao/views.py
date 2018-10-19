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


@login_required
def friend_list(request):
    friends = list(request.user.children.all())
    friends.sort(key=lambda x: x.create_time)
    pos_status_list = []
    for obj in friends:
        poses = dbutils.get_sdb_pos(obj.user)
        jihuo = dbutils.get_pos_jihuo_num(poses)
        pos_status_list.append((len(poses), jihuo))
    friends_res = zip(friends, pos_status_list)
    data = {"friends": friends_res}
    return render(request, "sdb/friend_list.html", data)


@login_required
def terminal_index(request):
    data = {}
    return render(request, "sdb/terminal_index.html", data)


@login_required
def trade_index(request):
    data = {}
    return render(request, "sdb/trade_index.html", data)


@login_required
def fenrun_index(request):
    data = {}
    return render(request, "sdb/fenrun_index.html", data)
