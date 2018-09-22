# -*- coding: utf-8 -*-
import redis
import string
import random
import time
from django.contrib.auth.models import User
from django.conf import settings
from .models import UserProfile
from kk import config


rclient = redis.Redis(**config.REDIS_DATA)


def get_vuser_by_code(code, is_phone):
    if is_phone:
        objs = UserProfile.objects.filter(phone=code)
    else:
        objs = UserProfile.objects.filter(code=code)
    if objs and len(objs) == 1:
        return objs[0].user
    else:
        return None


def get_user_by_username(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user


def get_user_by_id(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = None
    return user


def exists_code(code):
    objs = UserProfile.objects.filter(code=code)
    if objs:
        return True
    else:
        return False


def _generate_code(n):
    res = []
    s = string.letters + string.digits
    for i in range(n):
        letter = random.choice(s)
        res.append(letter)
    return "".join(res)


def generate_code(n=6):
    code = _generate_code(n)
    if exists_code(code):
        return generate_code(n)
    else:
        return code


def datetime_to_timestamp(adatetime):
    return time.mktime(adatetime.timetuple())


def wrapper_raven(fun):
    """
    Wrapper for raven to trace manager commands
    """
    from raven import Client
    try:
        client = Client(settings.RAVEN_CONFIG["dsn"])
    except Exception:
        client = Client()

    def wrap(cls, *args, **kwargs):
        try:
            return fun(cls, *args, **kwargs)
        except Exception, e:
            print e
            client.captureException()
    return wrap
