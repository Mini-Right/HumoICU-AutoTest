#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/5/1 03:48
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : auth_user_info_service.py
# @Software    : PyCharm
# @Description :
from humo.databases.humo_system_user_table import HumoSystemUserTable
from humo.plugins.crypt.token import Token
from humo.plugins.curd import HumoTableCURD


class HumoAuthUserInfoService(object):
    @staticmethod
    def main(user_id: str):
        user_info: HumoSystemUserTable = HumoTableCURD().query_table_one(
            table_class=HumoSystemUserTable,
            params=[HumoSystemUserTable.user_id == user_id],
            is_dict=True
        )
        del user_info['password']
        return user_info
