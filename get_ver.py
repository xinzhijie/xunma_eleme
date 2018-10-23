# -*- coding: UTF-8 -*-
# 获取验证码
import requests
import re
import time
token = "Z8OEvGM7XuVrWuZPOxHez&LkMd7YLad64"
item_id = 3361


def get_phones():
    global item_id
    return requests.get("http://xapi.xunma.net/getPhone?ItemId=%s&token=%s&Count=1&Phone=17136398024" % (item_id, token))\
        .text.encode("utf-8").strip().split(";")


phones = get_phones()
while "False" in ''.join(phones):
    token = (re.findall(r"(.+?)&", requests.get("http://xapi.xunma.net/Login?uName=limeichao&pWord=limeichao3").text))[0]
    phones = get_phones()
print token
if phones[0]:
    code = ''
    # 计数器
    i = 0
    while True:
        i = i + 1
        code = requests.get(
            "http://xapi.xunma.net/getMessage?token=%s&itemId=%s&phone=%s" % (token, item_id, phones[0])).text.encode(
            "utf8")
        if "验证码" in code:
            code = re.findall(r"验证码是(.+?)，", code)[0]
            print code
            break
        # 计数器为20 停止并放弃号码
        if i > 20:
            break
        time.sleep(2)
requests.get("http://xapi.xunma.net/Exit?token=%s" % token)
