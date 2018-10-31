# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from collections import defaultdict
from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from . import models


def get_token_code():
    objs = models.SDBToken.objects.filter(is_disabled=False).order_by("-create_time")
    if objs:
        token = objs[0].token
    else:
        token = None
    return token


def disable_token(token):
    objs = models.SDBToken.objects.filter(token=token)
    for obj in objs:
        obj.is_disabled = True
        obj.save()


def add_token(token):
    obj = models.SDBToken.objects.create(token=token)
    return obj


def del_token():
    now = datetime.now() - timedelta(1)
    objs = models.SDBToken.objects.filter(create_time__lt=now)
    objs.delete()


def add_user_terminals(user, start, end):
    alist = []
    user_terminals = models.SDBPos.objects.filter(user=user)
    used_tids = {obj.terminal for obj in user_terminals}
    max_value = max(start, end)
    min_value = min(start, end)
    tids = range(min_value, max_value + 1)
    ok_tids = list(set(tids) - used_tids)
    terminal_objs = models.SDBTerminal.objects.filter(terminal__in=ok_tids)
    for terminal_obj in terminal_objs:
        obj = models.SDBPos(
            terminal=terminal_obj.terminal,
            user=user,
        )
        alist.append(obj)
    if alist:
        models.SDBPos.objects.bulk_create(alist)


def add_user_terminals_agent(user, agent):
    alist = []
    user_terminals = models.SDBPos.objects.filter(user=user)
    used_tids = {obj.terminal for obj in user_terminals}
    terminal_objs = models.SDBTerminal.objects.filter(agent=agent)
    for terminal_obj in terminal_objs:
        terminal = terminal_obj.terminal
        if terminal in used_tids:
            continue
        obj = models.SDBPos(
            terminal=terminal,
            user=user,
        )
        alist.append(obj)
    if alist:
        models.SDBPos.objects.bulk_create(alist)


def get_user_by_terminal(terminal):
    """
    通过终端号获取用户
    """
    try:
        obj = models.SDBPos.objects.get(terminal=terminal)
        user = obj.user
    except Exception:
        user = None
    return user


# rmb operation
def add_sdbuserrmb_rmb(user, rmb):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
        obj.rmb += rmb
        obj.save()


def sub_sdbuserrmb_rmb(user, rmb):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
        obj.rmb -= rmb
        obj.save()


def get_sdbuserrmb_num(user):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
    return obj.rmb


# child_rmb operation
def add_sdbuserrmb_child_rmb(user, rmb):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
        obj.child_rmb += rmb
        obj.save()


def sub_sdbuserrmb_child_rmb(user, rmb):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
        obj.child_rmb -= rmb
        obj.save()


def get_sdbuserrmb_child_num(user):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
    return obj.child_rmb


# child_rmb two operation
def add_sdbuserrmb_child_two_rmb(user, rmb):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
        obj.child_two_rmb += rmb
        obj.save()


def sub_sdbuserrmb_child_two_rmb(user, rmb):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
        obj.child_two_rmb -= rmb
        obj.save()


def get_sdbuserrmb_child_two_num(user):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
    return obj.child_two_rmb


# child_rmb three operation
def add_sdbuserrmb_child_three_rmb(user, rmb):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
        obj.child_three_rmb += rmb
        obj.save()


def sub_sdbuserrmb_child_three_rmb(user, rmb):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
        obj.child_three_rmb -= rmb
        obj.save()


def get_sdbuserrmb_child_three_num(user):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
    return obj.child_three_rmb


# fanxian rmb
def add_sdbuserrmb_fanxian_rmb(user, rmb):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
        obj.fanxian_rmb += rmb
        obj.save()


def sub_sdbuserrmb_fanxian_rmb(user, rmb):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
        obj.fanxian_rmb -= rmb
        obj.save()


def get_sdbuserrmb_fanxian_num(user):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
    return obj.fanxian_rmb


# fanxian child rmb
def add_sdbuserrmb_fanxian_child_rmb(user, rmb):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
        obj.fanxian_child_rmb += rmb
        obj.save()


def sub_sdbuserrmb_fanxian_child_rmb(user, rmb):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
        obj.fanxian_child_rmb -= rmb
        obj.save()


def get_sdbuserrmb_fanxian_child_num(user):
    with transaction.atomic():
        obj, created = models.SDBUserRMB.objects.select_for_update().get_or_create(user=user, defaults={"rmb": 0})
    return obj.fanxian_child_rmb


# pos
def get_sdb_pos(user):
    poses = models.SDBPos.objects.filter(user=user).values_list("terminal", flat=True)
    return list(poses)


def get_sdb_pos_objs(user):
    poses = get_sdb_pos(user)
    objs = models.SDBTerminal.objects.filter(terminal__in=poses)
    return objs


def get_pos_jihuo_num(poses):
    num = models.SDBTerminal.objects.filter(terminal__in=poses).filter(activate_status=u"已激活").count()
    return num


# trade
def get_latest_trade(poses):
    qs = models.SDBTrade.objects.filter(terminal__in=poses).filter(return_code="00")
    objs_01 = qs.filter(card_type=u"贷记卡").filter(trade_type__in=[u"刷卡支付收款", u"云闪付支付收款"]).filter(business_type=u"非VIP交易")
    objs_02 = qs.filter(trade_type=u"试刷")
    objs = objs_01 | objs_02
    objs = objs.order_by("-trade_date")[:100]
    return objs


# fenrun
def get_sdb_fenrun(user):
    objs = models.SDBFenRun.objects.filter(user=user)
    if objs:
        res = objs[0]
    else:
        res = None
    return res
