# -*- coding: utf-8 -*-
from django.contrib import admin
from easy_select2 import select2_modelform
from . import models
from . import forms as fms


@admin.register(models.SDBToken)
class SDBTokenAdmin(admin.ModelAdmin):
    list_display = ["id", "token", "is_disabled", "create_time", "update_time"]
    fields = ["token", "is_disabled"]


@admin.register(models.SDBTrade)
class SDBTradeAdmin(admin.ModelAdmin):
    list_display = ["id", "trans_id", "merchant", "trade_date", "trade_rmb", "trade_type", "trade_status", "card_code", "card_type", "return_code", "return_desc", "terminal", "agent_level", "agent", "business_type", "update_time"]
    fields = ["trans_id", "merchant", "trade_date", "trade_rmb", "trade_type", "trade_status", "card_code", "card_type", "return_code", "return_desc", "terminal", "agent_level", "agent", "business_type"]
    search_fields = ["trans_id", "terminal", "trade_date", "merchant"]


@admin.register(models.SDBTerminal)
class SDBTerminalAdmin(admin.ModelAdmin):
    list_display = ["id", "terminal", "batch", "company", "pos_type", "pos_version", "agent", "agent_name", "bind_status", "activate_status", "bind_merchant", "bind_time", "update_time"]
    fields = ["terminal", "batch", "company", "pos_type", "pos_version", "agent", "agent_name", "bind_status", "activate_status", "bind_merchant", "bind_time"]
    search_fields = ["terminal", "bind_status", "activate_status", "bind_time", "agent"]


@admin.register(models.SDBPos)
class SDBPosAdmin(admin.ModelAdmin):
    form = fms.AdminSDBPosForm
    list_display = ["id", "user", "terminal", "create_time", "update_time"]
    fields = ["user", "terminal"]
    search_fields = ["terminal", "user__username"]


@admin.register(models.SDBFenRun)
class SDBFenRunAdmin(admin.ModelAdmin):
    form = select2_modelform(models.SDBFenRun)
    list_display = ["id", "user", "hardware_point", "point", "profit", "tax", "create_time", "update_time"]
    fields = ["user", "hardware_point", "point", "profit", "tax"]
    search_fields = ["user__username"]
