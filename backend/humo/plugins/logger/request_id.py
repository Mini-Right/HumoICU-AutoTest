#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 01:16
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : contextvars.py
# @Software    : PyCharm
# @Description :
import contextvars

# 创建全局上下文变量 request_id_var
request_id_var = contextvars.ContextVar('request_id')


# 辅助函数 get_request_id 和 set_request_id
def get_request_id():
    return request_id_var.get('-')


def set_request_id(request_id):
    request_id_var.set(request_id)
