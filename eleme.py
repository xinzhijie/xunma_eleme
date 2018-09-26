# -*- coding: UTF-8 -*-
import requests
from verification_code import get_code
import json
import base64
from requests.cookies import RequestsCookieJar


def get_captcha_hash(phone):
    param1 = {"captcha_str": phone}
    verification = requests.post("https://h5.ele.me/restapi/eus/v3/captchas", data=param1).text.encode("utf-8")
    verification = json.loads(verification)
    captcha_hash = verification["captcha_hash"].encode("utf-8")
    captcha_image = verification["captcha_image"].replace("data:image/jpeg;base64,", "")
    img_data = base64.b64decode(captcha_image)
    file_code = open('code.jpg', 'wb')
    file_code.write(img_data)
    file_code.close()
    code = get_code()
    param1 = {"mobile": phone, "captcha_value": code, "captcha_hash": captcha_hash}
    state = requests.post("https://h5.ele.me/restapi/eus/login/mobile_send_code", data=param1).text.encode("utf-8")
    return state


def get_ele(phone):
    param = {"mobile": phone, "captcha_value": "", "captcha_hash": ""}
    response = requests.post("https://h5.ele.me/restapi/eus/login/mobile_send_code", data=param).text.encode("utf-8")
    result = json.loads(response)
    if "账户存在风险" in response:
        result = get_captcha_hash(phone)
        while "验证码错误" in result:
            result = get_captcha_hash(phone)
        result = json.loads(result)
    return result


def send(phone, validate_token, phone_code):
    param = {"mobile": phone, "validate_code": phone_code, "validate_token": validate_token}
    response = requests.post("https://h5.ele.me/restapi/eus/login/login_by_mobile", data=param)
    temp = str(response.cookies.get("SID"))
    result = json.loads(response.text.encode("utf8"))
    result["SID"] = temp
    return result


def get_message(result):
    cookie_jar = RequestsCookieJar()
    cookie_jar.set("SID", result["SID"])
    param = {"channel": "app_activity_1"}
    response = requests.post("https://h5.ele.me/restapi/member/v1/users/%s/supervip/growth/prize" % result["user_id"], cookies=cookie_jar, data=param)
    return response.text.encode("utf8")

