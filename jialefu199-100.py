# -*- coding: UTF-8 -*-
from requests.cookies import RequestsCookieJar
import requests

cieList = ['DISTRIBUTED_JSESSIONID=0359B14152EC11E9A8B908D40C5DDD82', 'DISTRIBUTED_JSESSIONID=1689029252EF11E9AF3008D40C5DDD82']
equipmentList = ['android-9a47c08d40c5ddd82', 'android-99b2f08d40c5ddd82']
useridList = ['258932956', '258439776']
userSessionList = ['BF14874D438EADE08FE589CDC6223986', '8F6C131D696BF404B9B5E47C6683DF5C']
phoneList = ['18711456044', '13408648838']


def get_jialefu_youhui(cie, equipment, user_id, user_session, phone):

    headers = {'Host': 'www.carrefour.cn',
               'Connection': 'keep-alive',
               'channel': 'production',
               'unique': equipment,
               'language': 'zh-CN',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
               'normalSubsiteId': '58',
               'Accept': 'application/json, text/plain, */*',
               'osVersion': '8.1',
               'userid': user_id,
               'userSession': user_session,
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
    response = requests.get("https://www.carrefour.cn/mobile/api/activity/coupon/getActivityCoupon?param=%7B%22type%22%3A262%7D", cookies=cookie_jar, headers=headers)
    return response.text.encode("utf8")


for index in range(len(phoneList)):
    print get_jialefu_youhui(cieList[index], equipmentList[index], useridList[index], userSessionList[index], phoneList[index])
