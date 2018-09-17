# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


STATUS_CHOICE = (
    ('UP', u'未支付'),
    ('PD', u'已支付'),
    ('SU', u'成功'),
)


@python_2_unicode_compatible
class UserProfile(models.Model):
    SEX_CHOICE = [
        ('F', u'女'),
        ('M', u'男'),
        ('O', u'其他')
    ]
    user = models.OneToOneField(User)
    phone = models.CharField(u"手机", max_length=20, unique=True)
    name = models.CharField(u"姓名", max_length=20)
    sex = models.CharField(u"性别", choices=SEX_CHOICE, max_length=1)
    is_vip = models.BooleanField(u"是否VIP", default=False)
    code = models.CharField(u"邀请码", max_length=36, unique=True)
    father = models.ForeignKey(User, verbose_name=u"上家", related_name="children", null=True, blank=True)
    update_time = models.DateTimeField(u"创建时间", auto_now=True)
    create_time = models.DateTimeField(u"更新时间", auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            from .utils import generate_code
            self.code = generate_code()
        return super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        db_table = "vuser_profile"
        verbose_name = verbose_name_plural = u"用户属性"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class WXUser(models.Model):
    """
    微信用户
    """
    user = models.OneToOneField(User)
    openid = models.CharField(u"openid", max_length=128, unique=True)
    nickname = models.CharField(u"昵称", max_length=64, blank=True)
    sex = models.CharField(u"性别", max_length=10, blank=True)
    province = models.CharField(u"省份", max_length=64, blank=True)
    city = models.CharField(u"城市", max_length=64, blank=True)
    country = models.CharField(u"国家", max_length=64, blank=True)
    headimgurl = models.CharField(u"头像", max_length=512, blank=True)
    unionid = models.CharField(u"unionid", max_length=128, blank=True)
    update_time = models.DateTimeField(u"创建时间", auto_now=True)
    create_time = models.DateTimeField(u"更新时间", auto_now_add=True)

    class Meta:
        db_table = "wx_user"
        verbose_name = verbose_name_plural = u"微信用户"

    def __str__(self):
        return self.openid
