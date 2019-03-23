# -*- coding: UTF-8 -*-
import requests
import re
import time
from jialefu import get_jialefu_ver, get_jialefu_login, get_jialefu_youhui, get_jialefu_password, get_jialefu_list
# 默认token
token = "01122947651cac1af3f107a7bdc1481165ad22a70b01"
# 家乐福
item_id = 10596


# 获取饿了么号码并发送验证码
def get_phones():
    global token
    global item_id
    return requests.get("http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=%s&itemid=%s" % (token, item_id))\
        .text.encode("utf-8").strip().split(";")


def get_verification():
    global token
    global item_id
    # 判断token是否过期
    phones = get_phones()
    while "过期" in ''.join(phones):
        print("token过期")
        return
    print token
    if "余额不足" in ''.join(phones):
        print("余额不足")
        return
    # 获取号码
    for phone in phones:
        phone = phone[8:]
        if phone:
            # 家乐福
            result = get_jialefu_ver(phone)
            code = ''
            # 计数器
            i = 0
            while True:
                i = i + 1
                code = requests.get\
                    ("http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=%s&itemid=%s&mobile=%s&release=1" % (token, item_id, phone)).text
                if "success" in code:
                    print(code)
                    # 家乐福
                    code = re.findall(r"验证码为(.+?)，", code)[0]
                    break
                # 计数器为20 停止并放弃号码
                if i > 20:
                    break
                time.sleep(3)
            # 释放手机号
            requests.get("http://api.fxhyd.cn/UserInterface.aspx?action=release&token=%s&itemid=%s&mobile=%s" % (token, item_id, phone))
            # print result
            result["code"] = code
            result["phone"] = phone
            return result


try:
    j = 0
    while j < 1:
        stat = 0
        j = j + 1
        result_ele = get_verification()
        if result_ele["code"] != "Null":
            print "手机号：" + result_ele["phone"]
            result_a = get_jialefu_login(result_ele["code"], result_ele["phone"])
            result1 = get_jialefu_youhui(result_a)
            print result1
            print get_jialefu_password(result_a)
            result2 = get_jialefu_list(result_a)
            print result2
            if result2.find("199") != -1:
                print("1111111111111111111111111111111111111111111")
                break
except Exception as e:
    print('except:', e)
finally:
    print(token)
    # requests.get("http://xapi.xunma.net/Exit?token=%s" % token)
