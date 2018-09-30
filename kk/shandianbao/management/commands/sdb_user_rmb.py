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
    实时结算
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
        print "__sync sdb user rmb", start_date, end_date
        print now
        default_user = None
        # SDBTrade
        used_trans_ids = set(models.SDBProfit.objects.values_list("trans_id", flat=True))
        objs = models.SDBTrade.objects.filter(card_type=u"贷记卡").filter(return_code="00").filter(trade_type=u"刷卡支付收款")
        for obj in objs:
            if obj.trans_id in used_trans_ids:
                continue
            adatetime = utils.string_to_datetime(obj.trade_date[:10], format_str="%Y-%m-%d")
            adate = adatetime.date()
            if start_date <= adate <= end_date:
                process_sdb_rmb(obj, default_user)
        print "ok"


def process_sdb_rmb(obj, default_user):
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
    diff_point = Decimal(hardware_point) - Decimal(user_point)
    if diff_point <= 0:
        xrmb = 0
    else:
        myrmb = Decimal(diff_point) / Decimal("100.0") * trade_rmb
        xrmb = myrmb.quantize(Decimal('1.00'), ROUND_DOWN)
        if xrmb < 0:
            print "user rmb less than 0 !!!"
            print obj.trans_id
            return
    profit = models.SDBProfit.objects.create(
        user=user,
        rmb=int(100 * Decimal(xrmb)),
        point_type="DAI",
        point=user_point,
        hardware_point=hardware_point,
        profit=user.sdbfenrun.profit,
        tax=user.sdbfenrun.tax,
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
    dbutils.add_sdbuserrmb_rmb(user, profit.rmb)
    profit.status = "SU"
    profit.save()
    print "give user sdb profile ok", user.username, profit.rmb
