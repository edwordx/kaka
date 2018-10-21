# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import dbutils
from .models import SDBFenRun
from vuser.utils import get_user_by_id
from vuser.utils import rclient, get_user_by_username


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
def terminal_list(request):
    objs = dbutils.get_sdb_pos_objs(request.user)
    data = {"items": objs}
    return render(request, "sdb/terminal_list.html", data)


@login_required
def terminal_statistics(request):
    poses = dbutils.get_sdb_pos(request.user)
    total = len(poses)
    jihuo = dbutils.get_pos_jihuo_num(poses)
    left = total - jihuo
    if total > 0:
        ratio = jihuo * 100.0 / total
    else:
        ratio = 0
    ratio = "%.2f" % ratio
    data = {"total": total, "jihuo": jihuo, "left": left, "ratio": ratio}
    return render(request, "sdb/terminal_statistics.html", data)


@login_required
def trade_index(request):
    data = {}
    return render(request, "sdb/trade_index.html", data)


@login_required
def trade_list(request):
    poses = dbutils.get_sdb_pos(request.user)
    objs = dbutils.get_latest_trade(poses)
    data = {"items": objs}
    return render(request, "sdb/trade_list.html", data)


@login_required
def fenrun_index(request):
    data = {}
    return render(request, "sdb/fenrun_index.html", data)


@login_required
def set_fenrun(request, child):
    data = {}
    user = request.user
    # 关系判断
    child_user = get_user_by_username(child)
    children = [obj.phone for obj in request.user.children.all()]
    if not child_user or child not in children:
        error = [u"用户不存在或者不是您邀请来的"]
        data.update({"error": error})
        return render(request, "sdb/set_fenrun.html", data)
    try:
        f_child_point = float(child_user.sdbfenrun.point)
        f_child_point_yun = float(child_user.sdbfenrun.point_yun)
    except Exception, e:
        print e
        error = [u"此用户未设置过分润， 请联系管理员设置"]
        data.update({"error": error})
        return render(request, "sdb/set_fenrun.html", data)
    # 分润
    if hasattr(user, "sdbfenrun"):
        f_point = float(user.sdbfenrun.point)
        f_point_yun = float(user.sdbfenrun.point_yun)
        point_list = [x[0] for x in SDBFenRun.POINT_CHOICE if float(x[0]) >= f_point]
        point_yun_list = [x[0] for x in SDBFenRun.POINT_CHOICE_YUN if float(x[0]) >= f_point_yun]
        child_fenrun = {
            "point": json.dumps(point_list),
            "point_yun": json.dumps(point_yun_list)
        }
    else:
        point_list = []
        point_yun_list = []
        child_fenrun = {}
    data.update(child_fenrun)

    if request.method == 'POST':
        # 操作频繁
        key = 'sdb_setfenrun_locked_%s' % (user.id)
        locked = rclient.get(key)
        if locked:
            error = [u"操作太频繁"]
            data.update({"error": error})
            return render(request, "sdb/set_fenrun.html", data)
        else:
            rclient.set(key, True)
            rclient.expire(key, 10)
        # 数值判断
        point = request.POST.get("point")
        point_yun = request.POST.get("point_yun")
        if point not in point_list or point_yun not in point_yun_list:
            error = [u"分润点错误"]
            data.update({"error": error})
            return render(request, "sdb/set_fenrun.html", data)
        # 保存改动
        child_user.sdbfenrun.point = point
        child_user.sdbfenrun.point_yun = point_yun
        child_user.sdbfenrun.save()
        return redirect("friend_list")
    return render(request, "sdb/set_fenrun.html", data)


@login_required
def tixian_list(request):
    objs = []
    data = {"items": objs}
    return render(request, "sdb/tixian_list.html", data)
