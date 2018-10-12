# -*- coding: utf-8 -*-
import sys
from decimal import Decimal, ROUND_DOWN
import warnings
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from shandianbao import models
from kk import utils
from vuser.utils import wrapper_raven
from shandianbao import dbutils

reload(sys)
sys.setdefaultencoding('utf-8')
warnings.filterwarnings("ignore")


class Command(BaseCommand):
    """
    实时结算（推荐奖励）
    """
    def add_arguments(self, parser):
        parser.add_argument(
            '--start',
            action='store',
            dest='start',
            help=''
        )
        parser.add_argument(
            '--end',
            action='store',
            dest='end',
            help=''
        )

    @wrapper_raven
    def handle(self, start, end, *args, **options):
        now = datetime.now()
        if end is None:
            end_datetime = now
        else:
            end_datetime = utils.string_to_datetime(end)
        if start is None:
            start_datetime = end_datetime - timedelta(3)
        else:
            start_datetime = utils.string_to_datetime(start)
        start_date = start_datetime.date()
        end_date = end_datetime.date()
        print "__sync sdb child user rmb yun", start_date, end_date
        print now
        default_user = None
        # SDBTrade
        objs = models.SDBTrade.objects.filter(card_type=u"贷记卡").filter(return_code="00").filter(trade_type=u"云闪付支付收款").filter(business_type=u"非VIP交易")
        # SDBChildOneProfit
        one_ids = set(models.SDBChildOneProfit.objects.values_list("trans_id", flat=True))
        two_ids = set(models.SDBChildTwoProfit.objects.values_list("trans_id", flat=True))
        three_ids = set(models.SDBChildThreeProfit.objects.values_list("trans_id", flat=True))
        for obj in objs:
            adatetime = utils.string_to_datetime(obj.trade_date[:10], format_str="%Y-%m-%d")
            adate = adatetime.date()
            if start_date <= adate <= end_date:
                if obj.trans_id not in one_ids:
                    process_sdb_one_rmb(obj, default_user)
                if obj.trans_id not in two_ids:
                    process_sdb_two_rmb(obj, default_user)
                if obj.trans_id not in three_ids:
                    process_sdb_three_rmb(obj, default_user)
        print "ok"


def process_sdb_one_rmb(obj, default_user):
    print "process_sdb_one_rmb....."
    user = dbutils.get_user_by_terminal(obj.terminal)
    if user is None:
        print "user is None!"
        return

    if hasattr(user, "sdbfenrun"):
        user_point = user.sdbfenrun.point
        hardware_point = user.sdbfenrun.hardware_point
    else:
        print "no user fenrun!"
        return
    if not user_point or not hardware_point:
        print "no user_point or hardware_point!"
        return
    try:
        trade_rmb = Decimal(obj.trade_rmb)
    except Exception:
        print "no system trade rmb"
        return
    # father info
    if hasattr(user, "userprofile"):
        father = user.userprofile.father
    else:
        father = None
    if not father:
        print "no father!"
        return

    if hasattr(father, "sdbfenrun"):
        father_user_point = father.sdbfenrun.point
        father_hardware_point = father.sdbfenrun.hardware_point
    else:
        print "no father fenrun!"
        return
    if not father_user_point or not father_hardware_point:
        print "no father_user_point or father_hardware_point!"
        return

    diff_point = Decimal(user_point) - Decimal(father_user_point)
    if diff_point <= 0:
        xrmb = 0
    else:
        myrmb = Decimal(diff_point) / Decimal("100.0") * trade_rmb
        xrmb = myrmb.quantize(Decimal('1.00'), ROUND_DOWN)
        if xrmb < 0:
            print "user rmb less than 0 !!!"
            print obj.trans_id
            return
    profit = models.SDBChildOneProfit.objects.create(
        user=father,
        rmb=int(100 * Decimal(xrmb)),
        diff_point=str(diff_point),
        point_type="YUN",
        point=father_user_point,
        hardware_point=father_hardware_point,
        profit=father.sdbfenrun.profit,
        tax=father.sdbfenrun.tax,
        # obj
        trans_id=obj.trans_id,
        merchant=obj.merchant,
        trade_date=obj.trade_date,
        trade_rmb=obj.trade_rmb,
        trade_type=obj.trade_type,
        trade_status=obj.trade_status,
        card_code=obj.card_code,
        card_type=obj.card_type,
        return_code=obj.return_code,
        return_desc=obj.return_desc,
        terminal=obj.terminal,
        agent_level=obj.agent_level,
        agent=obj.agent,
        business_type=obj.business_type
    )
    profit.status = "PD"
    profit.pay_time = datetime.now()
    profit.save()
    dbutils.add_sdbuserrmb_child_rmb(father, profit.rmb)
    profit.status = "SU"
    profit.save()
    print "give child one sdb profile ok", father.username, profit.rmb


