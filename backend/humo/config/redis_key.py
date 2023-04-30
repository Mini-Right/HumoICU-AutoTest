#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/5/1 02:55
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : redis_key.py
# @Software    : PyCharm
# @Description :

# 登录失败次数
REDIS_KEY_SIGN_IN_ERROR_COUNT = 'sign_in:error:{username}'

# 用户token
REDIS_KEY_USER_TOKEN = 'user:{user_id}:token'


# 注册短信发送次数
REDIS_KEY_REGISTER_SEND_CODE_COUNT = "register:mobile_count:{mobile}"

# 注册短信验证码
REDIS_KEY_REGISTER_MOBILE_CODE = "register:mobile:{mobile}"

# 注册邮箱激活
REDIS_KEY_REGISTER_EMAIL = "register:email:{token}"
