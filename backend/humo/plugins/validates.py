#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 02:16
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : validates.py
# @Software    : PyCharm
# @Description :
import re


def verify_email(val: str) -> bool:
    """
    校验邮箱格式是否合法。
    """
    pattern = r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    return bool(re.match(pattern, val))


def verify_mobile(val: str) -> bool:
    """
    校验手机号格式是否合法
    :return:
    """
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, val))
