# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from easy_select2 import select2_modelform
from . import models
from . import forms as fms
from . import utils, dbutils


def is_superuser(request):
    if request.user.is_active and request.user.is_superuser:
        return True
    else:
        return False


class MyUserAdmin(UserAdmin):

    def user_change_password(self, request, id, from_url=""):
        user = self.get_object(request, unquote(id))
        operator = request.user
        if user.is_superuser and user.id != operator.id:
            raise PermissionDenied
        return UserAdmin.user_change_password(self, request, id)


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "namex", "fatherx", "phone", "sex", "code", "create_time", "terminals_agent"]
    fields = ["user", "phone", "name", "sex", "is_vip", "code", "father"]
    search_fields = ["name", "phone"]
    all_fields = [f.name for f in models.UserProfile._meta.get_fields()]
    readonly_fields = all_fields

    def get_readonly_fields(self, request, obj=None):
        if is_superuser(request):
            return []
        else:
            return super(UserProfileAdmin, self).get_readonly_fields(request, obj)

    def fatherx(self, obj):
        if obj.father and hasattr(obj.user, "userprofile"):
            return '<a href="/admin/vuser/userprofile/?father__id__exact=%s" target="_blank">%s</a>' % (obj.father.id, obj.father.userprofile.name)
        else:
            return u"无"
    fatherx.allow_tags = True
    fatherx.short_description = u'导师'

    def namex(self, obj):
        return '<a href="/admin/vuser/userprofile/?father__id__exact=%s" target="_blank">%s</a>' % (obj.user.id, obj.name)
    namex.allow_tags = True
    namex.short_description = u'姓名'
    namex.admin_order_field = "name"

    def terminals(self, obj):
        return u'<a href="/sdb/add_user_terminals/?user_id=%s" target="_blank">添加终端</a>' % obj.user.id
    terminals.allow_tags = True
    terminals.short_description = u'添加终端'

    def terminals_agent(self, obj):
        return u'<a href="/sdb/add_user_terminals_agent/?user_id=%s" target="_blank">添加终端</a>' % obj.user.id
    terminals_agent.allow_tags = True
    terminals_agent.short_description = u'添加代理终端'


@admin.register(models.WXUser)
class WXUserAdmin(admin.ModelAdmin):
    list_display = ["user", "nicknamex", "openid", "nickname", "sex", "province", "city", "country", "headimgurl", "update_time"]
    fields = []
    search_fields = ["user__username"]

    def nicknamex(self, obj):
        user = obj.user
        if hasattr(user, "userprofile"):
            name = user.userprofile.name
        else:
            name = u"无"
        return name
    nicknamex.allow_tags = True
    nicknamex.short_description = u'姓名'
