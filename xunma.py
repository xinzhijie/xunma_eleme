# -*- coding: UTF-8 -*-
import requests
import re
import time
from eleme import get_ele, send, get_message_fruit
# 默认token
token = "Z8OEvGM7XuVrWuZPOxHez&LkMd7YLad64"
item_id = 3361


# 获取饿了么号码并发送验证码
def get_phones():
    global item_id
    return requests.get("http://xapi.xunma.net/getPhone?ItemId=%s&token=%s&Count=1" % (item_id, token))\
        .text.encode("utf-8").strip().split(";")


def get_verification():
    global token
    global item_id
    # 判断token是否过期
    phones = get_phones()
    while "False" in ''.join(phones):
        token = (re.findall(r"(.+?)&", requests.get("http://xapi.xunma.net/Login?uName=limeichao&pWord=limeichao1").text))[0]
        phones = get_phones()
    # 获取饿了么号码的验证码
    for phone in phones:
        if phone:
            result = get_ele(phone)
            code = ''
            # 计数器
            i = 0
            while True:
                i = i + 1
                code = requests.get("http://xapi.xunma.net/getMessage?token=%s&itemId=%s&phone=%s" % (token, item_id, phone)).text.encode("utf8")
                if "验证码" in code:
                    code = re.findall(r"验证码是(.+?)，", code)[0]
                    break
                # 计数器为20 停止并放弃号码
                if i > 20:
                    break
                time.sleep(2)
            # 释放手机号
            requests.get("http://xapi.xunma.net/releasePhone?token=%s&phoneList=%s-%s;" % (token, phone, item_id))
            result["code"] = code
            result["phone"] = phone
            if code != "Null":
                return result


# 循环三次
j = 0
while j < 1:
    j = j + 1
    result_ele = get_verification()
    print result_ele["phone"]
    print result_ele["code"]
    print get_message_fruit(send(result_ele["phone"], result_ele["validate_token"], result_ele["code"]))
    requests.get("http://xapi.xunma.net/Exit?token=%s" % token)
