# -*- coding: utf-8 -*-
from django.contrib import admin
from easy_select2 import select2_modelform
from . import models
from . import forms as fms


def is_superuser(request):
    if request.user.is_active and request.user.is_superuser:
        return True
    else:
        return False


@admin.register(models.SDBToken)
class SDBTokenAdmin(admin.ModelAdmin):
    list_display = ["id", "token", "is_disabled", "create_time", "update_time"]
    fields = ["token", "is_disabled"]


@admin.register(models.SDBTrade)
class SDBTradeAdmin(admin.ModelAdmin):
    list_display = ["trans_id", "merchant", "trade_date", "trade_rmb", "trade_type", "trade_status", "card_code", "card_type", "return_code", "return_desc", "terminal", "agent_level", "agent", "business_type", "update_time"]
    fields = ["trans_id", "merchant", "trade_date", "trade_rmb", "trade_type", "trade_status", "card_code", "card_type", "return_code", "return_desc", "terminal", "agent_level", "agent", "business_type"]
    search_fields = ["trans_id", "terminal", "trade_date", "merchant"]
    list_filter = ["card_type", "trade_type", "trade_status", "return_code"]


@admin.register(models.SDBTerminal)
class SDBTerminalAdmin(admin.ModelAdmin):
    list_display = ["terminal", "batch", "company", "pos_type", "pos_version", "agent", "agent_name", "bind_status", "activate_status", "bind_merchant", "bind_time", "update_time"]
    fields = ["terminal", "batch", "company", "pos_type", "pos_version", "agent", "agent_name", "bind_status", "activate_status", "bind_merchant", "bind_time"]
    search_fields = ["terminal", "bind_status", "activate_status", "bind_time", "agent"]


@admin.register(models.SDBPos)
class SDBPosAdmin(admin.ModelAdmin):
    form = fms.AdminSDBPosForm
    list_display = ["user", "nickname", "terminal", "create_time", "update_time"]
    fields = ["user", "terminal"]
    search_fields = ["terminal", "user__username"]

    def nickname(self, obj):
        user = obj.user
        if hasattr(user, "userprofile"):
            name = user.userprofile.name
        else:
            name = u"无"
        return name
    nickname.allow_tags = True
    nickname.short_description = u'昵称'


@admin.register(models.SDBFenRun)
class SDBFenRunAdmin(admin.ModelAdmin):
    form = select2_modelform(models.SDBFenRun)
    list_display = ["user", "nickname", "hardware_point", "point", "hardware_point_yun", "point_yun", "hardware_point_yin", "point_yin", "hardware_point_wx", "point_wx", "fanxian_rmb", "profit", "tax", "create_time", "update_time"]
    fields = ["user", "hardware_point", "point", "hardware_point_yun", "point_yun", "hardware_point_yin", "point_yin", "hardware_point_wx", "point_wx", "fanxian_rmb", "profit", "tax"]
    search_fields = ["user__username"]

    def nickname(self, obj):
        user = obj.user
        if hasattr(user, "userprofile"):
            name = user.userprofile.name
        else:
            name = u"无"
        return name
    nickname.allow_tags = True
    nickname.short_description = u'昵称'


@admin.register(models.SDBUserRMB)
class SDBUserRMBAdmin(admin.ModelAdmin):
    form = select2_modelform(models.SDBUserRMB)
    list_display = ["user", "nickname", "rmb", "child_rmb", "child_two_rmb", "child_three_rmb", "fanxian_rmb", "fanxian_child_rmb", "is_auto", "create_time", "update_time"]
    fields = ["user", "rmb", "child_rmb", "child_two_rmb", "child_three_rmb", "fanxian_rmb", "fanxian_child_rmb", "is_auto"]
    search_fields = ["user__username"]
    readonly_fields = fields
    list_filter = ["is_auto"]
    actions = ['auto_ok_action', 'auto_no_action']

    def get_readonly_fields(self, request, obj=None):
        if is_superuser(request):
            return []
        else:
            return super(SDBUserRMBAdmin, self).get_readonly_fields(request, obj)

    def auto_ok_action(self, request, queryset):
        for obj in queryset:
            obj.is_auto = True
            obj.save()
    auto_ok_action.short_description = u"自动到账"

    def auto_no_action(self, request, queryset):
        for obj in queryset:
            obj.is_auto = False
            obj.save()
    auto_no_action.short_description = u"不自动到账"

    def nickname(self, obj):
        user = obj.user
        if hasattr(user, "userprofile"):
            name = user.userprofile.name
        else:
            name = u"无"
        return name
    nickname.allow_tags = True
    nickname.short_description = u'昵称'


