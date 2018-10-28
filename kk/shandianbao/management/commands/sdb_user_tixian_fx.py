# -*- coding: utf-8 -*-
import sys
import warnings
from datetime import datetime
from django.core.management.base import BaseCommand
from shandianbao import models
from kk.utils import wx_tixian
from vuser.utils import get_user_by_username, wrapper_raven
from vuser.dbutils import get_wx_user
from shandianbao import dbutils


reload(sys)
sys.setdefaultencoding('utf-8')
warnings.filterwarnings("ignore")

MIN_RMB = 1000  # 10元起


class Command(BaseCommand):
    """
    实时结算
    """
    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            action='store',
            dest='phone',
            help=''
        )

    @wrapper_raven
    def handle(self, phone, *args, **options):
        now = datetime.now()
        print "__sync sdb user tixian __ fanxian"
        print now
        if phone == "all":
            objs = models.SDBUserRMB.objects.filter(is_auto=True)
            tixian(objs)
        else:
            user = get_user_by_username(phone)
            if not user:
                print "no user", phone
                return
            if hasattr(user, "sdbuserrmb"):
                objs = [user.sdbuserrmb]
                tixian(objs)
        print "ok"


def tixian(objs):
    for obj in objs:
        print "start:", obj.user, obj.fanxian_rmb
        user = obj.user
        user_rmb = obj.fanxian_rmb
        if user_rmb < MIN_RMB:
            print "less than 10 RMB!"
            continue
        if hasattr(user, "sdbfenrun"):
            profit = user.sdbfenrun.profit
            tax = user.sdbfenrun.tax
        else:
            print "no user fenrun!"
            continue
        wx_user = get_wx_user(user)
        if not wx_user:
            print "no wx user!"
            continue
        if not hasattr(user, "userprofile"):
            print "no userprofile!"
            continue
        name = user.userprofile.name
        n = user_rmb / MIN_RMB
        tixian_rmb = n * MIN_RMB
        real_rmb = int(tixian_rmb * (profit / 100.0) * (1 - tax / 100.0))
        fee_rmb = tixian_rmb - real_rmb
        tx = models.SDBTiXianOrder.objects.create(
            user=user,
            user_account=wx_user.openid,
            rmb=tixian_rmb,
            fee=fee_rmb,
            profit=profit,
            tax=tax,
            order_type="FANXIAN_RMB",
        )
        dbutils.sub_sdbuserrmb_fanxian_rmb(user, tx.rmb)
        tx.pay_time = datetime.now()
        tx.status = "PD"
        tx.save()
        # give user wx rmb
        res = wx_tixian(wx_user.openid, str(real_rmb), name)
        if res["result_code"] == "SUCCESS":
            tx.status = 'SU'
            tx.finish_time = datetime.now()
            tx.save()
            print "pay ok!"
        else:
            print "pay error!"
            print res
