# -*- coding: UTF-8 -*-
import requests
import re
import time
from eleme import get_ele, send, get_message_phone, get_message_fruit, get_bonus
from jialefu import get_jialefu_ver, get_jialefu_login, get_jialefu_youhui, get_jialefu_password, get_jialefu_list
# 默认token
token = "Z8OEvGM7XuVrWuZPOxHez&LkMd7YLad64"
# 家乐福
item_id = 3950


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
            # 家乐福
            result = get_jialefu_ver(phone)
            code = ''
            # 计数器
            i = 0
            while True:
                i = i + 1
                code = requests.get("http://xapi.xunma.net/getMessage?token=%s&itemId=%s&phone=%s" % (token, item_id, phone)).text.encode("utf8")
                if "验证码" in code:
                    print(code)
                    # 家乐福
                    code = re.findall(r"验证码为(.+?)，", code)[0]
                    break
                # 计数器为20 停止并放弃号码
                if i > 20:
                    break
                time.sleep(2)
            # 释放手机号
            requests.get("http://xapi.xunma.net/releasePhone?token=%s&phoneList=%s-%s;" % (token, phone, item_id))
            # print result
            result["code"] = code
            result["phone"] = phone
            return result


# import time
# date = 10
# while date > 0:
#     t = time.time()
#     date = 1543881630 - int(t)
#     if date < 0:
#         date = 0
#     time.sleep(date/2)
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
    # print(token)
    requests.get("http://xapi.xunma.net/Exit?token=%s" % token)
