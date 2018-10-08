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
