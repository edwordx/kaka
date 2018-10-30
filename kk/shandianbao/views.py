# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import dbutils
from .models import SDBFenRun, SDBTiXianOrder, SDBPos
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
def terminal_change(request):
    user = request.user
    terminals = dbutils.get_sdb_pos(user)
    child_objs = user.children.all()
    users = []
    for child in child_objs:
        info = {
            "title": child.name,
            "value": child.phone
        }
        users.append(info)
    data = {"terminals": json.dumps(terminals), "users": json.dumps(users)}
    if request.method == 'POST':
        phone = request.POST.get("phone")
        terminal = request.POST.get("terminal", "")  # 逗号间隔
        terminal_list = terminal.split(",")
        ok_terminal_list = [t for t in terminal_list if t in terminals]
        child_user = get_user_by_username(phone)
        if child_user:
            objs = SDBPos.objects.filter(user=user).filter(terminal__in=ok_terminal_list)
            objs.update(user=child_user)
        return redirect("terminal_list")
    return render(request, "sdb/terminal_change.html", data)


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


def trade_info(request):
    data = {}
    user = request.user
    key = "cache:sdb:trade:%s" % user.username
    data_json = rclient.get(key)
    if data_json:
        try:
            res = json.loads(data_json)
            terminal_num = res["terminal_num"]
            rmb = res["rmb"]
            rmb_yun = res["rmb_yun"]
        except Exception:
            terminal_num = 0
            rmb = 0
            rmb_yun = 0
    else:
        terminal_num = 0
        rmb = 0
        rmb_yun = 0
    data = {"terminal_num": terminal_num, "rmb": rmb, "rmb_yun": rmb_yun}
    return render(request, "sdb/trade_info.html", data)


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
def fenrun_info(request):
    user = request.user
    fen = dbutils.get_sdbuserrmb_num(user)
    rmb = "%.2f" % (fen / 100.0)
    fenrun_obj = dbutils.get_sdb_fenrun(user)
    data = {
        "fenrun": fenrun_obj,
        "rmb": rmb
    }
    return render(request, "sdb/fenrun_info.html", data)


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
    # try:
    #     f_child_point = float(child_user.sdbfenrun.point)
    #     f_child_point_yun = float(child_user.sdbfenrun.point_yun)
    # except Exception, e:
    #     print e
    #     error = [u"此用户未设置过分润， 请联系管理员设置"]
    #     data.update({"error": error})
    #     return render(request, "sdb/set_fenrun.html", data)
    # 分润
    if hasattr(user, "sdbfenrun"):
        f_point = float(user.sdbfenrun.point)
        f_point_yun = float(user.sdbfenrun.point_yun)
        f_fanxian = float(user.sdbfenrun.fanxian_rmb)
        point_list = [x[0] for x in SDBFenRun.POINT_CHOICE if float(x[0]) >= f_point]
        point_yun_list = [x[0] for x in SDBFenRun.POINT_CHOICE_YUN if float(x[0]) >= f_point_yun]
        fanxian_list = [x[0] for x in SDBFenRun.FX_RMB_CHOICE if float(x[0]) <= f_fanxian]
        child_fenrun = {
            "point": json.dumps(point_list),
            "point_yun": json.dumps(point_yun_list),
            "fanxian": json.dumps(fanxian_list)
        }
    else:
        point_list = []
        point_yun_list = []
        fanxian_list = []
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
        fanxian = request.POST.get("fanxian")
        if point not in point_list or point_yun not in point_yun_list or fanxian not in fanxian_list:
            error = [u"分润点错误"]
            data.update({"error": error})
            return render(request, "sdb/set_fenrun.html", data)
        # 保存改动
        if hasattr(child_user, "sdbfenrun"):
            child_user.sdbfenrun.point = point
            child_user.sdbfenrun.point_yun = point_yun
            child_user.sdbfenrun.fanxian_rmb = fanxian
            child_user.sdbfenrun.save()
        else:
            # 全部继承上级的数据
            SDBFenRun.objects.create(
                user=child_user,
                hardware_point=user.sdbfenrun.hardware_point,
                point=point,
                hardware_point_yun=user.sdbfenrun.hardware_point_yun,
                point_yun=point_yun,
                hardware_point_yin=user.sdbfenrun.hardware_point_yin,
                hardware_point_wx=user.sdbfenrun.hardware_point_wx,
                fanxian_rmb=fanxian,
                profit=user.sdbfenrun.profit,
                tax=user.sdbfenrun.tax,
            )
        return redirect("friend_list")
    return render(request, "sdb/set_fenrun.html", data)


@login_required
def tixian_list(request):
    objs = SDBTiXianOrder.objects.filter(user=request.user)
    items = []
    for obj in objs:
        info = {
            "rmb": obj.rmb / 100.0,
            "pay_time": obj.pay_time,
            "status": obj.get_status_display
        }
        items.append(info)
    data = {"items": items}
    return render(request, "sdb/tixian_list.html", data)
