# -*- coding: UTF-8 -*-
import requests
from verification_code import get_code
import json
import base64
from requests.cookies import RequestsCookieJar


# 获取验证码图片并下载为code.jpg
def get_captcha_hash(phone):
    param1 = {"captcha_str": phone}
    verification = requests.post("https://h5.ele.me/restapi/eus/v3/captchas", data=param1).text.encode("utf-8")
    verification = json.loads(verification)
    captcha_hash = verification["captcha_hash"].encode("utf-8")
    # base64 转图片
    captcha_image = verification["captcha_image"].replace("data:image/jpeg;base64,", "")
    img_data = base64.b64decode(captcha_image)
    # 下载为code.jpg
    file_code = open('code.jpg', 'wb')
    file_code.write(img_data)
    file_code.close()
    code = get_code()
    # 请求发送手机短信验证码
    param1 = {"mobile": phone, "captcha_value": code, "captcha_hash": captcha_hash}
    state = requests.post("https://h5.ele.me/restapi/eus/login/mobile_send_code", data=param1).text.encode("utf-8")
    # 返回结果 正确的：列表结果  错误的：字符串
    return state


# 发送手机短信验证码
def get_ele(phone):
    param = {"mobile": phone, "captcha_value": "", "captcha_hash": ""}
    response = requests.post("https://h5.ele.me/restapi/eus/login/mobile_send_code", data=param).text.encode("utf-8")
    result = json.loads(response)
    if "账户存在风险" in response:
        # 存在风险调用验证码
        result = get_captcha_hash(phone)
        while "验证码错误" in result:
            # 错误重新调用
            result = get_captcha_hash(phone)
        result = json.loads(result)
    # 返回结果result = ｛"validate_token"： “sdsdsad”｝
    return result


# 登陆 获取SID
def send(phone, validate_token, phone_code):
    param = {"mobile": phone, "validate_code": phone_code, "validate_token": validate_token}
    response = requests.post("https://h5.ele.me/restapi/eus/login/login_by_mobile", data=param)
    temp = str(response.cookies.get("SID"))
    result = json.loads(response.text.encode("utf8"))
    result["SID"] = temp
    # 返回SID 返回user_id
    return result


# 登陆成功拿这SID 抽奖
def get_message(result):
    cookie_jar = RequestsCookieJar()
    cookie_jar.set("SID", result["SID"])
    param = {"channel": "app_activity_1"}
    response = requests.post("https://h5.ele.me/restapi/member/v1/users/%s/supervip/growth/prize" % result["user_id"], cookies=cookie_jar, data=param)
    return response.text.encode("utf8")

