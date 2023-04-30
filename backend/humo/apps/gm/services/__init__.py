#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/5/9 21:20
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :

from humo.databases.humo_system_user_table import HumoSystemUserTable
from humo.plugins.curd import HumoTableCURD
from humo.plugins.logger import logger
from humo.plugins.session import RedisSession


def gm_reset_register_sms_send_count(mobile: str):
    """重置指定手机号注册发送短信次数"""
    redis_key = f"register:mobile_count:{mobile}"
    RedisSession.HUMO.delete(redis_key)
    logger.info(f"[GM-Tools] 重置指定手机号注册发送短信次数: {mobile}")


def gm_reset_register_sms_send_count_all():
    """重置全部手机号注册发送短信次数"""
    keys = RedisSession.HUMO.keys('register:mobile_count:*')
    [gm_reset_register_sms_send_count(mobile=_.split(':')[-1]) for _ in keys]


def gm_delete_user(username: str):
    """删除指定用户"""
    HumoTableCURD().delete(table_class=HumoSystemUserTable, params=[HumoSystemUserTable.username == username])
    logger.info(f"[GM-Tools] 删除指定用户: {username}")


def gm_delete_user_all():
    """删除全部用户"""
    HumoTableCURD().delete(table_class=HumoSystemUserTable, params=[])
    logger.info(f"[GM-Tools] 删除全部用户")


if __name__ == '__main__':
    gm_delete_user_all()
