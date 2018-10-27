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
    首刷返现
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
        print "__sync sdb user rmb fanxian", start_date, end_date
        print now
        default_user = None
        # SDBTrade
        fx_objs = models.SDBProfit.objects.filter(point_type='FX')
        used_trans_ids = set()
        used_termials = set()
        for fx_obj in fx_objs:
            trans_id = fx_obj.trans_id
            terminal = fx_obj.terminal
            used_trans_ids.add(trans_id)
            used_termials.add(terminal)

        objs = models.SDBTrade.objects.filter(return_code="00").filter(trade_type=u"试刷")
        for obj in objs:
            if obj.trans_id in used_trans_ids:
                continue
            if obj.terminal in used_termials:
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
        fanxian_rmb = user.sdbfenrun.fanxian_rmb
    else:
        print "no user fenrun!"
        return
    if not fanxian_rmb:
        print "no fanxian_rmb!"
        return
    profit = models.SDBProfit.objects.create(
        user=user,
        rmb=int(100 * Decimal(fanxian_rmb)),
        point_type="FX",
        point=fanxian_rmb,
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
    dbutils.add_sdbuserrmb_fanxian_rmb(user, profit.rmb)
    profit.status = "SU"
    profit.save()
    print "give user sdb fanxian profile ok", user.username, profit.rmb
