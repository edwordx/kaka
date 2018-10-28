# -*- coding: utf-8 -*-
import uuid
import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MaxValueValidator, MinValueValidator


STATUS_CHOICE = (
    ('UP', u'未支付'),
    ('PD', u'已支付'),
    ('SU', u'成功'),
)

POINT_TYPE_CHOICE = (
    ('DAI', u'贷记卡'),
    ('JIE', u'借记卡'),
    ('YUN', u'云闪付'),
    ('YIN', u'银联快捷'),
    ('WX', u'微信支付宝'),
    ('FX', u'返现'),
)


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
        verbose_name = verbose_name_plural = u"用户终端"

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
    POINT_CHOICE = [("%.3f" % (i / 1000.), "%.3f" % (i / 1000.)) for i in range(500, 725, 5)]
    HARD_POINT_CHOICE = [("%.3f" % (i / 1000.), "%.3f" % (i / 1000.)) for i in range(550, 725, 5)]
    # 云闪付
    POINT_CHOICE_YUN = [("%.3f" % (i / 1000.), "%.3f" % (i / 1000.)) for i in range(300, 725, 5)]
    HARD_POINT_CHOICE_YUN = [("%.3f" % (i / 1000.), "%.3f" % (i / 1000.)) for i in range(350, 725, 5)]
    # 银联快捷
    POINT_CHOICE_YIN = [("%.3f" % (i / 1000.), "%.3f" % (i / 1000.)) for i in range(400, 550, 5)]
    HARD_POINT_CHOICE_YIN = [("%.3f" % (i / 1000.), "%.3f" % (i / 1000.)) for i in range(450, 550, 5)]
    # 微信
    POINT_CHOICE_WX = [("%.3f" % (i / 1000.), "%.3f" % (i / 1000.)) for i in range(300, 725, 5)]
    HARD_POINT_CHOICE_WX = [("%.3f" % (i / 1000.), "%.3f" % (i / 1000.)) for i in range(380, 550, 5)]
    # 首刷返现
    FX_RMB_CHOICE = [("%s" % i, "%s" % i) for i in range(120, 210, 10)]

    user = models.OneToOneField(User, verbose_name=u"用户")
    hardware_point = models.CharField(u"贷记卡硬件费率", choices=HARD_POINT_CHOICE, max_length=50)
    point = models.CharField(u"贷记卡代理费率", choices=POINT_CHOICE, max_length=50)
    hardware_point_yun = models.CharField(u"云闪付硬件费率", choices=HARD_POINT_CHOICE_YUN, max_length=50, blank=True)
    point_yun = models.CharField(u"云闪付代理费率", choices=POINT_CHOICE_YUN, max_length=50, blank=True)
    hardware_point_yin = models.CharField(u"银联快捷硬件费率", choices=HARD_POINT_CHOICE_YIN, max_length=50, blank=True)
    point_yin = models.CharField(u"银联快捷代理费率", choices=POINT_CHOICE_YIN, max_length=50, blank=True)
    hardware_point_wx = models.CharField(u"微信支付宝硬件费率", choices=HARD_POINT_CHOICE_WX, max_length=50, blank=True)
    point_wx = models.CharField(u"微信支付宝代理费率", choices=POINT_CHOICE_WX, max_length=50, blank=True)
    fanxian_rmb = models.CharField(u"返现金额（元）", choices=FX_RMB_CHOICE, max_length=50, default='120')
    profit = models.IntegerField(u"分润比例", default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    tax = models.IntegerField(u"税点比例", default=6, validators=[MinValueValidator(3), MaxValueValidator(30)])
    message = models.TextField(u"说明", blank=True)
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(u"更新时间", auto_now=True)

    class Meta:
        db_table = "sdb_fenrun"
        verbose_name = verbose_name_plural = u"用户分润"

    def __str__(self):
        return self.point


class SDBUserRMB(models.Model):
    """
    用户金钱表
    """
    user = models.OneToOneField(User)
    rmb = models.IntegerField(u"金额(分)")
    is_auto = models.BooleanField(u"自动到账", default=False)
    child_rmb = models.IntegerField(u"推荐（一级）金额(分)", default=0)
    child_two_rmb = models.IntegerField(u"推荐（二级）金额(分)", default=0)
    child_three_rmb = models.IntegerField(u"推荐（三级）金额(分)", default=0)
    fanxian_rmb = models.IntegerField(u"首刷返现", default=0)
    fanxian_child_rmb = models.IntegerField(u"推荐首刷返现", default=0)
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(u"更新时间", auto_now=True)

    class Meta:
        db_table = "sdb_user_rmb"
        verbose_name = verbose_name_plural = u"用户金钱"
        ordering = ["-rmb", "-child_rmb"]

    def __str__(self):
        return str(self.rmb)


@python_2_unicode_compatible
class SDBProfit(models.Model):
    """
    用户获利表
    """
    user = models.ForeignKey(User, verbose_name=u"用户")
    rmb = models.IntegerField(u"利润金额(分)", default=0)
    point_type = models.CharField(u"费率类型", choices=POINT_TYPE_CHOICE, max_length=10)
    # from fenrun
    point = models.CharField(u"费率", max_length=50, blank=True)
    hardware_point = models.CharField(u"硬件费率", max_length=50, blank=True)
    profit = models.IntegerField(u"分润比例")
    tax = models.IntegerField(u"税点比例")
    # from trade
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
    # 状态和时间
    status = models.CharField(u"订单状态", choices=STATUS_CHOICE, max_length=10, default="UP")
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)
    pay_time = models.DateTimeField(u"分红时间", null=True, blank=True)

    class Meta:
        db_table = "sdb_user_profit"
        verbose_name = verbose_name_plural = u"用户获利表"
        ordering = ["-pay_time"]

    def __str__(self):
        return self.trans_id


