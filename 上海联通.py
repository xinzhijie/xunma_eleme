# -*- coding: UTF-8 -*-
# 获取验证码
import requests
import re


def get_phones(token):
    return requests.get(
        "https://cdh.10010sh.cn/cucase/front/newOpen/selectNumber.shtml?page=%s&section&actiId=0fae23db5e164ef78cf8a93c5a70ca3d" % (token))\
        .text.encode("utf-8")


# f2 = open('test.txt', 'r+')
# for i in range(1000):
#     temp = get_phones(i + 1)
#     if 'numberList' in eval(temp).keys():
#         print(i + 1)
#     else:
#         break
#     for item in eval(temp)['numberList']:
#         # if re.match(r'"(?:0(?=1)|1(?=2)|2(?=3)|3(?=4)|4(?=5)|5(?=6)|6(?=7)|7(?=8)|8(?=9)){5}\d', '11212'):
#         f2.write(item + ',')
#         print item

def read_file(path):
    with open(path, 'r+') as f:
        str1 = f.read()
    return str1.strip()


temp = read_file("test.txt").split(",")
temp.sort()
# f2 = open('sort.txt', 'r+')
for item in temp:
    # f2.write(item + ',')
    if re.match(r'^\d*(\d)\1(\d)\2$', item):
        print item
