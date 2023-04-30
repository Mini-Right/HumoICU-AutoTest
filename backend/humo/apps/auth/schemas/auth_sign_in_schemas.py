#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/5/1 02:36
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : auth_sign_in_schemas.py
# @Software    : PyCharm
# @Description :
from pydantic import BaseModel, Field


class HumoAuthSignInAccountSchema(BaseModel):
    username: str = Field(default=..., title='用户名')
    password: str = Field(default=..., title='密码')