def process_sdb_two_rmb(obj, default_user):
    print "process_sdb_two_rmb....."
    user = dbutils.get_user_by_terminal(obj.terminal)
    if user is None:
        print "user is None!"
        return

    if hasattr(user, "sdbfenrun"):
        user_point = user.sdbfenrun.point
        hardware_point = user.sdbfenrun.hardware_point
    else:
        print "no user fenrun!"
        return
    if not user_point or not hardware_point:
        print "no user_point or hardware_point!"
        return
    try:
        trade_rmb = Decimal(obj.trade_rmb)
    except Exception:
        print "no system trade rmb"
        return
    # father info
    if hasattr(user, "userprofile"):
        father = user.userprofile.father
    else:
        father = None
    if not father:
        print "no father!"
        return

    if hasattr(father, "sdbfenrun"):
        father_user_point = father.sdbfenrun.point
        father_hardware_point = father.sdbfenrun.hardware_point
    else:
        print "no father fenrun!"
        return
    if not father_user_point or not father_hardware_point:
        print "no father_user_point or father_hardware_point!"
        return

    # father two info
    if hasattr(father, "userprofile"):
        father_two = father.userprofile.father
    else:
        father_two = None
    if not father_two:
        print "no father_two!"
        return

    if hasattr(father_two, "sdbfenrun"):
        father_two_user_point = father_two.sdbfenrun.point
        father_two_hardware_point = father_two.sdbfenrun.hardware_point
    else:
        print "no father_two fenrun!"
        return
    if not father_two_user_point or not father_two_hardware_point:
        print "no father_two_user_point or father_two_hardware_point!"
        return

    diff_one = Decimal(user_point) - Decimal(father_user_point)
    diff_one = max(Decimal("0.0"), diff_one)
    diff_two = Decimal(user_point) - Decimal(father_two_user_point)
    diff_two = max(Decimal("0.0"), diff_two)

    diff_point = diff_two - diff_one
    if diff_point <= 0:
        xrmb = 0
    else:
        myrmb = Decimal(diff_point) / Decimal("100.0") * trade_rmb
        xrmb = myrmb.quantize(Decimal('1.00'), ROUND_DOWN)
        if xrmb < 0:
            print "user rmb less than 0 !!!"
            print obj.trans_id
            return
    profit = models.SDBChildTwoProfit.objects.create(
        user=father_two,
        rmb=int(100 * Decimal(xrmb)),
        diff_point=str(diff_point),
        point_type="YUN",
        point=father_two_user_point,
        hardware_point=father_two_hardware_point,
        profit=father_two.sdbfenrun.profit,
        tax=father_two.sdbfenrun.tax,
        # obj
        trans_id=obj.trans_id,
        merchant=obj.merchant,
        trade_date=obj.trade_date,
        trade_rmb=obj.trade_rmb,
        trade_type=obj.trade_type,
        trade_status=obj.trade_status,
        card_code=obj.card_code,
        card_type=obj.card_type,
        return_code=obj.return_code,
        return_desc=obj.return_desc,
        terminal=obj.terminal,
        agent_level=obj.agent_level,
        agent=obj.agent,
        business_type=obj.business_type
    )
    profit.status = "PD"
    profit.pay_time = datetime.now()
    profit.save()
    dbutils.add_sdbuserrmb_child_two_rmb(father_two, profit.rmb)
    profit.status = "SU"
    profit.save()
    print "give child two sdb profile ok", father_two.username, profit.rmb