class SDBChildProfit(models.Model):
    """
    推荐获利表
    """
    user = models.ForeignKey(User, verbose_name=u"用户")
    rmb = models.IntegerField(u"利润金额(分)", default=0)
    diff_point = models.CharField(u"费率差值", max_length=50, blank=True)
    point_type = models.CharField(u"费率类型", choices=POINT_TYPE_CHOICE, max_length=10)
    # from fenrun
    point = models.CharField(u"费率", max_length=50, blank=True)
    hardware_point = models.CharField(u"硬件费率", max_length=50, blank=True)
    profit = models.IntegerField(u"分润比例")
    tax = models.IntegerField(u"税点比例")
    # from trade
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
    # 状态和时间
    status = models.CharField(u"订单状态", choices=STATUS_CHOICE, max_length=10, default="UP")
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)
    pay_time = models.DateTimeField(u"分红时间", null=True, blank=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class SDBChildOneProfit(SDBChildProfit):

    class Meta:
        db_table = "sdb_child_one_profit"
        verbose_name = verbose_name_plural = u"推荐获利表（一级）"
        ordering = ["-pay_time"]

    def __str__(self):
        return self.trans_id


@python_2_unicode_compatible
class SDBChildTwoProfit(SDBChildProfit):

    class Meta:
        db_table = "sdb_child_two_profit"
        verbose_name = verbose_name_plural = u"推荐获利表（二级）"
        ordering = ["-pay_time"]

    def __str__(self):
        return self.trans_id


@python_2_unicode_compatible
class SDBChildThreeProfit(SDBChildProfit):

    class Meta:
        db_table = "sdb_child_three_profit"
        verbose_name = verbose_name_plural = u"推荐获利表（三级）"
        ordering = ["-pay_time"]

    def __str__(self):
        return self.trans_id


@python_2_unicode_compatible
class SDBTiXianOrder(models.Model):
    ORDER_TYPE_CHOICE = (
        ('RMB', u'余额提现'),
        ('CHILD_RMB', u'推荐一级提现'),
        ('CHILD_TWO_RMB', u'推荐二级提现'),
        ('CHILD_THREE_RMB', u'推荐三级提现'),
        ('FANXIAN_RMB', u'返现提现'),
        ('FANXIAN_CHILD_RMB', u'推荐返现提现'),
    )
    user = models.ForeignKey(User, verbose_name=u"用户")
    user_account = models.CharField(u"用户账号", max_length=512, blank=True)
    rmb = models.IntegerField(u"提现金额(分)")
    fee = models.IntegerField(u"提现税费(分)")
    profit = models.IntegerField(u"分润比例")
    tax = models.IntegerField(u"税点比例")
    status = models.CharField(u"订单状态", choices=STATUS_CHOICE, max_length=10, default="UP")
    order_id = models.CharField(u"订单ID", max_length=64, unique=True)
    order_type = models.CharField(u"提现类型", choices=ORDER_TYPE_CHOICE, max_length=20, default="RMB")
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)
    pay_time = models.DateTimeField(u"提现时间", null=True, blank=True)
    finish_time = models.DateTimeField(u"完结时间", null=True, blank=True)

    def __str__(self):
        return self.order_id

    def save(self, *args, **kwargs):
        if not self.order_id:
            uid = str(uuid.uuid4())
            self.order_id = hashlib.md5(uid).hexdigest()
        return super(SDBTiXianOrder, self).save(*args, **kwargs)

    def _pay_rmb(self):
        return self.rmb - self.fee
    _pay_rmb.short_description = u"到账金额"
    pay_rmb = property(_pay_rmb)

    class Meta:
        db_table = "sdb_tixian_order"
        verbose_name = verbose_name_plural = u"用户提现"
        ordering = ["-pay_time"]
