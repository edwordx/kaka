# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-20 19:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shandianbao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SDBPos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terminal', models.CharField(max_length=64, unique=True, verbose_name='\u7ec8\u7aef\u53f7')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'db_table': 'sdb_pos',
                'verbose_name': '\u7528\u6237POS\u673a',
                'verbose_name_plural': '\u7528\u6237POS\u673a',
            },
        ),
    ]