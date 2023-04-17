#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 00:50
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : config.schemas.py
# @Software    : PyCharm
# @Description :
import os

from pydantic import BaseSettings, Field

from root_path import ROOT_PATH


class ConfigSchema(BaseSettings):
    JWT_SECRET: str = Field(default=..., title='JWT_SECRET')
    REQUEST_TIMEOUT: int = Field(default=..., title='REQUEST_TIMEOUT')

    class Config:
        env_file = {
            'dev': f'{ROOT_PATH}/humo/config/dev_config.toml',
            'prod': f'{ROOT_PATH}/humo/config/prod_config.toml',
        }[os.environ.get('ENVIRONMENT', 'dev')]
