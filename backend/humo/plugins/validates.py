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
    Args:
        val (str): 待校验的邮箱地址。
    Returns:
        bool: 如果邮箱格式合法，返回True；否则返回False。
    """
    pattern = r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    return True if re.match(pattern, val) else False