@admin.register(models.SDBProfit)
class SDBProfitAdmin(admin.ModelAdmin):
    list_display = ["user", "nickname", "rmb", "point_type", "point", "hardware_point", "profit", "tax", "trans_id", "merchant", "trade_date", "trade_rmb", "trade_type", "trade_status", "card_code", "card_type", "return_code", "return_desc", "terminal", "agent_level", "agent", "business_type", "status", "create_time", "pay_time"]
    fields = ["user", "rmb", "point_type", "point", "hardware_point", "profit", "tax", "trans_id", "merchant", "trade_date", "trade_rmb", "trade_type", "trade_status", "card_code", "card_type", "return_code", "return_desc", "terminal", "agent_level", "agent", "business_type", "status", "create_time", "pay_time"]
    readonly_fields = fields
    search_fields = ["user__username", "trans_id", "terminal", "trade_date", "merchant"]
    list_filter = ["point_type"]

    def nickname(self, obj):
        user = obj.user
        if hasattr(user, "userprofile"):
            name = user.userprofile.name
        else:
            name = u"无"
        return name
    nickname.allow_tags = True
    nickname.short_description = u'昵称'


@admin.register(models.SDBChildOneProfit)
class SDBChildOneProfitAdmin(admin.ModelAdmin):
    list_display = ["user", "nickname", "rmb", "diff_point", "point_type", "point", "hardware_point", "profit", "tax", "trans_id", "merchant", "trade_date", "trade_rmb", "trade_type", "trade_status", "card_code", "card_type", "return_code", "return_desc", "terminal", "agent_level", "agent", "business_type", "status", "create_time", "pay_time"]
    fields = ["user", "rmb", "diff_point", "point_type", "point", "hardware_point", "profit", "tax", "trans_id", "merchant", "trade_date", "trade_rmb", "trade_type", "trade_status", "card_code", "card_type", "return_code", "return_desc", "terminal", "agent_level", "agent", "business_type", "status", "create_time", "pay_time"]
    readonly_fields = fields
    search_fields = ["user__username", "trans_id", "terminal", "trade_date", "merchant"]
    list_filter = ["point_type"]

    def nickname(self, obj):
        user = obj.user
        if hasattr(user, "userprofile"):
            name = user.userprofile.name
        else:
            name = u"无"
        return name
    nickname.allow_tags = True
    nickname.short_description = u'昵称'


@admin.register(models.SDBChildTwoProfit)
class SDBChildTwoProfitAdmin(admin.ModelAdmin):
    list_display = ["user", "nickname", "rmb", "diff_point", "point_type", "point", "hardware_point", "profit", "tax", "trans_id", "merchant", "trade_date", "trade_rmb", "trade_type", "trade_status", "card_code", "card_type", "return_code", "return_desc", "terminal", "agent_level", "agent", "business_type", "status", "create_time", "pay_time"]
    fields = ["user", "rmb", "diff_point", "point_type", "point", "hardware_point", "profit", "tax", "trans_id", "merchant", "trade_date", "trade_rmb", "trade_type", "trade_status", "card_code", "card_type", "return_code", "return_desc", "terminal", "agent_level", "agent", "business_type", "status", "create_time", "pay_time"]
    readonly_fields = fields
    search_fields = ["user__username", "trans_id", "terminal", "trade_date", "merchant"]
    list_filter = ["point_type"]

    def nickname(self, obj):
        user = obj.user
        if hasattr(user, "userprofile"):
            name = user.userprofile.name
        else:
            name = u"无"
        return name
    nickname.allow_tags = True
    nickname.short_description = u'昵称'


@admin.register(models.SDBChildThreeProfit)
class SDBChildThreeProfitAdmin(admin.ModelAdmin):
    list_display = ["user", "nickname", "rmb", "diff_point", "point_type", "point", "hardware_point", "profit", "tax", "trans_id", "merchant", "trade_date", "trade_rmb", "trade_type", "trade_status", "card_code", "card_type", "return_code", "return_desc", "terminal", "agent_level", "agent", "business_type", "status", "create_time", "pay_time"]
    fields = ["user", "rmb", "diff_point", "point_type", "point", "hardware_point", "profit", "tax", "trans_id", "merchant", "trade_date", "trade_rmb", "trade_type", "trade_status", "card_code", "card_type", "return_code", "return_desc", "terminal", "agent_level", "agent", "business_type", "status", "create_time", "pay_time"]
    readonly_fields = fields
    search_fields = ["user__username", "trans_id", "terminal", "trade_date", "merchant"]
    list_filter = ["point_type"]

    def nickname(self, obj):
        user = obj.user
        if hasattr(user, "userprofile"):
            name = user.userprofile.name
        else:
            name = u"无"
        return name
    nickname.allow_tags = True
    nickname.short_description = u'昵称'


@admin.register(models.SDBTiXianOrder)
class SDBTiXianOrderAdmin(admin.ModelAdmin):
    list_display = ["user", "nickname", "user_account", "rmb", "fee", "status", "order_id", "order_type", "create_time", "pay_time", "finish_time"]
    fields = ["user", "nickname", "user_account", "rmb", "fee", "status", "order_id", "order_type", "pay_time", "finish_time"]
    search_fields = ["user__username", ]
    list_filter = ["status", "order_type"]

    def nickname(self, obj):
        user = obj.user
        if hasattr(user, "userprofile"):
            name = user.userprofile.name
        else:
            name = u"无"
        return name
    nickname.allow_tags = True
    nickname.short_description = u'昵称'
