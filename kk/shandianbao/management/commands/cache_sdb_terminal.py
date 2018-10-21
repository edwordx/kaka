# -*- coding: utf-8 -*-
from decimal import Decimal
import sys
import json
from collections import defaultdict
import warnings
from django.core.management.base import BaseCommand
from shandianbao import models
from vuser.utils import wrapper_raven
from vuser.utils import rclient


reload(sys)
sys.setdefaultencoding('utf-8')
warnings.filterwarnings("ignore")


class Command(BaseCommand):
    """
    统计
    交易终端数量
    贷记卡交易总额
    云闪付交易总额
    """

    @wrapper_raven
    def handle(self, *args, **options):
        print "__cache sdb terminal"
        user_terminal_dict = get_user_pos()
        terminals = []
        for phone in user_terminal_dict:
            terminals.extend(user_terminal_dict[phone])

        # 数据
        trade_data, trade_data_yun = get_trade_list(terminals)
        for phone, poses in user_terminal_dict.iteritems():
            rmb = Decimal("0")
            rmb_yun = Decimal("0")
            pos_set = set()
            for pos in poses:
                if pos in trade_data or pos in trade_data_yun:
                    pos_set.add(pos)
                trade_rmb = [Decimal(x) for x in trade_data[pos]]
                trade_rmb_yun = [Decimal(x) for x in trade_data_yun[pos]]
                rmb += sum(trade_rmb)
                rmb_yun += sum(trade_rmb_yun)
            key = "cache:sdb:trade:%s" % phone
            data = {
                "terminal_num": len(pos_set),
                "rmb": "%.2f" % rmb,
                "rmb_yun": "%.2f" % rmb_yun,
            }
            data_json = json.dumps(data)
            rclient.set(key, data_json)
        print "ok"


def get_user_pos():
    objs = models.SDBPos.objects.all()
    res = defaultdict(list)
    for obj in objs:
        res[obj.user.username].append(obj.terminal)
    return res


def get_trade_list(terminals):
    res_yun = defaultdict(list)
    res = defaultdict(list)
    objs = models.SDBTrade.objects.filter(terminal__in=terminals).filter(return_code="00").filter(business_type=u"非VIP交易")
    for obj in objs:
        if obj.card_type == u"贷记卡" and obj.trade_type == u"云闪付支付收款":
            res_yun[obj.terminal].append(obj.trade_rmb)
        elif obj.card_type == u"贷记卡" and obj.trade_type == u"刷卡支付收款":
            res[obj.terminal].append(obj.trade_rmb)
    return res, res_yun
