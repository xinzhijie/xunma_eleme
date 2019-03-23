# -*- coding: UTF-8 -*-
import requests
import json
import re


token = "Z8OEvGM7XuVrWuZPOxHez&LkMd7YLad64"
# haidilao
item_id = 13236


# 获取饿了么号码并发送验证码
def get_phones():
    global token
    global item_id
    return requests.get("http://xapi.xunma.net/getPhone?ItemId=%s&token=%s&Count=1" % (item_id, token))\
        .text.encode("utf-8").strip().split(";")


def get_verification():
    global token
    global item_id
    # 判断token是否过期
    phones = get_phones()
    while "过期" in ''.join(phones):
        print("token过期")
        token = (re.findall(r"(.+?)&", requests.get("http://xapi.xunma.net/Login?uName=limeichao&pWord=limeichao").text))[0]
        phones = get_phones()
    print token
    if "余额不足" in ''.join(phones):
        print("余额不足")
        return
    # 获取饿了么号码的验证码
    for phone in phones:
        if phone:
            result = dongjianzhe(phone)
            # 释放手机号
            requests.get("http://xapi.xunma.net/releasePhone?token=%s&phoneList=%s-%s;" % (token, phone, item_id))
            return result


def dongjianzhe(phone):

    headers = {'Content-Type': 'application/json;charset=utf-8',
                   'Host': 'dj.shenmk.com',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'}
    param = {"countryCode":"+86","telephone": phone}

    verification = requests.post("https://dj.shenmk.com/api/base/customer/captcha/send/sms",
                                 data=json.dumps(param), headers=headers).text.encode("utf-8")

    if "用户未注册" in verification:
        return "0"
    else:
        print phone
        return "1"


try:
    j = 0
    while j < 2:
        stat = 0
        j = j + 1
        result_ele = get_verification()
        if result_ele == "1":
            break
        if result_ele == "0":
            print "0"
except Exception as e:
    print('except:', e)
finally:
    # print(token)
    requests.get("http://xapi.xunma.net/Exit?token=%s" % token)
