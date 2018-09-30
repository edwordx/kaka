# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-30 18:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shandianbao', '0004_auto_20180928_2054'),
    ]

    operations = [
        migrations.CreateModel(
            name='SDBProfit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rmb', models.IntegerField(default=0, verbose_name='\u5229\u6da6\u91d1\u989d(\u5206)')),
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
                'db_table': 'sdb_user_profit',
                'verbose_name': '\u91d1\u7528\u6237\u83b7\u5229\u8868',
                'verbose_name_plural': '\u91d1\u7528\u6237\u83b7\u5229\u8868',
            },
        ),
        migrations.CreateModel(
            name='SDBUserRMB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rmb', models.IntegerField(verbose_name='\u91d1\u989d(\u5206)')),
                ('is_auto', models.BooleanField(default=False, verbose_name='\u81ea\u52a8\u5230\u8d26')),
                ('child_rmb', models.IntegerField(default=0, verbose_name='\u63a8\u8350\u91d1\u989d(\u5206)')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-rmb', '-child_rmb'],
                'db_table': 'sdb_user_rmb',
                'verbose_name': '\u91d1\u7528\u6237\u91d1\u94b1\u8868',
                'verbose_name_plural': '\u91d1\u7528\u6237\u91d1\u94b1\u8868',
            },
        ),
        migrations.AlterModelOptions(
            name='sdbfenrun',
            options={'verbose_name': '\u5206\u6da6\u8bbe\u7f6e', 'verbose_name_plural': '\u5206\u6da6\u8bbe\u7f6e'},
        ),
        migrations.AlterField(
            model_name='sdbfenrun',
            name='hardware_point_wx',
            field=models.CharField(blank=True, choices=[(b'0.380', b'0.380'), (b'0.385', b'0.385'), (b'0.390', b'0.390'), (b'0.395', b'0.395'), (b'0.400', b'0.400'), (b'0.405', b'0.405'), (b'0.410', b'0.410'), (b'0.415', b'0.415'), (b'0.420', b'0.420'), (b'0.425', b'0.425'), (b'0.430', b'0.430'), (b'0.435', b'0.435'), (b'0.440', b'0.440'), (b'0.445', b'0.445'), (b'0.450', b'0.450'), (b'0.455', b'0.455'), (b'0.460', b'0.460'), (b'0.465', b'0.465'), (b'0.470', b'0.470'), (b'0.475', b'0.475'), (b'0.480', b'0.480'), (b'0.485', b'0.485'), (b'0.490', b'0.490'), (b'0.495', b'0.495'), (b'0.500', b'0.500'), (b'0.505', b'0.505'), (b'0.510', b'0.510'), (b'0.515', b'0.515'), (b'0.520', b'0.520'), (b'0.525', b'0.525'), (b'0.530', b'0.530'), (b'0.535', b'0.535'), (b'0.540', b'0.540'), (b'0.545', b'0.545')], max_length=50, verbose_name='\u5fae\u4fe1\u652f\u4ed8\u5b9d\u786c\u4ef6\u8d39\u7387'),
        ),
        migrations.AlterField(
            model_name='sdbfenrun',
            name='point_wx',
            field=models.CharField(blank=True, choices=[(b'0.300', b'0.300'), (b'0.305', b'0.305'), (b'0.310', b'0.310'), (b'0.315', b'0.315'), (b'0.320', b'0.320'), (b'0.325', b'0.325'), (b'0.330', b'0.330'), (b'0.335', b'0.335'), (b'0.340', b'0.340'), (b'0.345', b'0.345'), (b'0.350', b'0.350'), (b'0.355', b'0.355'), (b'0.360', b'0.360'), (b'0.365', b'0.365'), (b'0.370', b'0.370'), (b'0.375', b'0.375'), (b'0.380', b'0.380'), (b'0.385', b'0.385'), (b'0.390', b'0.390'), (b'0.395', b'0.395'), (b'0.400', b'0.400'), (b'0.405', b'0.405'), (b'0.410', b'0.410'), (b'0.415', b'0.415'), (b'0.420', b'0.420'), (b'0.425', b'0.425'), (b'0.430', b'0.430'), (b'0.435', b'0.435'), (b'0.440', b'0.440'), (b'0.445', b'0.445'), (b'0.450', b'0.450'), (b'0.455', b'0.455'), (b'0.460', b'0.460'), (b'0.465', b'0.465'), (b'0.470', b'0.470'), (b'0.475', b'0.475'), (b'0.480', b'0.480'), (b'0.485', b'0.485'), (b'0.490', b'0.490'), (b'0.495', b'0.495'), (b'0.500', b'0.500'), (b'0.505', b'0.505'), (b'0.510', b'0.510'), (b'0.515', b'0.515'), (b'0.520', b'0.520'), (b'0.525', b'0.525'), (b'0.530', b'0.530'), (b'0.535', b'0.535'), (b'0.540', b'0.540'), (b'0.545', b'0.545'), (b'0.550', b'0.550'), (b'0.555', b'0.555'), (b'0.560', b'0.560'), (b'0.565', b'0.565'), (b'0.570', b'0.570'), (b'0.575', b'0.575'), (b'0.580', b'0.580'), (b'0.585', b'0.585'), (b'0.590', b'0.590'), (b'0.595', b'0.595'), (b'0.600', b'0.600'), (b'0.605', b'0.605'), (b'0.610', b'0.610'), (b'0.615', b'0.615'), (b'0.620', b'0.620'), (b'0.625', b'0.625'), (b'0.630', b'0.630'), (b'0.635', b'0.635'), (b'0.640', b'0.640'), (b'0.645', b'0.645'), (b'0.650', b'0.650'), (b'0.655', b'0.655'), (b'0.660', b'0.660'), (b'0.665', b'0.665'), (b'0.670', b'0.670'), (b'0.675', b'0.675'), (b'0.680', b'0.680'), (b'0.685', b'0.685'), (b'0.690', b'0.690'), (b'0.695', b'0.695'), (b'0.700', b'0.700'), (b'0.705', b'0.705'), (b'0.710', b'0.710'), (b'0.715', b'0.715'), (b'0.720', b'0.720')], max_length=50, verbose_name='\u5fae\u4fe1\u652f\u4ed8\u5b9d\u4ee3\u7406\u8d39\u7387'),
        ),
    ]