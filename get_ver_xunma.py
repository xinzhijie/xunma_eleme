# -*- coding: UTF-8 -*-
# 获取验证码
import requests
import re
import time
token = "Z8OEvGM7XuVrWuZPOxHez&LkMd7YLad64"
# 家乐福
item_id = 3950
# 饿了么
# item_id = 3361

# 18482329763
# 13438035157

def get_phones():
    global item_id
    return requests.get("http://xapi.xunma.net/getPhone?ItemId=%s&token=%s&Count=1&Phone=18482231138" % (item_id, token))\
        .text.encode("utf-8").strip().split(";")


try:
    phones = get_phones()
    while "过期" in ''.join(phones):
        token = (re.findall(r"(.+?)&", requests.get("http://xapi.xunma.net/Login?uName=limeichao&pWord=limeichao").text))[0]
        phones = get_phones()
    print token
    if "没有" not in ''.join(phones) and "不在" not in ''.join(phones):
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
                    print code
                    break
                # 计数器为20 停止并放弃号码
                if i > 20:
                    break
                time.sleep(2)
    elif "余额不足" in ''.join(phones):
        print("余额不足")
    else:
        print("号码不存在")
except Exception as e:
    print('except:', e)
finally:
    requests.get("http://xapi.xunma.net/Exit?token=%s" % token)
