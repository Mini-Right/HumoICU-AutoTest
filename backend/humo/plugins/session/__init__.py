#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 02:05
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from redis.client import Redis

from humo.config import config
from humo.plugins.session._mysql import MySQLSessionGenerate
from humo.plugins.session._redis import init_redis_session


class MySQLSession(object):
    HUMO = MySQLSessionGenerate(config.DB.HUMO).session


class RedisSession(object):
    pomelo: Redis = init_redis_session(config.REDIS.HUMO)
