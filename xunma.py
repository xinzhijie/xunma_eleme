# -*- coding: UTF-8 -*-
import requests
import re
import time
from eleme import get_ele, send, get_message
# 默认token
token = "Z8OEvGM7XuVrWuZPOxHez&LkMd7YLad64"


# 获取饿了么号码并发送验证码
def get_phones():
    return requests.get("http://xapi.xunma.net/getPhone?ItemId=3361&token=%s&Count=1" % token).text.encode("utf-8")\
        .strip().split(";")


# 判断token是否过期
phones = get_phones()
while "False" in ''.join(phones):
    token = (re.findall(r"(.+?)&", requests.get("http://xapi.xunma.net/Login?uName=limeichao&pWord=limeichao").text))[0]
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
            code = requests.get("http://xapi.xunma.net/getMessage?token=%s&itemId=3361&phone=%s" % (token, phone)).text.encode("utf8")
            print code
            if "验证码" in code:
                code = re.findall(r"验证码是(.+?)，", code)[0]
                break
            # 计数器为20 停止并放弃号码
            if i > 20:
                break
            time.sleep(2)
        if code != "Null":
            print get_message(send(phone, result["validate_token"], code))
        # 释放手机号
        release = requests.get("http://xapi.xunma.net/releasePhone?token=%s&phoneList=%s-3361;" % (token, phone)).text
