#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 22:57
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :

from alibabacloud_tea_openapi import models as open_api_models

from humo.config import config


class AliYunService(object):
    def __init__(self):
        self.config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=config.ALIYUN.AccessKeyId,
            # 必填，您的 AccessKey Secret,
            access_key_secret=config.ALIYUN.AccessKeySecret,
        )
