# -*- coding: utf-8 -*-
from django.db.models import Q
from . import models


# 微信绑定相关
def is_bing_wx(user, openid):
    objs = models.WXUser.objects.filter(Q(user=user) | Q(openid=openid))
    if objs:
        return True
    else:
        return False


def get_wx_user(user):
    objs = models.WXUser.objects.filter(user=user)
    if objs:
        return objs[0]
    else:
        return None


def get_wx_user_by_openid(openid):
    objs = models.WXUser.objects.filter(openid=openid)
    if objs:
        return objs[0]
    else:
        return None


def get_user_pos(user):
    poses = models.UserPos.objects.filter(user=user).values_list("code", flat=True)
    return list(poses)
