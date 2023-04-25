#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 00:07
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : auth_register_schemas.py
# @Software    : PyCharm
# @Description :
from pydantic import BaseModel, Field


class HumoAuthRegisterSchema(BaseModel):
    username: str = Field(default=..., title='用户名')
    password: str = Field(default=..., title='密码')
    email: str = Field(default=..., title='邮箱')
