#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 01:13
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py
# @Software    : PyCharm
# @Description :
from typing import Optional

from humo.config.config_schemas import ConfigSchema


class Singleton:
    _instance: Optional[ConfigSchema] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ConfigSchema()
        return cls._instance


def humo_config() -> ConfigSchema:
    return Singleton.get_instance()


config: ConfigSchema = humo_config()
