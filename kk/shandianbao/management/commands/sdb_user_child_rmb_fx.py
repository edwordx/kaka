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
    实时结算（推荐奖励）返现
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
        print "__sync sdb child user rmb fanxian", start_date, end_date
        print now
        default_user = None
        # SDBTrade
        objs = models.SDBTrade.objects.filter(return_code="00").filter(trade_type=u"试刷")
        # SDBChildOneProfit
        one_fx_objs = models.SDBChildOneProfit.objects.filter(point_type='FX')
        one_used_trans_ids = set()
        one_used_termials = set()
        for fx_obj in one_fx_objs:
            trans_id = fx_obj.trans_id
            terminal = fx_obj.terminal
            one_used_trans_ids.add(trans_id)
            one_used_termials.add(terminal)

        # SDBChildTwoProfit
        two_fx_objs = models.SDBChildTwoProfit.objects.filter(point_type='FX')
        two_used_trans_ids = set()
        two_used_termials = set()
        for fx_obj in two_fx_objs:
            trans_id = fx_obj.trans_id
            terminal = fx_obj.terminal
            two_used_trans_ids.add(trans_id)
            two_used_termials.add(terminal)

        # SDBChildThreeProfit
        three_fx_objs = models.SDBChildThreeProfit.objects.filter(point_type='FX')
        three_used_trans_ids = set()
        three_used_termials = set()
        for fx_obj in three_fx_objs:
            trans_id = fx_obj.trans_id
            terminal = fx_obj.terminal
            three_used_trans_ids.add(trans_id)
            three_used_termials.add(terminal)

        for obj in objs:
            adatetime = utils.string_to_datetime(obj.trade_date[:10], format_str="%Y-%m-%d")
            adate = adatetime.date()
            if start_date <= adate <= end_date:
                if obj.trans_id not in one_used_trans_ids and obj.terminal not in one_used_termials:
                    process_sdb_one_rmb(obj, default_user)
                if obj.trans_id not in two_used_trans_ids and obj.terminal not in two_used_termials:
                    process_sdb_two_rmb(obj, default_user)
                if obj.trans_id not in three_used_trans_ids and obj.terminal not in three_used_termials:
                    process_sdb_three_rmb(obj, default_user)
        print "ok"


def process_sdb_one_rmb(obj, default_user):
    print "process_sdb_fanxian_one_rmb....."
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
        print "no user fanxian_rmb!"
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
        father_fanxian_rmb = father.sdbfenrun.fanxian_rmb
    else:
        print "no father fenrun!"
        return
    if not father_fanxian_rmb:
        print "no father_fanxian_rmb!"
        return

    diff_fanxian_rmb = Decimal(father_fanxian_rmb) - Decimal(fanxian_rmb)
    if diff_fanxian_rmb <= 0:
        xrmb = 0
        print "user rmb less than 0 !!!"
        print obj.trans_id
    else:
        xrmb = diff_fanxian_rmb
    profit = models.SDBChildOneProfit.objects.create(
        user=father,
        rmb=int(100 * Decimal(xrmb)),
        diff_point=str(diff_fanxian_rmb),
        point_type="FX",
        point=father_fanxian_rmb,
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
    dbutils.add_sdbuserrmb_fanxian_child_rmb(father, profit.rmb)
    profit.status = "SU"
    profit.save()
    print "give child one sdb fanxian profile ok", father.username, profit.rmb


def process_sdb_two_rmb(obj, default_user):
    print "process_sdb_fanxian_two_rmb....."
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
        print "no user_fanxian_rmb!"
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
        father_fanxian_rmb = father.sdbfenrun.fanxian_rmb
    else:
        print "no father fenrun!"
        return
    if not father_fanxian_rmb:
        print "no father_fanxian_rmb!"
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
        father_two_fanxian_rmb = father_two.sdbfenrun.fanxian_rmb
    else:
        print "no father_two fenrun!"
        return
    if not father_two_fanxian_rmb:
        print "no father_two_fanxian_rmb!"
        return

    diff_one = Decimal(father_fanxian_rmb) - Decimal(fanxian_rmb)
    diff_one = max(Decimal("0.0"), diff_one)
    diff_two = Decimal(father_two_fanxian_rmb) - Decimal(fanxian_rmb)
    diff_two = max(Decimal("0.0"), diff_two)

    diff_rmb = diff_two - diff_one
    if diff_rmb <= 0:
        xrmb = 0
    else:
        xrmb = diff_rmb
    profit = models.SDBChildTwoProfit.objects.create(
        user=father_two,
        rmb=int(100 * Decimal(xrmb)),
        diff_point=str(diff_rmb),
        point_type="FX",
        point=father_two_fanxian_rmb,
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
    dbutils.add_sdbuserrmb_fanxian_child_rmb(father_two, profit.rmb)
    profit.status = "SU"
    profit.save()
    print "give child two sdb fanxian profile ok", father_two.username, profit.rmb


def process_sdb_three_rmb(obj, default_user):
    print "process_sdb_fanxian_three_rmb....."
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
        print "no user_fanxian_rmb!"
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
        father_fanxian_rmb = father.sdbfenrun.fanxian_rmb
    else:
        print "no father fenrun!"
        return
    if not father_fanxian_rmb:
        print "no father_fanxian_rmb!"
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
        father_two_fanxian_rmb = father_two.sdbfenrun.fanxian_rmb
    else:
        print "no father_two fenrun!"
        return
    if not father_two_fanxian_rmb:
        print "no father_two_fanxian_rmb!"
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
        father_three_fanxian_rmb = father_three.sdbfenrun.fanxian_rmb
    else:
        print "no father_three fenrun!"
        return
    if not father_three_fanxian_rmb:
        print "no father_three_fanxian_rmb!"
        return

    diff_one = Decimal(father_fanxian_rmb) - Decimal(fanxian_rmb)
    diff_one = max(Decimal("0.0"), diff_one)
    diff_two = Decimal(father_two_fanxian_rmb) - Decimal(fanxian_rmb)
    diff_two = max(Decimal("0.0"), diff_two)
    diff_three = Decimal(father_three_fanxian_rmb) - Decimal(fanxian_rmb)
    diff_three = max(Decimal("0.0"), diff_three)

    diff_rmb = diff_three - max(diff_two, diff_one)
    if diff_rmb <= 0:
        xrmb = 0
    else:
        xrmb = diff_rmb
    profit = models.SDBChildThreeProfit.objects.create(
        user=father_three,
        rmb=int(100 * Decimal(xrmb)),
        diff_point=str(diff_rmb),
        point_type="FX",
        point=father_three_fanxian_rmb,
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
    dbutils.add_sdbuserrmb_fanxian_child_rmb(father_three, profit.rmb)
    profit.status = "SU"
    profit.save()
    print "give child three sdb fanxian profile ok", father_three.username, profit.rmb
