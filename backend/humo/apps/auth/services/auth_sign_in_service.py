#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/5/1 02:34
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : auth_sign_in.py
# @Software    : PyCharm
# @Description :
from humo.apps.auth.schemas.auth_sign_in_schemas import HumoAuthSignInAccountSchema
from humo.config import config
from humo.config.redis_key import REDIS_KEY_SIGN_IN_ERROR_COUNT, REDIS_KEY_USER_TOKEN
from humo.databases.humo_system_user_table import HumoSystemUserTable
from humo.plugins.crypt import Password
from humo.plugins.crypt.token import Token
from humo.plugins.curd import HumoTableCURD
from humo.plugins.logger import logger
from humo.plugins.session import RedisSession
from humo.plugins.time_utils import get_seconds_until_tomorrow


class HumoAuthSignInService(object):
    def __init__(self):
        pass

    @staticmethod
    def __sign_in_error_count(username: str):
        """登录失败次数"""
        sign_in_error_count = RedisSession.HUMO.get(REDIS_KEY_SIGN_IN_ERROR_COUNT.format(username=username))
        logger.info(f"账号当日登录失败次数 {username}: {sign_in_error_count}")
        if sign_in_error_count is not None and int(sign_in_error_count) > 5:
            HumoTableCURD().update(
                table_class=HumoSystemUserTable,
                params=[HumoSystemUserTable.username == username],
                update=dict(status=1)
            )
            raise Exception('账号当日登录失败次数过多 请明日再试')

    def verify(self, data: HumoAuthSignInAccountSchema, user_info: HumoSystemUserTable):
        if not user_info:
            raise Exception('账号不存在')
        if not Password().verify_password(plain_password=data.password, hashed_password=user_info.password):
            redis_count_key = REDIS_KEY_SIGN_IN_ERROR_COUNT.format(username=data.username)
            RedisSession.HUMO.incr(name=redis_count_key)
            RedisSession.HUMO.expire(name=redis_count_key, time=get_seconds_until_tomorrow())
            self.__sign_in_error_count(username=data.username)
            raise Exception('密码错误 请重试')
        if user_info.active == 0:
            raise Exception('账号未激活')
        if user_info.status == 0:
            raise Exception('账号已被禁用')


class HumoAuthSignInAccountService(HumoAuthSignInService):
    def __init__(self):
        super().__init__()

    def main(self, data: HumoAuthSignInAccountSchema):
        user_info: HumoSystemUserTable = HumoTableCURD().query_table_one(
            table_class=HumoSystemUserTable,
            params=[HumoSystemUserTable.username == data.username]
        )
        self.verify(data=data, user_info=user_info)
        user_token = Token.create_access_token(subject=user_info.user_id)
        RedisSession.HUMO.set(
            name=REDIS_KEY_USER_TOKEN.format(user_id=user_info.user_id),
            value=user_token,
            ex=config.REQUEST_TIMEOUT
        )
        return {'token': user_token}


if __name__ == '__main__':
    print(Password().verify_password('123456', '$2b$12$yZ.es677.a0J.K4gWakLDOHG7BOfQbkIWUtGbd.a4GQsKfUmMgnpm'))