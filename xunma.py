# -*- coding: UTF-8 -*-
import requests
import re
import time
from eleme import get_ele, send, get_message_phone, get_message_fruit, get_bonus
from jialefu import get_jialefu_ver, get_jialefu_login, get_jialefu_youhui, get_jialefu_password
# 默认token
token = "Z8OEvGM7XuVrWuZPOxHez&LkMd7YLad64"
# 饿了么
# item_id = 3361

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
            # 饿了么
            # result = get_ele(phone)
            code = ''
            # 计数器
            i = 0
            while True:
                i = i + 1
                code = requests.get("http://xapi.xunma.net/getMessage?token=%s&itemId=%s&phone=%s" % (token, item_id, phone)).text.encode("utf8")
                if "验证码" in code:
                    # 饿了么
                    # code = re.findall(r"验证码是(.+?)，", code)[0]

                    # 家乐福
                    code = re.findall(r"验证码为(.+?)，", code)[0]
                    break
                # 计数器为20 停止并放弃号码
                if i > 20:
                    break
                time.sleep(2)
            # 释放手机号
            requests.get("http://xapi.xunma.net/releasePhone?token=%s&phoneList=%s-%s;" % (token, phone, item_id))
            result["code"] = code
            result["phone"] = phone
            return result


# # 循环三次
# j = 0
# while j < 5:
#     stat = 0
#     j = j + 1
#     result_ele = get_verification()
#     if result_ele["code"] != "Null":
#         print "手机号：" + result_ele["phone"]
#         result_a = send(result_ele["phone"], result_ele["validate_token"], result_ele["code"])
#         # 抽奖新用户和果蔬红包
#         print get_message_fruit(result_a)
#         # 判断商超红包
#         shangchao = get_message_phone(result_a)
#         # 判断奖励金和会员
#         jianglijin = get_bonus(result_a)
#         print shangchao
#         if "超级会员不存在或已过期" not in jianglijin:
#             stat = stat + 1
#             print "该账号有会员"
#             print "11111111111111111111111111111111111111111111111111111111"
#         if "商超首单" in shangchao :
#             print "该账号有商超首单红包"
#             print "22222222222222222222222222222222222222222222222222222222"
#             stat = stat + 1
#         if "超市新客礼" in shangchao:
#             print "该账号有超市新客礼红包"
#             print "22222222222222222222222222222222222222222222222222222222"
#             stat = stat + 1
#         if "首单红包" in shangchao:
#             stat = stat + 1
#             print "该账号有新用户首单红包"
#             print "33333333333333333333333333333333333333333333333333333333"
#         if stat > 0:
#             break
# print(token)
# requests.get("http://xapi.xunma.net/Exit?token=%s" % token)


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
print(token)
requests.get("http://xapi.xunma.net/Exit?token=%s" % token)
