# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from collections import defaultdict
from decimal import Decimal
from django.db import transaction
from django.contrib.auth.models import User
from django.db.models import Q
from . import models
from . import utils
from kk.utils import string_to_datetime


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
