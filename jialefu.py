# -*- coding: UTF-8 -*-
import requests
from verification_code import get_code
import json
import base64
from requests.cookies import RequestsCookieJar
cie = 'DISTRIBUTED_JSESSIONID=DEFD9D7FC4D14DC88E9132EC2E4CC21D'

def get_jialefu_ver(phone):
    global cie
    headers = {'Host': 'www.carrefour.cn',
               'Connection': 'keep-alive',
               'Content-Length': '44',
               'Origin': 'file://',
               'language': 'zh-CN',
               'channel': 'production',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
               'normalSubsiteId': '58',
               'Accept': 'application/json, text/plain, */*',
               'osVersion': '8.1',
               'unique': 'android-kw4bz6df1ophmrls',
               'subsiteId': '58',
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
               'os': 'android',
               'appVersion': '2.8.0',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,en-US;q=0.9',
               'Cookie': cie,
               'X-Requested-With': 'cn.carrefour.app.mobile'}

    cookie_jar = RequestsCookieJar()
    cookie_jar.set("Cookie", cie)
    parameter = "param=%7B%22mobile%22%3A%22" + phone + "%22%7D"
    # param = {"param": parameter}
    response = requests.post("https://www.carrefour.cn/mobile/api/user/getLoginVerifyCode", cookies=cookie_jar,
                             data=parameter, headers=headers)
    result = {"phone": phone}
    if "SUCCESS" in response.text.encode("utf8"):
        return result
    return ""


def get_jialefu_login(ver, phone):
    global cie
    headers = {'Host': 'www.carrefour.cn',
               'Connection': 'keep-alive',
               'Content-Length': '81',
               'Origin': 'file://',
               'language': 'zh-CN',
               'channel': 'production',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
               'normalSubsiteId': '58',
               'Accept': 'application/json, text/plain, */*',
               'osVersion': '8.1',
               'unique': 'android-kw4bz6df1ophmrls',
               'subsiteId': '58',
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
               'os': 'android',
               'appVersion': '2.8.0',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,en-US;q=0.9',
               'Cookie': cie,
               'X-Requested-With': 'cn.carrefour.app.mobile'}

    cookie_jar = RequestsCookieJar()
    cookie_jar.set("Cookie", cie)
    parameter = "param=%7B%22loginName%22%3A%22" + phone + "%22%2C%22verifyCode%22%3A%22" + ver + "%22%7D"
    # param = {"param": parameter}
    response = requests.post("https://www.carrefour.cn/mobile/api/user/verifyCodeLogin", cookies=cookie_jar,
                             data=parameter, headers=headers)
    return response.data.encode("utf8")


# 查看奖励金
def get_jialefu_youhui(result):
    global cie
    headers = {'Host': 'www.carrefour.cn',
               'Connection': 'keep-alive',
               'channel': 'production',
               'language': 'zh-CN',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
               'normalSubsiteId': '58',
               'Accept': 'application/json, text/plain, */*',
               'osVersion': '8.1',
               'userid': result["id"],
               'userSession': result["userSession"],
               'subsiteId': '58',
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
               'os': 'android',
               'appVersion': '2.8.0',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,en-US;q=0.9',
               'Cookie': cie,
               'X-Requested-With': 'cn.carrefour.app.mobile'}
    cookie_jar = RequestsCookieJar()
    cookie_jar.set("Cookie", cie)
    response = requests.get("https://www.carrefour.cn/mobile/api/activity/coupon/getActivityCoupon?param=%7B%22type%22%3A154%7D", cookies=cookie_jar, headers=headers)
    return response.text.encode("utf8")



def get_jialefu_password(result):
    global cie
    headers = {'Host': 'www.carrefour.cn',
               'Connection': 'keep-alive',
               'channel': 'production',
               'language': 'zh-CN',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
               'normalSubsiteId': '58',
               'Accept': 'application/json, text/plain, */*',
               'osVersion': '8.1',
               'userid': result["id"],
               'userSession': result["userSession"],
               'subsiteId': '58',
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
               'os': 'android',
               'appVersion': '2.8.0',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,en-US;q=0.9',
               'Cookie': cie,
               'X-Requested-With': 'cn.carrefour.app.mobile'}

    cookie_jar = RequestsCookieJar()
    cookie_jar.set("Cookie", cie)
    parameter = "param=%7B%22loginPassword%22%3A%22qwer123456%22%2C%22loginPasswordStrength%22%3A1%7D"
    # param = {"param": parameter}
    response = requests.post("https://www.carrefour.cn/mobile/api/account/setLoginPassword", cookies=cookie_jar,
                             data=parameter, headers=headers)
    return response.data.userSession.encode("utf8")


