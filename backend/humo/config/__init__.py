#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 01:13
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py
# @Software    : PyCharm
# @Description :
import os
from typing import Optional

from humo.config.config_schemas import ConfigSchema, DBItemSchema, RedisItemSchema
from root_path import ROOT_PATH


class Singleton:
    _instance: Optional[ConfigSchema] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            env_file = {
                'dev': f'{ROOT_PATH}/humo/config/dev_config.json',
                'prod': f'{ROOT_PATH}/humo/config/prod_config.json',
            }[os.environ.get('ENVIRONMENT', 'dev')]
            cls._instance = ConfigSchema.from_json(env_file)
        return cls._instance


def humo_config() -> ConfigSchema:
    return Singleton.get_instance()


config: ConfigSchema = humo_config()