def process_sdb_three_rmb(obj, default_user):
    print "process_sdb_three_rmb......."
    user = dbutils.get_user_by_terminal(obj.terminal)
    if user is None:
        print "user is None!"
        return

    if hasattr(user, "sdbfenrun"):
        user_point = user.sdbfenrun.point
        hardware_point = user.sdbfenrun.hardware_point
    else:
        print "no user fenrun!"
        return
    if not user_point or not hardware_point:
        print "no user_point or hardware_point!"
        return
    try:
        trade_rmb = Decimal(obj.trade_rmb)
    except Exception:
        print "no system trade rmb"
        return
    # father info
    if hasattr(user, "userprofile"):
        father = user.userprofile.father
    else:
        father = None
    if not father:
        print "no father!"
        return

    if hasattr(father, "sdbfenrun"):
        father_user_point = father.sdbfenrun.point
        father_hardware_point = father.sdbfenrun.hardware_point
    else:
        print "no father fenrun!"
        return
    if not father_user_point or not father_hardware_point:
        print "no father_user_point or father_hardware_point!"
        return

    # father two info
    if hasattr(father, "userprofile"):
        father_two = father.userprofile.father
    else:
        father_two = None
    if not father_two:
        print "no father_two!"
        return

    if hasattr(father_two, "sdbfenrun"):
        father_two_user_point = father_two.sdbfenrun.point
        father_two_hardware_point = father_two.sdbfenrun.hardware_point
    else:
        print "no father_two fenrun!"
        return
    if not father_two_user_point or not father_two_hardware_point:
        print "no father_two_user_point or father_two_hardware_point!"
        return

    # father three info
    if hasattr(father_two, "userprofile"):
        father_three = father_two.userprofile.father
    else:
        father_three = None
    if not father_three:
        print "no father_three!"
        return

    if hasattr(father_three, "sdbfenrun"):
        father_three_user_point = father_three.sdbfenrun.point
        father_three_hardware_point = father_three.sdbfenrun.hardware_point
    else:
        print "no father_three fenrun!"
        return
    if not father_three_user_point or not father_three_hardware_point:
        print "no father_three_user_point or father_three_hardware_point!"
        return

    diff_one = Decimal(user_point) - Decimal(father_user_point)
    diff_one = max(Decimal("0.0"), diff_one)
    diff_two = Decimal(user_point) - Decimal(father_two_user_point)
    diff_two = max(Decimal("0.0"), diff_two)
    diff_three = Decimal(user_point) - Decimal(father_three_user_point)
    diff_three = max(Decimal("0.0"), diff_three)

    diff_point = diff_three - max(diff_two, diff_one)
    if diff_point <= 0:
        xrmb = 0
    else:
        myrmb = Decimal(diff_point) / Decimal("100.0") * trade_rmb
        xrmb = myrmb.quantize(Decimal('1.00'), ROUND_DOWN)
        if xrmb < 0:
            print "user rmb less than 0 !!!"
            print obj.trans_id
            return
    profit = models.SDBChildThreeProfit.objects.create(
        user=father_three,
        rmb=int(100 * Decimal(xrmb)),
        diff_point=str(diff_point),
        point_type="YUN",
        point=father_three_user_point,
        hardware_point=father_three_hardware_point,
        profit=father_three.sdbfenrun.profit,
        tax=father_three.sdbfenrun.tax,
        # obj
        trans_id=obj.trans_id,
        merchant=obj.merchant,
        trade_date=obj.trade_date,
        trade_rmb=obj.trade_rmb,
        trade_type=obj.trade_type,
        trade_status=obj.trade_status,
        card_code=obj.card_code,
        card_type=obj.card_type,
        return_code=obj.return_code,
        return_desc=obj.return_desc,
        terminal=obj.terminal,
        agent_level=obj.agent_level,
        agent=obj.agent,
        business_type=obj.business_type
    )
    profit.status = "PD"
    profit.pay_time = datetime.now()
    profit.save()
    dbutils.add_sdbuserrmb_child_three_rmb(father_three, profit.rmb)
    profit.status = "SU"
    profit.save()
    print "give child three sdb profile ok", father_three.username, profit.rmb
