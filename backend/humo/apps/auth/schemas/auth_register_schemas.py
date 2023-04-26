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
    email: str = Field(default=None, title='邮箱')
    mobile: str = Field(default=None, title='手机号')
    code: str = Field(default=None, title='验证码')
    register_type: str = Field(default=None, title='注册类型  email / mobile')


class HumoAuthEmailRegisterSchema(BaseModel):
    username: str = Field(default=..., title='用户名')
    password: str = Field(default=..., title='密码')
    email: str = Field(default=..., title='邮箱')


class HumoAuthMobileRegisterSchema(BaseModel):
    username: str = Field(default=..., title='用户名')
    password: str = Field(default=..., title='密码')
    mobile: str = Field(default=..., title='手机号')
    code: str = Field(default=..., title='验证码')
