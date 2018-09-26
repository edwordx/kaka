# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MaxValueValidator, MinValueValidator


@python_2_unicode_compatible
class SDBTrade(models.Model):
    """
    数据来源https://shandianbao.chinapnr.com/supm/TRD101/index
    交易管理--交易明细查询
    """
    trans_id = models.CharField(u"流水号", max_length=64, unique=True)
    merchant = models.CharField(u"商户号", max_length=64)
    trade_date = models.CharField(u"交易日期", max_length=64)
    trade_rmb = models.CharField(u"交易金额（元）", max_length=64)
    trade_type = models.CharField(u"交易类型", max_length=64)
    trade_status = models.CharField(u"交易状态", max_length=64)
    card_code = models.CharField(u"卡号", max_length=64)
    card_type = models.CharField(u"卡类型", max_length=64)
    return_code = models.CharField(u"返回码", max_length=64)
    return_desc = models.CharField(u"返回码描述", max_length=64)
    terminal = models.CharField(u"终端号", max_length=64)
    agent_level = models.CharField(u"代理商等级", max_length=64)
    agent = models.CharField(u"代理商号", max_length=64)
    business_type = models.CharField(u"业务类型", max_length=64)
    update_time = models.DateTimeField(u"爬取更新时间", auto_now=True)

    class Meta:
        db_table = "sdb_trade"
        verbose_name = verbose_name_plural = u"交易明细"
        ordering = ["-trade_date"]

    def __str__(self):
        return self.trans_id


@python_2_unicode_compatible
class SDBTerminal(models.Model):
    """
    数据来源https://shandianbao.chinapnr.com/supm/TRD101/index
    终端管理--终端明细查询
    """
    terminal = models.CharField(u"终端号", max_length=64, unique=True)
    batch = models.CharField(u"批次号", max_length=64)
    company = models.CharField(u"机具厂商", max_length=64)
    pos_type = models.CharField(u"机具类型", max_length=64)
    pos_version = models.CharField(u"机具型号", max_length=64)
    agent = models.CharField(u"代理商号", max_length=64)
    agent_name = models.CharField(u"代理简称", max_length=64)
    bind_status = models.CharField(u"绑定状态", max_length=64)
    activate_status = models.CharField(u"激活状态", max_length=64)
    bind_merchant = models.CharField(u"绑定商户号", max_length=64)
    bind_time = models.CharField(u"绑定时间", max_length=64)
    update_time = models.DateTimeField(u"爬取更新时间", auto_now=True)

    class Meta:
        db_table = "sdb_terminal"
        verbose_name = verbose_name_plural = u"终端明细"
        ordering = ["-terminal"]

    def __str__(self):
        return self.terminal


@python_2_unicode_compatible
class SDBToken(models.Model):
    token = models.TextField(u"token")
    is_disabled = models.BooleanField(u"是否禁用", default=False)
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(u"更新时间", auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "sdb_token"
        verbose_name = verbose_name_plural = u"凭证"
        ordering = ["-create_time"]


@python_2_unicode_compatible
class SDBPos(models.Model):
    user = models.ForeignKey(User, verbose_name=u"用户")
    terminal = models.CharField(u"终端号", max_length=64, unique=True)
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(u"更新时间", auto_now=True)

    class Meta:
        db_table = "sdb_pos"
        verbose_name = verbose_name_plural = u"用户POS机"

    def __str__(self):
        return self.terminal


# @python_2_unicode_compatible
# class SDBPosProxy(SDBPos):

#     class Meta:
#         proxy = True
#         verbose_name = verbose_name_plural = u"用户POS机"

#     def __str__(self):
#         return self.terminal

@python_2_unicode_compatible
class SDBFenRun(models.Model):
    POINT_CHOICE = [
        ("0.5", u"0.5"),
        ("0.505", u"0.505"),
        ("0.51", u"0.51"),
        ("0.515", u"0.515"),
        ("0.52", u"0.52"),
        ("0.525", u"0.525"),
        ("0.53", u"0.53"),
        ("0.535", u"0.535"),
        ("0.54", u"0.54"),
        ("0.545", u"0.545"),
        ("0.55", u"0.55"),
        ("0.555", u"0.555"),
        ("0.56", u"0.56"),
        ("0.565", u"0.565"),
        ("0.57", u"0.57"),
        ("0.575", u"0.575"),
        ("0.58", u"0.58"),
        ("0.585", u"0.585"),
        ("0.59", u"0.59"),
        ("0.595", u"0.595"),
        ("0.6", u"0.6"),
        ("0.605", u"0.605"),
        ("0.61", u"0.61"),
        ("0.615", u"0.615"),
        ("0.62", u"0.62"),
        ("0.625", u"0.625"),
        ("0.63", u"0.63"),
        ("0.635", u"0.635"),
        ("0.64", u"0.64"),
        ("0.645", u"0.645"),
        ("0.65", u"0.65"),
        ("0.655", u"0.655"),
        ("0.66", u"0.66"),
        ("0.665", u"0.665"),
        ("0.67", u"0.67"),
        ("0.675", u"0.675"),
        ("0.68", u"0.68"),
        ("0.685", u"0.685"),
        ("0.69", u"0.69"),
        ("0.695", u"0.695"),
        ("0.7", u"0.7"),
        ("0.705", u"0.705"),
        ("0.71", u"0.71"),
        ("0.715", u"0.715"),
        ("0.72", u"0.72"),
    ]

    HARD_POINT_CHOICE = [
        ("0.55", u"0.55"),
        ("0.555", u"0.555"),
        ("0.56", u"0.56"),
        ("0.565", u"0.565"),
        ("0.57", u"0.57"),
        ("0.575", u"0.575"),
        ("0.58", u"0.58"),
        ("0.585", u"0.585"),
        ("0.59", u"0.59"),
        ("0.595", u"0.595"),
        ("0.6", u"0.6"),
        ("0.605", u"0.605"),
        ("0.61", u"0.61"),
        ("0.615", u"0.615"),
        ("0.62", u"0.62"),
        ("0.625", u"0.625"),
        ("0.63", u"0.63"),
        ("0.635", u"0.635"),
        ("0.64", u"0.64"),
        ("0.645", u"0.645"),
        ("0.65", u"0.65"),
        ("0.655", u"0.655"),
        ("0.66", u"0.66"),
        ("0.665", u"0.665"),
        ("0.67", u"0.67"),
        ("0.675", u"0.675"),
        ("0.68", u"0.68"),
        ("0.685", u"0.685"),
        ("0.69", u"0.69"),
        ("0.695", u"0.695"),
        ("0.7", u"0.7"),
        ("0.705", u"0.705"),
        ("0.71", u"0.71"),
        ("0.715", u"0.715"),
        ("0.72", u"0.72"),
    ]
    user = models.OneToOneField(User, verbose_name=u"用户")
    hardware_point = models.CharField(u"硬件费率", choices=HARD_POINT_CHOICE, max_length=50)
    point = models.CharField(u"代理费率", choices=POINT_CHOICE, max_length=50)
    profit = models.IntegerField(u"分润比例", default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    tax = models.IntegerField(u"税点比例", default=6, validators=[MinValueValidator(3), MaxValueValidator(30)])
    message = models.TextField(u"说明", blank=True)
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(u"更新时间", auto_now=True)

    class Meta:
        db_table = "sdb_fenrun"
        verbose_name = verbose_name_plural = u"贷记卡分润"

    def __str__(self):
        return self.point
