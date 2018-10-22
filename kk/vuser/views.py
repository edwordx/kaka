# -*- coding: utf-8 -*-
import logging
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from .forms import LoginForm, RegisterForm
from .models import UserProfile, WXUser
from . import dbutils
from kk import config, wx_utils


logger = logging.getLogger('statistics')


@login_required
def home(request):
    """
    用户首页
    """
    data = {}
    return render(request, "kk/index.html", data)


def home_login(request):
    scope = "snsapi_base"
    state = "vuser_account"
    url = wx_utils.get_wx_authorize_url(config.WX_REDIRECT_URL_LOGIN, state, scope)
    return redirect(url)


def news(request):
    """
    资讯页
    """
    data = {}
    return render(request, "kk/news.html", data)


def account(request):
    """
    账户页
    """
    data = {}
    if request.user.is_authenticated:
        return render(request, "kk/account.html", data)
    else:
        return redirect("vuser_login")


def loginx(request):
    """
    登陆
    """
    if request.user.is_authenticated:
        return redirect("vuser_account")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                request.session['user_name'] = username
                return redirect("vuser_account")
    hashkey = CaptchaStore.generate_key()
    img_url = captcha_image_url(hashkey)
    data = {"img_url": img_url, "hashkey": hashkey}
    return render(request, "kk/login.html", data)


def login(request):
    data = {}
    if request.user.is_authenticated:
        return redirect("vuser_account")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return redirect("vuser_account")
        else:
            error = form.errors.get("__all__")
            data.update({"error": error, "errors": form.errors})
    hashkey = CaptchaStore.generate_key()
    img_url = captcha_image_url(hashkey)
    data.update({"img_url": img_url, "hashkey": hashkey})
    return render(request, "kk/login.html", data)


@login_required
def logout(request):
    auth.logout(request)
    return redirect("vuser_home")


def register(request):
    data = {}
    if request.user.is_authenticated:
        return redirect("vuser_account")
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            sex = form.cleaned_data.get('sex')
            name = form.cleaned_data.get('name')
            user = User.objects.create_user(username=username, password=password)
            user.save()
            UserProfile.objects.create(user=user, phone=user.username, sex=sex, name=name, father=form.get_father_user())
            auth.login(request, user)
            return redirect("vuser_account")
        else:
            error = form.errors.get("__all__")
            data.update({"error": error, "errors": form.errors})
    hashkey = CaptchaStore.generate_key()
    img_url = captcha_image_url(hashkey)
    data.update({"img_url": img_url, "hashkey": hashkey})
    return render(request, "kk/register.html", data)


@login_required
def bind_wx_page(request):
    # 绑定微信
    # 判断已经绑定过
    user = request.user
    wx_user = dbutils.get_wx_user(user)
    if wx_user:
        wx_info = {
            "nickname": wx_user.nickname,
            "headimgurl": wx_user.headimgurl
        }
        return render(request, "kk/wx_info.html", wx_info)
    return render(request, "kk/wx_page.html", {})


@login_required
def bind_wx(request):
    # 绑定微信
    # 判断已经绑定过
    user = request.user
    wx_user = dbutils.get_wx_user(user)
    if wx_user:
        wx_info = {
            "nickname": wx_user.nickname,
            "headimgurl": wx_user.headimgurl
        }
        return render(request, "kk/wx_info.html", wx_info)
    # 判断用户profile有内容
    if not hasattr(user, "userprofile"):
        return HttpResponse(u"用户信息有误")
    # 判断是否关注过（忽略，提现的时候判断）
    state = user.username
    url = wx_utils.get_wx_authorize_url(config.WX_REDIRECT_URL, state)
    return redirect(url)


def wx_redirect(request):
    """
    Info response
    {
    "openid":" OPENID",
    "nickname": NICKNAME,
    "sex":"1",
    "province":"PROVINCE"
    "city":"CITY",
    "country":"COUNTRY",
    "headimgurl":    "http://thirdwx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/46",
    "privilege":[ "PRIVILEGE1" "PRIVILEGE2"     ],
    "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
    }
    """
    # logger.info("wx_redirect")
    # logger.info(request.GET)
    code = request.GET.get("code")
    username = request.GET.get("state")
    user = dbutils.get_user_by_username(username)
    res = wx_utils.get_access_token(code)
    # access_token = res["access_token"]
    openid = res["openid"]
    scope = res["scope"]
    # 判断openid 是否绑定过
    if scope == "snsapi_userinfo":
        # 通过access_token和openid拉取用户信息
        # info_res = wx_utils.get_sns_userinfo(access_token, openid)
        api_access_token = wx_utils.get_api_access_token()
        info_res = wx_utils.get_userinfo(api_access_token, openid)
        if not info_res["subscribe"]:
            return HttpResponse(u"未关注公众号，不允许绑定")
        # logger.info(info_res)
        # 创建绑定关系 带用户信息
        if not dbutils.is_bing_wx(user, openid):
            WXUser.objects.create(
                user=user,
                openid=info_res["openid"],
                nickname=info_res["nickname"],
                sex=info_res["sex"],
                province=info_res["province"],
                city=info_res["city"],
                country=info_res["country"],
                headimgurl=info_res["headimgurl"],
                unionid=info_res.get("unionid", ""),
            )
        else:
            return HttpResponse(u"账户或者微信被绑定过")
    return HttpResponse(u"绑定成功")


def wx_redirect_login(request):
    """
    微信自动登陆回调
    """
    code = request.GET.get("code")
    uri = request.GET.get("state")
    res = wx_utils.get_access_token(code)
    # access_token = res["access_token"]
    openid = res["openid"]
    # scope = res["scope"]
    api_access_token = wx_utils.get_api_access_token()
    info = wx_utils.get_userinfo(api_access_token, openid)
    # 判断openid 是否关注过
    # 判断openid 是否绑定过
    if info["subscribe"]:
        wx_user = dbutils.get_wx_user_by_openid(openid)
        if wx_user:
            auth.login(request, wx_user.user)
    return redirect(uri)
