# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-08 14:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shandianbao', '0006_auto_20181007_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='SDBChildThreeProfit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rmb', models.IntegerField(default=0, verbose_name='\u5229\u6da6\u91d1\u989d(\u5206)')),
                ('diff_point', models.CharField(blank=True, max_length=50, verbose_name='\u8d39\u7387\u5dee\u503c')),
                ('point_type', models.CharField(choices=[(b'DAI', '\u8d37\u8bb0\u5361'), (b'JIE', '\u501f\u8bb0\u5361'), (b'YUN', '\u4e91\u95ea\u4ed8'), (b'YIN', '\u94f6\u8054\u5feb\u6377'), (b'WX', '\u5fae\u4fe1\u652f\u4ed8\u5b9d')], max_length=10, verbose_name='\u8d39\u7387\u7c7b\u578b')),
                ('point', models.CharField(blank=True, max_length=50, verbose_name='\u8d39\u7387')),
                ('hardware_point', models.CharField(blank=True, max_length=50, verbose_name='\u786c\u4ef6\u8d39\u7387')),
                ('profit', models.IntegerField(verbose_name='\u5206\u6da6\u6bd4\u4f8b')),
                ('tax', models.IntegerField(verbose_name='\u7a0e\u70b9\u6bd4\u4f8b')),
                ('trans_id', models.CharField(max_length=64, unique=True, verbose_name='\u6d41\u6c34\u53f7')),
                ('merchant', models.CharField(max_length=64, verbose_name='\u5546\u6237\u53f7')),
                ('trade_date', models.CharField(max_length=64, verbose_name='\u4ea4\u6613\u65e5\u671f')),
                ('trade_rmb', models.CharField(max_length=64, verbose_name='\u4ea4\u6613\u91d1\u989d\uff08\u5143\uff09')),
                ('trade_type', models.CharField(max_length=64, verbose_name='\u4ea4\u6613\u7c7b\u578b')),
                ('trade_status', models.CharField(max_length=64, verbose_name='\u4ea4\u6613\u72b6\u6001')),
                ('card_code', models.CharField(max_length=64, verbose_name='\u5361\u53f7')),
                ('card_type', models.CharField(max_length=64, verbose_name='\u5361\u7c7b\u578b')),
                ('return_code', models.CharField(max_length=64, verbose_name='\u8fd4\u56de\u7801')),
                ('return_desc', models.CharField(max_length=64, verbose_name='\u8fd4\u56de\u7801\u63cf\u8ff0')),
                ('terminal', models.CharField(max_length=64, verbose_name='\u7ec8\u7aef\u53f7')),
                ('agent_level', models.CharField(max_length=64, verbose_name='\u4ee3\u7406\u5546\u7b49\u7ea7')),
                ('agent', models.CharField(max_length=64, verbose_name='\u4ee3\u7406\u5546\u53f7')),
                ('business_type', models.CharField(max_length=64, verbose_name='\u4e1a\u52a1\u7c7b\u578b')),
                ('status', models.CharField(choices=[(b'UP', '\u672a\u652f\u4ed8'), (b'PD', '\u5df2\u652f\u4ed8'), (b'SU', '\u6210\u529f')], default=b'UP', max_length=10, verbose_name='\u8ba2\u5355\u72b6\u6001')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='\u5206\u7ea2\u65f6\u95f4')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'ordering': ['-pay_time'],
                'db_table': 'sdb_child_three_profit',
                'verbose_name': '\u63a8\u8350\u83b7\u5229\u8868\uff08\u4e09\u7ea7\uff09',
                'verbose_name_plural': '\u63a8\u8350\u83b7\u5229\u8868\uff08\u4e09\u7ea7\uff09',
            },
        ),
        migrations.CreateModel(
            name='SDBChildTwoProfit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rmb', models.IntegerField(default=0, verbose_name='\u5229\u6da6\u91d1\u989d(\u5206)')),
                ('diff_point', models.CharField(blank=True, max_length=50, verbose_name='\u8d39\u7387\u5dee\u503c')),
                ('point_type', models.CharField(choices=[(b'DAI', '\u8d37\u8bb0\u5361'), (b'JIE', '\u501f\u8bb0\u5361'), (b'YUN', '\u4e91\u95ea\u4ed8'), (b'YIN', '\u94f6\u8054\u5feb\u6377'), (b'WX', '\u5fae\u4fe1\u652f\u4ed8\u5b9d')], max_length=10, verbose_name='\u8d39\u7387\u7c7b\u578b')),
                ('point', models.CharField(blank=True, max_length=50, verbose_name='\u8d39\u7387')),
                ('hardware_point', models.CharField(blank=True, max_length=50, verbose_name='\u786c\u4ef6\u8d39\u7387')),
                ('profit', models.IntegerField(verbose_name='\u5206\u6da6\u6bd4\u4f8b')),
                ('tax', models.IntegerField(verbose_name='\u7a0e\u70b9\u6bd4\u4f8b')),
                ('trans_id', models.CharField(max_length=64, unique=True, verbose_name='\u6d41\u6c34\u53f7')),
                ('merchant', models.CharField(max_length=64, verbose_name='\u5546\u6237\u53f7')),
                ('trade_date', models.CharField(max_length=64, verbose_name='\u4ea4\u6613\u65e5\u671f')),
                ('trade_rmb', models.CharField(max_length=64, verbose_name='\u4ea4\u6613\u91d1\u989d\uff08\u5143\uff09')),
                ('trade_type', models.CharField(max_length=64, verbose_name='\u4ea4\u6613\u7c7b\u578b')),
                ('trade_status', models.CharField(max_length=64, verbose_name='\u4ea4\u6613\u72b6\u6001')),
                ('card_code', models.CharField(max_length=64, verbose_name='\u5361\u53f7')),
                ('card_type', models.CharField(max_length=64, verbose_name='\u5361\u7c7b\u578b')),
                ('return_code', models.CharField(max_length=64, verbose_name='\u8fd4\u56de\u7801')),
                ('return_desc', models.CharField(max_length=64, verbose_name='\u8fd4\u56de\u7801\u63cf\u8ff0')),
                ('terminal', models.CharField(max_length=64, verbose_name='\u7ec8\u7aef\u53f7')),
                ('agent_level', models.CharField(max_length=64, verbose_name='\u4ee3\u7406\u5546\u7b49\u7ea7')),
                ('agent', models.CharField(max_length=64, verbose_name='\u4ee3\u7406\u5546\u53f7')),
                ('business_type', models.CharField(max_length=64, verbose_name='\u4e1a\u52a1\u7c7b\u578b')),
                ('status', models.CharField(choices=[(b'UP', '\u672a\u652f\u4ed8'), (b'PD', '\u5df2\u652f\u4ed8'), (b'SU', '\u6210\u529f')], default=b'UP', max_length=10, verbose_name='\u8ba2\u5355\u72b6\u6001')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='\u5206\u7ea2\u65f6\u95f4')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'ordering': ['-pay_time'],
                'db_table': 'sdb_child_two_profit',
                'verbose_name': '\u63a8\u8350\u83b7\u5229\u8868\uff08\u4e8c\u7ea7\uff09',
                'verbose_name_plural': '\u63a8\u8350\u83b7\u5229\u8868\uff08\u4e8c\u7ea7\uff09',
            },
        ),
        migrations.AddField(
            model_name='sdbuserrmb',
            name='child_three_rmb',
            field=models.IntegerField(default=0, verbose_name='\u63a8\u8350\uff08\u4e09\u7ea7\uff09\u91d1\u989d(\u5206)'),
        ),
        migrations.AddField(
            model_name='sdbuserrmb',
            name='child_two_rmb',
            field=models.IntegerField(default=0, verbose_name='\u63a8\u8350\uff08\u4e8c\u7ea7\uff09\u91d1\u989d(\u5206)'),
        ),
        migrations.AlterField(
            model_name='sdbuserrmb',
            name='child_rmb',
            field=models.IntegerField(default=0, verbose_name='\u63a8\u8350\uff08\u4e00\u7ea7\uff09\u91d1\u989d(\u5206)'),
        ),
    ]
