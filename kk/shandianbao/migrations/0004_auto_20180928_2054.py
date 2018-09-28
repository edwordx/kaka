# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-28 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shandianbao', '0003_sdbfenrun'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sdbfenrun',
            options={'verbose_name': '\u8d37\u8bb0\u5361\u5206\u6da6', 'verbose_name_plural': '\u8d37\u8bb0\u5361\u5206\u6da6'},
        ),
        migrations.AddField(
            model_name='sdbfenrun',
            name='hardware_point_wx',
            field=models.CharField(blank=True, choices=[(b'0.380', b'0.380'), (b'0.385', b'0.385'), (b'0.390', b'0.390'), (b'0.395', b'0.395'), (b'0.400', b'0.400'), (b'0.405', b'0.405'), (b'0.410', b'0.410'), (b'0.415', b'0.415'), (b'0.420', b'0.420'), (b'0.425', b'0.425'), (b'0.430', b'0.430'), (b'0.435', b'0.435'), (b'0.440', b'0.440'), (b'0.445', b'0.445'), (b'0.450', b'0.450'), (b'0.455', b'0.455'), (b'0.460', b'0.460'), (b'0.465', b'0.465'), (b'0.470', b'0.470'), (b'0.475', b'0.475'), (b'0.480', b'0.480'), (b'0.485', b'0.485'), (b'0.490', b'0.490'), (b'0.495', b'0.495'), (b'0.500', b'0.500'), (b'0.505', b'0.505'), (b'0.510', b'0.510'), (b'0.515', b'0.515'), (b'0.520', b'0.520'), (b'0.525', b'0.525'), (b'0.530', b'0.530'), (b'0.535', b'0.535'), (b'0.540', b'0.540'), (b'0.545', b'0.545')], max_length=50, verbose_name='\u5fae\u4fe1\u786c\u4ef6\u8d39\u7387'),
        ),
        migrations.AddField(
            model_name='sdbfenrun',
            name='hardware_point_yin',
            field=models.CharField(blank=True, choices=[(b'0.450', b'0.450'), (b'0.455', b'0.455'), (b'0.460', b'0.460'), (b'0.465', b'0.465'), (b'0.470', b'0.470'), (b'0.475', b'0.475'), (b'0.480', b'0.480'), (b'0.485', b'0.485'), (b'0.490', b'0.490'), (b'0.495', b'0.495'), (b'0.500', b'0.500'), (b'0.505', b'0.505'), (b'0.510', b'0.510'), (b'0.515', b'0.515'), (b'0.520', b'0.520'), (b'0.525', b'0.525'), (b'0.530', b'0.530'), (b'0.535', b'0.535'), (b'0.540', b'0.540'), (b'0.545', b'0.545')], max_length=50, verbose_name='\u94f6\u8054\u5feb\u6377\u786c\u4ef6\u8d39\u7387'),
        ),
        migrations.AddField(
            model_name='sdbfenrun',
            name='hardware_point_yun',
            field=models.CharField(blank=True, choices=[(b'0.350', b'0.350'), (b'0.355', b'0.355'), (b'0.360', b'0.360'), (b'0.365', b'0.365'), (b'0.370', b'0.370'), (b'0.375', b'0.375'), (b'0.380', b'0.380'), (b'0.385', b'0.385'), (b'0.390', b'0.390'), (b'0.395', b'0.395'), (b'0.400', b'0.400'), (b'0.405', b'0.405'), (b'0.410', b'0.410'), (b'0.415', b'0.415'), (b'0.420', b'0.420'), (b'0.425', b'0.425'), (b'0.430', b'0.430'), (b'0.435', b'0.435'), (b'0.440', b'0.440'), (b'0.445', b'0.445'), (b'0.450', b'0.450'), (b'0.455', b'0.455'), (b'0.460', b'0.460'), (b'0.465', b'0.465'), (b'0.470', b'0.470'), (b'0.475', b'0.475'), (b'0.480', b'0.480'), (b'0.485', b'0.485'), (b'0.490', b'0.490'), (b'0.495', b'0.495'), (b'0.500', b'0.500'), (b'0.505', b'0.505'), (b'0.510', b'0.510'), (b'0.515', b'0.515'), (b'0.520', b'0.520'), (b'0.525', b'0.525'), (b'0.530', b'0.530'), (b'0.535', b'0.535'), (b'0.540', b'0.540'), (b'0.545', b'0.545'), (b'0.550', b'0.550'), (b'0.555', b'0.555'), (b'0.560', b'0.560'), (b'0.565', b'0.565'), (b'0.570', b'0.570'), (b'0.575', b'0.575'), (b'0.580', b'0.580'), (b'0.585', b'0.585'), (b'0.590', b'0.590'), (b'0.595', b'0.595'), (b'0.600', b'0.600'), (b'0.605', b'0.605'), (b'0.610', b'0.610'), (b'0.615', b'0.615'), (b'0.620', b'0.620'), (b'0.625', b'0.625'), (b'0.630', b'0.630'), (b'0.635', b'0.635'), (b'0.640', b'0.640'), (b'0.645', b'0.645'), (b'0.650', b'0.650'), (b'0.655', b'0.655'), (b'0.660', b'0.660'), (b'0.665', b'0.665'), (b'0.670', b'0.670'), (b'0.675', b'0.675'), (b'0.680', b'0.680'), (b'0.685', b'0.685'), (b'0.690', b'0.690'), (b'0.695', b'0.695'), (b'0.700', b'0.700'), (b'0.705', b'0.705'), (b'0.710', b'0.710'), (b'0.715', b'0.715'), (b'0.720', b'0.720')], max_length=50, verbose_name='\u4e91\u95ea\u4ed8\u786c\u4ef6\u8d39\u7387'),
        ),
        migrations.AddField(
            model_name='sdbfenrun',
            name='point_wx',
            field=models.CharField(blank=True, choices=[(b'0.300', b'0.300'), (b'0.305', b'0.305'), (b'0.310', b'0.310'), (b'0.315', b'0.315'), (b'0.320', b'0.320'), (b'0.325', b'0.325'), (b'0.330', b'0.330'), (b'0.335', b'0.335'), (b'0.340', b'0.340'), (b'0.345', b'0.345'), (b'0.350', b'0.350'), (b'0.355', b'0.355'), (b'0.360', b'0.360'), (b'0.365', b'0.365'), (b'0.370', b'0.370'), (b'0.375', b'0.375'), (b'0.380', b'0.380'), (b'0.385', b'0.385'), (b'0.390', b'0.390'), (b'0.395', b'0.395'), (b'0.400', b'0.400'), (b'0.405', b'0.405'), (b'0.410', b'0.410'), (b'0.415', b'0.415'), (b'0.420', b'0.420'), (b'0.425', b'0.425'), (b'0.430', b'0.430'), (b'0.435', b'0.435'), (b'0.440', b'0.440'), (b'0.445', b'0.445'), (b'0.450', b'0.450'), (b'0.455', b'0.455'), (b'0.460', b'0.460'), (b'0.465', b'0.465'), (b'0.470', b'0.470'), (b'0.475', b'0.475'), (b'0.480', b'0.480'), (b'0.485', b'0.485'), (b'0.490', b'0.490'), (b'0.495', b'0.495'), (b'0.500', b'0.500'), (b'0.505', b'0.505'), (b'0.510', b'0.510'), (b'0.515', b'0.515'), (b'0.520', b'0.520'), (b'0.525', b'0.525'), (b'0.530', b'0.530'), (b'0.535', b'0.535'), (b'0.540', b'0.540'), (b'0.545', b'0.545'), (b'0.550', b'0.550'), (b'0.555', b'0.555'), (b'0.560', b'0.560'), (b'0.565', b'0.565'), (b'0.570', b'0.570'), (b'0.575', b'0.575'), (b'0.580', b'0.580'), (b'0.585', b'0.585'), (b'0.590', b'0.590'), (b'0.595', b'0.595'), (b'0.600', b'0.600'), (b'0.605', b'0.605'), (b'0.610', b'0.610'), (b'0.615', b'0.615'), (b'0.620', b'0.620'), (b'0.625', b'0.625'), (b'0.630', b'0.630'), (b'0.635', b'0.635'), (b'0.640', b'0.640'), (b'0.645', b'0.645'), (b'0.650', b'0.650'), (b'0.655', b'0.655'), (b'0.660', b'0.660'), (b'0.665', b'0.665'), (b'0.670', b'0.670'), (b'0.675', b'0.675'), (b'0.680', b'0.680'), (b'0.685', b'0.685'), (b'0.690', b'0.690'), (b'0.695', b'0.695'), (b'0.700', b'0.700'), (b'0.705', b'0.705'), (b'0.710', b'0.710'), (b'0.715', b'0.715'), (b'0.720', b'0.720')], max_length=50, verbose_name='\u5fae\u4fe1\u4ee3\u7406\u8d39\u7387'),
        ),
        migrations.AddField(
            model_name='sdbfenrun',
            name='point_yin',
            field=models.CharField(blank=True, choices=[(b'0.400', b'0.400'), (b'0.405', b'0.405'), (b'0.410', b'0.410'), (b'0.415', b'0.415'), (b'0.420', b'0.420'), (b'0.425', b'0.425'), (b'0.430', b'0.430'), (b'0.435', b'0.435'), (b'0.440', b'0.440'), (b'0.445', b'0.445'), (b'0.450', b'0.450'), (b'0.455', b'0.455'), (b'0.460', b'0.460'), (b'0.465', b'0.465'), (b'0.470', b'0.470'), (b'0.475', b'0.475'), (b'0.480', b'0.480'), (b'0.485', b'0.485'), (b'0.490', b'0.490'), (b'0.495', b'0.495'), (b'0.500', b'0.500'), (b'0.505', b'0.505'), (b'0.510', b'0.510'), (b'0.515', b'0.515'), (b'0.520', b'0.520'), (b'0.525', b'0.525'), (b'0.530', b'0.530'), (b'0.535', b'0.535'), (b'0.540', b'0.540'), (b'0.545', b'0.545')], max_length=50, verbose_name='\u94f6\u8054\u5feb\u6377\u4ee3\u7406\u8d39\u7387'),
        ),
        migrations.AddField(
            model_name='sdbfenrun',
            name='point_yun',
            field=models.CharField(blank=True, choices=[(b'0.300', b'0.300'), (b'0.305', b'0.305'), (b'0.310', b'0.310'), (b'0.315', b'0.315'), (b'0.320', b'0.320'), (b'0.325', b'0.325'), (b'0.330', b'0.330'), (b'0.335', b'0.335'), (b'0.340', b'0.340'), (b'0.345', b'0.345'), (b'0.350', b'0.350'), (b'0.355', b'0.355'), (b'0.360', b'0.360'), (b'0.365', b'0.365'), (b'0.370', b'0.370'), (b'0.375', b'0.375'), (b'0.380', b'0.380'), (b'0.385', b'0.385'), (b'0.390', b'0.390'), (b'0.395', b'0.395'), (b'0.400', b'0.400'), (b'0.405', b'0.405'), (b'0.410', b'0.410'), (b'0.415', b'0.415'), (b'0.420', b'0.420'), (b'0.425', b'0.425'), (b'0.430', b'0.430'), (b'0.435', b'0.435'), (b'0.440', b'0.440'), (b'0.445', b'0.445'), (b'0.450', b'0.450'), (b'0.455', b'0.455'), (b'0.460', b'0.460'), (b'0.465', b'0.465'), (b'0.470', b'0.470'), (b'0.475', b'0.475'), (b'0.480', b'0.480'), (b'0.485', b'0.485'), (b'0.490', b'0.490'), (b'0.495', b'0.495'), (b'0.500', b'0.500'), (b'0.505', b'0.505'), (b'0.510', b'0.510'), (b'0.515', b'0.515'), (b'0.520', b'0.520'), (b'0.525', b'0.525'), (b'0.530', b'0.530'), (b'0.535', b'0.535'), (b'0.540', b'0.540'), (b'0.545', b'0.545'), (b'0.550', b'0.550'), (b'0.555', b'0.555'), (b'0.560', b'0.560'), (b'0.565', b'0.565'), (b'0.570', b'0.570'), (b'0.575', b'0.575'), (b'0.580', b'0.580'), (b'0.585', b'0.585'), (b'0.590', b'0.590'), (b'0.595', b'0.595'), (b'0.600', b'0.600'), (b'0.605', b'0.605'), (b'0.610', b'0.610'), (b'0.615', b'0.615'), (b'0.620', b'0.620'), (b'0.625', b'0.625'), (b'0.630', b'0.630'), (b'0.635', b'0.635'), (b'0.640', b'0.640'), (b'0.645', b'0.645'), (b'0.650', b'0.650'), (b'0.655', b'0.655'), (b'0.660', b'0.660'), (b'0.665', b'0.665'), (b'0.670', b'0.670'), (b'0.675', b'0.675'), (b'0.680', b'0.680'), (b'0.685', b'0.685'), (b'0.690', b'0.690'), (b'0.695', b'0.695'), (b'0.700', b'0.700'), (b'0.705', b'0.705'), (b'0.710', b'0.710'), (b'0.715', b'0.715'), (b'0.720', b'0.720')], max_length=50, verbose_name='\u4e91\u95ea\u4ed8\u4ee3\u7406\u8d39\u7387'),
        ),
        migrations.AlterField(
            model_name='sdbfenrun',
            name='hardware_point',
            field=models.CharField(choices=[(b'0.550', b'0.550'), (b'0.555', b'0.555'), (b'0.560', b'0.560'), (b'0.565', b'0.565'), (b'0.570', b'0.570'), (b'0.575', b'0.575'), (b'0.580', b'0.580'), (b'0.585', b'0.585'), (b'0.590', b'0.590'), (b'0.595', b'0.595'), (b'0.600', b'0.600'), (b'0.605', b'0.605'), (b'0.610', b'0.610'), (b'0.615', b'0.615'), (b'0.620', b'0.620'), (b'0.625', b'0.625'), (b'0.630', b'0.630'), (b'0.635', b'0.635'), (b'0.640', b'0.640'), (b'0.645', b'0.645'), (b'0.650', b'0.650'), (b'0.655', b'0.655'), (b'0.660', b'0.660'), (b'0.665', b'0.665'), (b'0.670', b'0.670'), (b'0.675', b'0.675'), (b'0.680', b'0.680'), (b'0.685', b'0.685'), (b'0.690', b'0.690'), (b'0.695', b'0.695'), (b'0.700', b'0.700'), (b'0.705', b'0.705'), (b'0.710', b'0.710'), (b'0.715', b'0.715'), (b'0.720', b'0.720')], max_length=50, verbose_name='\u8d37\u8bb0\u5361\u786c\u4ef6\u8d39\u7387'),
        ),
        migrations.AlterField(
            model_name='sdbfenrun',
            name='point',
            field=models.CharField(choices=[(b'0.500', b'0.500'), (b'0.505', b'0.505'), (b'0.510', b'0.510'), (b'0.515', b'0.515'), (b'0.520', b'0.520'), (b'0.525', b'0.525'), (b'0.530', b'0.530'), (b'0.535', b'0.535'), (b'0.540', b'0.540'), (b'0.545', b'0.545'), (b'0.550', b'0.550'), (b'0.555', b'0.555'), (b'0.560', b'0.560'), (b'0.565', b'0.565'), (b'0.570', b'0.570'), (b'0.575', b'0.575'), (b'0.580', b'0.580'), (b'0.585', b'0.585'), (b'0.590', b'0.590'), (b'0.595', b'0.595'), (b'0.600', b'0.600'), (b'0.605', b'0.605'), (b'0.610', b'0.610'), (b'0.615', b'0.615'), (b'0.620', b'0.620'), (b'0.625', b'0.625'), (b'0.630', b'0.630'), (b'0.635', b'0.635'), (b'0.640', b'0.640'), (b'0.645', b'0.645'), (b'0.650', b'0.650'), (b'0.655', b'0.655'), (b'0.660', b'0.660'), (b'0.665', b'0.665'), (b'0.670', b'0.670'), (b'0.675', b'0.675'), (b'0.680', b'0.680'), (b'0.685', b'0.685'), (b'0.690', b'0.690'), (b'0.695', b'0.695'), (b'0.700', b'0.700'), (b'0.705', b'0.705'), (b'0.710', b'0.710'), (b'0.715', b'0.715'), (b'0.720', b'0.720')], max_length=50, verbose_name='\u8d37\u8bb0\u5361\u4ee3\u7406\u8d39\u7387'),
        ),
    ]
