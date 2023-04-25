#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/25 22:24
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : redis.py
# @Software    : PyCharm
# @Description :
from redis import StrictRedis

from humo.config import RedisItemSchema


def init_redis_session(redis_config: RedisItemSchema):
    session = StrictRedis(
        host=redis_config.host,
        port=redis_config.port,
        db=redis_config.db,
        password=redis_config.password,
        decode_responses=True,
    )
    return session
